#include "CountProcessor.hpp"

CountProcessor::CountProcessor(const std::string& inputFile) : inputFile(inputFile), logger(Logger::getInstance()) {
	logger.logMessageToFile("CountProcessor::CountProcessor - entering constructor");

	countMaps[TID] = [&]() { printCount(tidCount, TID, cout); };
	countMaps[UNIT] = [&]() { printCount(unitCount, UNIT, cout); };
	countMaps[AREA] = [&]() { printCount(areaCount, AREA, cout); };
	countMaps[CLUSTER] = [&]() { printCount(clusterCount, CLUSTER, cout); };
	countMaps[QUAD] = [&]() { printCount(quadCount, QUAD, cout); };
}

/**
 * @brief Initiates the counting process based on the input log file.
 *
 * Prompts the user for GPU processing preference based on file size,
 * then calls the appropriate counting method and writes results to a file.
 */
void CountProcessor::processCounts() {
	logger.logMessageToFile("CountProcessor::processCounts - entering default constructor");

	LogReader logReader(inputFile);
#ifdef USE_ONEAPI
	if (logReader.getFileSize() > MIN_FILE_SIZE) {
		char answer;
		std::cout << "This is very big file, Would you like to execute the counting process on the GPU? Please enter 'y' for Yes or 'n' for No." << std::endl;
		cin >> answer;

		while (answer != YES && answer != NO) {
			std::cout << "Invalid input! Enter: 'y' for Yes or 'n' for No." << std::endl;
			cin >> answer;
		}

		if (answer == YES)
			countWithGpu();
		else
			countByMultiThreading();
	}
	else
		countByMultiThreading();
#else
	countByMultiThreading();
#endif



	writeResultsToFile(DEFAULT_RESULT_FILE_NAME);

	string objectToDispaly;

	cout << "Everything is ready!" << std::endl << "What to dispaly ? Enter ThreadId / Unit / Area / Cluster / Quad: " << std::endl
		<< "To exit - enter exit" << std::endl;

	std::cin >> objectToDispaly;

	while (objectToDispaly != EXIT) {
		displayCountByName(objectToDispaly);

		cout << std::endl << "What to dispaly? Enter ThreadId/ Unit/ Area/ Cluster/ Quad: " << std::endl
			<< "To exit - enter exit" << std::endl;

		std::cin >> objectToDispaly;
	}

	logger.logMessageToFile("CountProcessor::processCounts - default constructor - Function execution finished.");
}

/**
 * @brief Initiates the log counting process using GPU acceleration.
 *
 * This function performs log processing and counting tasks utilizing GPU hardware for parallelization.
 * It provides enhanced performance for large datasets by leveraging the computational power of the GPU.
 */

#ifdef USE_ONEAPI
void CountProcessor::countWithGpu() {

	std::cout << "Starting counting process..." << std::endl;

	PerformanceLogger performanceLogger;

	GPULogReader gpuLogReader(inputFile);
	gpuLogReader.getNextInParallel(NUM_THREADS, tidCount, unitCount, areaCount, clusterCount, quadCount);
}
#endif

/**
 * @brief Initiates the log counting process using CPU multi-threading.
 *
 * This function performs log processing and counting tasks by distributing the workload across multiple CPU threads.
 * It provides parallel processing to improve performance on systems with multi-core processors.
 */
void CountProcessor::countByMultiThreading() {

	cout << "Starting counting process..." << std::endl;

	PerformanceLogger performanceLogger;

	MultithreadedLogReader multithreadedLogReader(inputFile);

	multithreadedLogReader.readAndCountFileByThreads(tidCount, areaCount, unitCount, clusterCount, quadCount);
}

void CountProcessor::writeResultsToFile(const std::string& outputFile) {
	std::ofstream outFile(outputFile);

	if (!outFile.is_open()) {
		throw FileOpenException("Error opening output file.");
		return;
	}

	printCount(tidCount, TID, outFile);
	outFile << "-----------------------------------------------------------------------------" << std::endl;

	printCount(unitCount, UNIT, outFile);
	outFile << "-----------------------------------------------------------------------------" << std::endl;

	printCount(areaCount, AREA, outFile);
	outFile << "-----------------------------------------------------------------------------" << std::endl;

	printCount(clusterCount, CLUSTER, outFile);
	outFile << "-----------------------------------------------------------------------------" << std::endl;

	printCount(quadCount, QUAD, outFile);
	outFile << "-----------------------------------------------------------------------------" << std::endl;
}

/**
 * @brief Prints the count for the specified counting map to the output stream.
 *
 * @tparam T The type of the keys in the counting map.
 * @param countMap The counting map to print.
 * @param name The name associated with the count (used in output).
 * @param outStream The output stream where the count will be printed.
 */
template<typename T>
void CountProcessor::printCount(const std::unordered_map<T, int>& countMap, const std::string& name, std::ostream& outStream) {
	outStream << "Total " << name << ": " << std::endl;
	for (const auto& [key, value] : countMap) {
		outStream << name << " - " << key << " : " << value << std::endl;
	}
}

/**
 * @brief Displays the count for the specified object type.
 *
 * @param objectToDisplay The name of the object type to display counts for.
 */
void CountProcessor::displayCountByName(const std::string& objectToDisplay) {
	auto it = countMaps.find(objectToDisplay);
	if (it != countMaps.end()) {
		it->second();
	}
	else
		throw invalid_argument("Invalid option.");
}
