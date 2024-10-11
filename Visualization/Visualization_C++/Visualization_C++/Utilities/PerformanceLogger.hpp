#pragma once

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <chrono>
#include <filesystem>
#include "../Utilities/CustomExceptions.hpp"

using namespace std;
using namespace std::chrono;

/**
 * @brief Global vector to hold filter function names.
 *
 * This vector can be used to store the names of various filter functions
 * for performance logging purposes.
 */
extern vector<string> filterFunctions;

/**
 * @brief A class for logging performance metrics.
 *
 * This class measures the duration of code execution and logs
 * the relevant metadata to a specified output file.
 */
class PerformanceLogger {
private:
	ofstream outputFile;                     
	high_resolution_clock::time_point start; 
	high_resolution_clock::time_point end;

public:
	/**
	* @brief Construct a new Performance Logger object.
	*
	* Initializes the output file and records the start time for performance logging.
	*/
	PerformanceLogger();

	/**
	* @brief Destroy the Performance Logger object.
	*
	* Records the end time, calculates the duration, and logs the performance
	* data to the output file upon destruction of the object.
	*/
	~PerformanceLogger();
};
