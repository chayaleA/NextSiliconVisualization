#include "MultithreadedLogReader.hpp"

/**
* @brief Reads and counts log entries using multiple threads.
* @param tidCount Unordered map for tracking thread IDs count.
* @param areaCount Unordered map for tracking area counts.
* @param unitCount Unordered map for tracking unit counts.
* @param clusterCount Unordered map for tracking cluster counts.
* @param quadCount Unordered map for tracking quad counts.
*/
void MultithreadedLogReader::readAndCountFileByThreads(
    unordered_map<int, int>& tidCount,
    unordered_map<string, int>& areaCount,
    unordered_map<string, int>& unitCount,
    unordered_map<Cluster, int>& clusterCount,
    unordered_map<tuple<int, int, int>, int>& quadCount) {

    // Start the file reading, parsing, and mapping threads
    std::thread readerThread(&MultithreadedLogReader::fileReadingThread, this);
    std::thread parserThread(&MultithreadedLogReader::logParsingThread, this);
    std::thread mapperThread(&MultithreadedLogReader::logMappingThread, this,
        std::ref(tidCount), std::ref(areaCount), std::ref(unitCount),
        std::ref(clusterCount), std::ref(quadCount));

    // Wait for all threads to finish.
    readerThread.join();
    parserThread.join();
    mapperThread.join();
}

/**
* @brief Thread function for reading log lines from the file.
*/
void MultithreadedLogReader::fileReadingThread() {
    std::ifstream file(filePath);
    if (!file.is_open()) {
        throw FileOpenException("LogReaderExtended::fileReadingThread - filePath: " + filePath);
        return;
    }

    std::string line;
    while (getline(file, line)) {
        {
            std::lock_guard<std::mutex> lock(lineQueueMutex);
            logLineQueue.push(line);  
        }
        cvLine.notify_one(); 
    }

    file.close();

    {
        std::lock_guard<std::mutex> lock(lineQueueMutex);
        doneReading = true;
    }
    cvLine.notify_all();  
}

/**
* @brief Thread function for parsing log lines into log objects.
*/
void MultithreadedLogReader::logParsingThread() {
    std::string line;
    Log log;

    while (true) {
        {
            std::unique_lock<std::mutex> lock(lineQueueMutex);
            cvLine.wait(lock, [this] { return !logLineQueue.empty() || doneReading; });

            if (!logLineQueue.empty()) {
                line = logLineQueue.front();
                logLineQueue.pop();
            }
            else if (doneReading && logLineQueue.empty()) {
                break;
            }
        }

        if (parseCSVLine(line, log)) {
            {
                std::lock_guard<std::mutex> lock(logQueueMutex);
                logObjectQueue.push(log);
            }
            cvLog.notify_one();
        }
    }

    {
        std::lock_guard<std::mutex> lock(logQueueMutex);
        doneParsing = true;
    }
    cvLog.notify_all();
}

/**
* @brief Thread function for mapping log objects to counts.
* @param tidCount Unordered map for tracking thread IDs count.
* @param areaCount Unordered map for tracking area counts.
* @param unitCount Unordered map for tracking unit counts.
* @param clusterCount Unordered map for tracking cluster counts.
* @param quadCount Unordered map for tracking quad counts.
*/
void MultithreadedLogReader::logMappingThread(
    unordered_map<int, int>& tidCount,
    unordered_map<string, int>& areaCount,
    unordered_map<string, int>& unitCount,
    unordered_map<Cluster, int>& clusterCount,
    unordered_map<tuple<int, int, int>, int>& quadCount) {

    Log log;

    while (true) {
        {
            std::unique_lock<std::mutex> lock(logQueueMutex);
            cvLog.wait(lock, [this] { return !logObjectQueue.empty() || doneParsing; });

            if (!logObjectQueue.empty()) {
                log = logObjectQueue.front();
                logObjectQueue.pop();
            }
            else if (doneParsing && logObjectQueue.empty()) {
                break;
            }
        }

        tidCount[log.tid]++;
        areaCount[log.area]++;
        unitCount[log.unit]++;
        clusterCount[log.clusterId]++;
        quadCount[std::make_tuple(log.clusterId.chip, log.clusterId.die, log.clusterId.quad)]++;
    }
}

