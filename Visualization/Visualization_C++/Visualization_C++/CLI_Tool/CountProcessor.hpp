#pragma once

#include <string>
#include <unordered_map>
#include <utility>
#include <iostream>
#include <thread>
#include <mutex>
#include "../Filters/FilterFactory.hpp"
#include "../Utilities/Logger.hpp"
#include "../Utilities/PerformanceLogger.hpp"
#include "../Utilities/CustomExceptions.hpp"
#include "MultithreadedLogReader.hpp"
#ifdef USE_ONEAPI
#include "GPULogReader.hpp"
#endif

#define NUM_THREADS 6               
#define MIN_FILE_SIZE 1000000        
#define DEFAULT_RESULT_FILE_NAME "result.txt"

using namespace std;

/**
 * @brief The CountProcessor class is responsible for processing counts from log data.
 *
 * This class reads log data from a specified input file, processes counts based on different criteria
 * (such as ThreadId, Unit, Area, Cluster, and Quad), and writes the results to an output file. It can
 * leverage GPU processing or multi-threading for performance improvements.
 */
class CountProcessor {
public:
	CountProcessor(const std::string& inputFile);

	/**
	 * @brief Initiates the counting process based on the input log file.
	 *
	 * This method checks the file size, prompts the user for GPU processing preference,
	 * and invokes the appropriate counting method.
	 */
	void processCounts();

private:
	Logger& logger;													 
	std::string inputFile;											 
																	 
	std::unordered_map<int, int> tidCount;							 
	std::unordered_map<std::string, int> unitCount;					 
	std::unordered_map<std::string, int> areaCount;					 
	std::unordered_map<Cluster, int> clusterCount;					 
	std::unordered_map<tuple<int, int, int>, int> quadCount;		 

	std::unordered_map<std::string, std::function<void()>> countMaps;

	/**
	* @brief Initiates the log counting process using GPU acceleration.
	*
	* This function performs log processing and counting tasks utilizing GPU hardware for parallelization.
	* It provides enhanced performance for large datasets by leveraging the computational power of the GPU.
	*/
#ifdef USE_ONEAPI
	void countWithGpu();
#endif
	/**
	 * @brief Initiates the log counting process using CPU multi-threading.
	 *
	 * This function performs log processing and counting tasks by distributing the workload across multiple CPU threads.
	 * It provides parallel processing to improve performance on systems with multi-core processors.
	 */
	void countByMultiThreading();

	void writeResultsToFile(const std::string&);

	/**
	 * @brief Prints the count for the specified counting map to the output stream.
	 *
	 * @tparam T The type of the keys in the counting map.
	 * @param countMap The counting map to print.
	 * @param name The name associated with the count (used in output).
	 * @param outStream The output stream where the count will be printed.
	 */
	template<typename T>
	void printCount(const std::unordered_map<T, int>& countMap, const std::string& name, std::ostream& outStream);

	/**
	 * @brief Displays the count for the specified object type.
	 *
	 * @param objectToDisplay The name of the object type to display counts for.
	 */
	void displayCountByName(const std::string& objectToDisplay);
};