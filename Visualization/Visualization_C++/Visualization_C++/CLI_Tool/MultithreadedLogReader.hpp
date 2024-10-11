#pragma once
#include <future>
#include <thread>
#include <queue>
#include <mutex>
#include <unordered_map>
#include "../Logging/LogReader.hpp"
#include "../Utilities/Config.hpp"
#include "../Utilities/CustomExceptions.hpp"

using namespace std;

class MultithreadedLogReader : public LogReader
{
public:
	MultithreadedLogReader(const string& path) :LogReader(path) {}

	/**
	* @brief Reads and counts log entries using multiple threads.
	* @param tidCount Unordered map for tracking thread IDs count.
	* @param areaCount Unordered map for tracking area counts.
	* @param unitCount Unordered map for tracking unit counts.
	* @param clusterCount Unordered map for tracking cluster counts.
	* @param quadCount Unordered map for tracking quad counts.
	*/
	void readAndCountFileByThreads(unordered_map<int, int>&,
		unordered_map<string, int>&,
		unordered_map<string, int>&,
		unordered_map<Cluster, int>&,
		unordered_map<tuple<int, int, int>, int>&);

private:
	std::queue<std::string> logLineQueue;    
	std::queue<Log> logObjectQueue;          

	std::mutex lineQueueMutex, logQueueMutex;
	std::condition_variable cvLine, cvLog;   
	bool doneReading = false;				 
	bool doneParsing = false;				 

	/**
	* @brief Thread function for reading log lines from the file.
	*/
	void fileReadingThread();

	/**
	* @brief Thread function for parsing log lines into log objects.
	*/
	void logParsingThread();

	/**
	* @brief Thread function for mapping log objects to counts.
	* @param tidCount Unordered map for tracking thread IDs count.
	* @param areaCount Unordered map for tracking area counts.
	* @param unitCount Unordered map for tracking unit counts.
	* @param clusterCount Unordered map for tracking cluster counts.
	* @param quadCount Unordered map for tracking quad counts.
	*/
	void logMappingThread(unordered_map<int, int>&,
		unordered_map<string, int>&,
		unordered_map<string, int>&,
		unordered_map<Cluster, int>&,
		unordered_map<tuple<int, int, int>, int>&);
};
