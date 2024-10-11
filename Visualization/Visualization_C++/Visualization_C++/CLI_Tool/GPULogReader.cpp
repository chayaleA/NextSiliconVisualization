#ifdef USE_ONEAPI
#include "GPULogReader.hpp"

/**
* @brief Processes logs on the GPU.
* @param logs Vector of logs to be processed.
* @param tidCount Unordered map for tracking thread IDs count.
* @param unitCount Unordered map for tracking unit counts.
* @param areaCount Unordered map for tracking area counts.
* @param clusterCount Unordered map for tracking cluster counts.
* @param quadCount Unordered map for tracking quad counts.
*/
void GPULogReader::processLogsOnGPU(
    std::vector<LogOnGpu>& logs,
    std::unordered_map<int, int>& tidCount,
    std::unordered_map<std::string, int>& unitCount,
    std::unordered_map<std::string, int>& areaCount,
    std::unordered_map<Cluster, int>& clusterCount,
    std::unordered_map<std::tuple<int, int, int>, int>& quadCount) {

    size_t logSize = logs.size();
    if (logSize == 0) {
        return;
    }

    sycl::queue syclTaskQueue;

    LogOnGpu* logs_gpu = sycl::malloc_shared<LogOnGpu>(logSize, syclTaskQueue);
    int* counts = sycl::malloc_shared<int>(logSize * 3, syclTaskQueue);
    int* clusters = sycl::malloc_shared<int>(logSize * 5, syclTaskQueue);

    std::copy(logs.begin(), logs.end(), logs_gpu);

    size_t group_size = syclTaskQueue.get_device().get_info<sycl::info::device::max_work_group_size>();
    size_t global_size = ((logSize + group_size - 1) / group_size) * group_size;

    try {
        syclTaskQueue.submit([&](sycl::handler& syclHandler) {
            syclHandler.parallel_for(sycl::nd_range<1>(sycl::range<1>(global_size), sycl::range<1>(group_size)),
                [=](sycl::nd_item<1> item) {
                    size_t i = item.get_global_id(0);
                    if (i >= logSize) return;

                    const auto& log = logs_gpu[i];
                    counts[i * 3] = 1;
                    counts[i * 3 + 1] = 1;
                    counts[i * 3 + 2] = 1;

                    clusters[i * 5] = log.chip;
                    clusters[i * 5 + 1] = log.die;
                    clusters[i * 5 + 2] = log.quad;
                    clusters[i * 5 + 3] = log.row;
                    clusters[i * 5 + 4] = log.col;
                });
            }).wait_and_throw();
    }
    catch (const sycl::exception& e) {
        throw SYCLException("SYCL exception caught:" + string(e.what()));
    }

    std::lock_guard<std::mutex> lock(map_mutex);

#pragma omp parallel for
    for (size_t i = 0; i < logSize; ++i) {
        tidCount[logs[i].tid] += counts[i * 3];
        unitCount[logs[i].unit] += counts[i * 3 + 1];
        areaCount[logs[i].area] += counts[i * 3 + 2];

        Cluster cluster = {
            clusters[i * 5], clusters[i * 5 + 1], clusters[i * 5 + 2],
            clusters[i * 5 + 3], clusters[i * 5 + 4]
        };

        clusterCount[cluster] += 1;
        auto quad_key = std::make_tuple(clusters[i * 5], clusters[i * 5 + 1], clusters[i * 5 + 2]);
        quadCount[quad_key] += 1;
    }

    sycl::free(logs_gpu, syclTaskQueue);
    sycl::free(counts, syclTaskQueue);
    sycl::free(clusters, syclTaskQueue);
}

/**
* @brief Reads logs in parallel and updates counts.
* @param numThreads The number of threads to use for parallel processing.
* @param tidCount Unordered map for tracking thread IDs count.
* @param unitCount Unordered map for tracking unit counts.
* @param areaCount Unordered map for tracking area counts.
* @param clusterCount Unordered map for tracking cluster counts.
* @param quadCount Unordered map for tracking quad counts.
*/
void GPULogReader::getNextInParallel(
    size_t numThreads,
    std::unordered_map<int, int>& tidCount,
    std::unordered_map<std::string, int>& unitCount,
    std::unordered_map<std::string, int>& areaCount,
    std::unordered_map<Cluster, int>& clusterCount,
    std::unordered_map<std::tuple<int, int, int>, int>& quadCount)
{
    size_t fileSize = getFileSize();
    if (fileSize == 0) {
        throw FileOpenException("File size is 0 or file could not be opened.");
        return;
    }
    size_t chunkSize = fileSize / numThreads;

    tbb::parallel_for(tbb::blocked_range<size_t>(0, numThreads),
        [&](const tbb::blocked_range<size_t>& r) {
            for (size_t i = r.begin(); i != r.end(); ++i) {
                std::ifstream file = openFileAtChunk(filePath, i, chunkSize);
                if (!file.is_open()) continue;

                std::vector<LogOnGpu> logs = readLogsFromChunk(file, i, chunkSize, numThreads, fileSize);

                processLogsOnGPU(logs, tidCount, unitCount, areaCount, clusterCount, quadCount);
            }
        });
}

/**
* @brief Opens a file at a specific chunk and skips to the beginning of the chunk.
*
* This function opens the log file, seeks to the position of the specified chunk,
* and ensures that the reading starts at the beginning of the next full line to avoid partial lines.
*
* @param filePath The path to the log file.
* @param chunkIndex The index of the chunk (0-based).
* @param chunkSize The size of each chunk in bytes.
* @return A file stream positioned at the start of the specified chunk.
*/
std::ifstream GPULogReader::openFileAtChunk(const std::string& filePath, size_t chunkIndex, size_t chunkSize) {
    std::ifstream file(filePath);
    if (!file.is_open()) {
        throw FileOpenException("LogReaderExtended::openFileAtChunk. filePath"+ filePath + "chunkIndex"+ to_string(chunkIndex)+ "chunkSize"+ to_string(chunkSize));
        return file;
    }
    file.seekg(chunkIndex * chunkSize);
    if (chunkIndex > 0) {
        std::string dummy;
        std::getline(file, dummy);
    }
    return file;
}

/**
* @brief Reads logs from a specified chunk in the file and converts them to GPU-compatible format.
*
* This function reads lines from the chunk assigned to a thread, parses each line as a log entry,
* and stores it in a vector of `LogOnGpu` objects. The function ensures that reading stops when the end of the chunk is reached.
*
* @param file The input file stream positioned at the start of the chunk.
* @param chunkIndex The index of the current chunk.
* @param chunkSize The size of each chunk in bytes.
* @param numThreads The total number of threads.
* @param fileSize The total size of the log file.
* @return A vector of logs (`LogOnGpu` format) read from the chunk.
*/
std::vector<LogOnGpu> GPULogReader::readLogsFromChunk(std::ifstream& file, size_t chunkIndex, size_t chunkSize, size_t numThreads, size_t fileSize) {
    std::vector<LogOnGpu> logs;
    std::string line;
    while (file.tellg() < (chunkIndex + 1 == numThreads ? fileSize : (chunkIndex + 1) * chunkSize) && std::getline(file, line)) {
        Log log;
        parseCSVLine(line, log);
        logs.emplace_back();
        logs.back().chip = log.clusterId.chip;
        logs.back().die = log.clusterId.die;
        logs.back().quad = log.clusterId.quad;
        logs.back().row = log.clusterId.row;
        logs.back().col = log.clusterId.col;
        logs.back().tid = log.tid;
        logs.back().setArea(log.area);
        logs.back().setUnit(log.unit);
    }
    return logs;
}

#endif