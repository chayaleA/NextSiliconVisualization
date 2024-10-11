#ifdef USE_ONEAPI
#pragma once
#pragma warning(push, 0)
#include <sycl.hpp>
#include <tbb/parallel_for.h>
#include <tbb/blocked_range.h>
#pragma warning(pop)
#include <future>
#include <thread>
#include <mutex>
#include <omp.h>
#include <unordered_map>
#include "../Logging/LogReader.hpp"
#include "../Models/LogOnGpu.hpp"
#include "../Utilities/Config.hpp"
#include "../Utilities/CustomExceptions.hpp"

using namespace sycl;

using namespace std;

class GPULogReader : public LogReader
{
public:

	GPULogReader(const string& path) :LogReader(path) {}

	/**
	* @brief Processes logs on the GPU.
	* @param logs Vector of logs to be processed.
	* @param tidCount Unordered map for tracking thread IDs count.
	* @param unitCount Unordered map for tracking unit counts.
	* @param areaCount Unordered map for tracking area counts.
	* @param clusterCount Unordered map for tracking cluster counts.
	* @param quadCount Unordered map for tracking quad counts.
	*/
	void processLogsOnGPU(std::vector<LogOnGpu>&,
		std::unordered_map<int, int>&,
		std::unordered_map<std::string, int>&,
		std::unordered_map<std::string, int>&,
		std::unordered_map<Cluster, int>&,
		std::unordered_map<std::tuple<int, int, int>, int>&);

	/**
	* @brief Reads logs in parallel and updates counts.
	* @param numThreads The number of threads to use for parallel processing.
	* @param tidCount Unordered map for tracking thread IDs count.
	* @param unitCount Unordered map for tracking unit counts.
	* @param areaCount Unordered map for tracking area counts.
	* @param clusterCount Unordered map for tracking cluster counts.
	* @param quadCount Unordered map for tracking quad counts.
	*/
	void getNextInParallel(size_t,
		std::unordered_map<int, int>&,
		std::unordered_map<std::string, int>&,
		std::unordered_map<std::string, int>&,
		std::unordered_map<Cluster, int>&,
		std::unordered_map<std::tuple<int, int, int>, int>&);

private:

	std::mutex map_mutex;

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
	std::ifstream openFileAtChunk(const std::string&, size_t, size_t);

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
	std::vector<LogOnGpu> readLogsFromChunk(std::ifstream&, size_t, size_t, size_t, size_t);
};

#endif