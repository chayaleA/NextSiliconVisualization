#pragma once
#ifdef USE_PYBIND
#include <pybind11/pybind11.h>
#endif
#include <fstream>
#include <string>
#include <sstream>
#include <iostream>
#include <ctime>
#include <cmath>
#include <regex>
#include <iomanip>
#include "../Utilities/Logger.hpp"
#include "../Utilities/CustomExceptions.hpp"

using namespace std;

#ifdef USE_PYBIND
namespace py = pybind11;
#endif

/**
 * @class LogsFactory
 * @brief A class for handling log file operations.
 */
class LogsFactory {
public:
	LogsFactory(const string& path) : filePath(path),logger(Logger::getInstance()) {}

	LogsFactory() : logger(Logger::getInstance()) {}
	 
	void setPath(const string&);

	time_t getFirstLogTime();

	time_t getLastLogTime();

	time_t getTimeFromLine(const string& line);

	string time_tToString(time_t);
	
	time_t stringToTime_t(const string&);

	/**
	 * @brief Performs a binary search for a specific timestamp in the log file.
	 * @param targetTimestamp The timestamp to search for.
	 * @return The position of the closest timestamp in the file.
	 */
	streampos binarySearchTimestamp(const time_t& targetTimestamp);

	~LogsFactory();

private:
	ifstream fileStream; 
	string filePath;     
	Logger& logger;      

	int compareTimestamps(time_t, time_t);

	void openFile();

	void closeFile();
};