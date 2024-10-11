#ifndef CLIHANDLER_H
#define CLIHANDLER_H

#include <iostream>
#include <fstream>
#include "CLI11.hpp"
#include "FilterProcessor.hpp"
#include "CountProcessor.hpp"

using namespace std;
using namespace CLI;

#define DEFAULT_INPUT_FILE "logs.csv"        
#define DEFAULT_OUTPUT_FILE "filtered_logs.csv"

/**
 * @brief Handles command-line interface interactions for filtering log files.
 *
 * This class manages command-line options, parses input arguments,
 * and executes the appropriate filtering or counting operations based on user input.
 */
class CLIHandler {
public:
	CLIHandler(int argc, char** argv);

	/**
	* @brief Executes the filtering or counting operations based on parsed options.
	*/
	void execute();

private:
	CLI::App app;                                 
	std::string inputFile = DEFAULT_INPUT_FILE;
	std::string outputFile = DEFAULT_OUTPUT_FILE;
	std::vector<std::string> filters;             
	bool countFlag = false;                       

	/**
	 * @brief Sets up command-line options for the CLI application.
	 *
	 * This method defines all available options and flags for the command-line application.
	 */
	void setupCLIOptions();
};

#endif
