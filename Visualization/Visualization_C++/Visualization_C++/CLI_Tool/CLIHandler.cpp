#include "CLIHandler.hpp"

CLIHandler::CLIHandler(int argc, char** argv) : app("filter a huge log file", "filter") {
	setupCLIOptions();
	try {
		app.parse(argc, argv);
	}
	catch (const CLI::ParseError& e) {
		app.exit(e);
	}
}

/**
 * @brief Sets up command-line options for the CLI application.
 *
 * This method defines the options and flags that the user can specify
 * when running the command-line application.
 */
void CLIHandler::setupCLIOptions() {
	app.add_option("-i,--input", inputFile, "Input log file")->required();
	app.add_option("-o,--output", outputFile, "Name of output filtered log file");
	app.add_option("-f,--filter", filters, "Filter criteria (format: type=value)");
	app.add_flag("-c,--processCounts", countFlag, "Count specific categories (TID, UNIT, AREA, CLUSTER, QUAD)");
	app.add_flag_callback("--help-filters", FilterProcessor::showFilterHelp, "Show help for filter formats");
}

/**
 * @brief Executes filtering or counting operations based on command-line options.
 *
 * If the countFlag is set, it processes counts using CountProcessor.
 * If filters are provided, it processes them using FilterProcessor.
 */
void CLIHandler::execute() {
	if (app.get_option("--help")->count() || app.get_option("--help-filters")->count())
		return; // Exit if help options are requested.

	if (countFlag) {
		CountProcessor countProcessor(inputFile);
		countProcessor.processCounts(); // Process counts if countFlag is set.
		return;
	}

	FilterProcessor filterProcessor(inputFile, filters, outputFile);
	filterProcessor.processFilters(); // Process filters if countFlag is not set.
}