#ifndef FILTERPROCESSOR_H
#define FILTERPROCESSOR_H

#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include "../Filters/FilterFactory.hpp"
#include "../Utilities/CustomExceptions.hpp"

/**
 * @brief The FilterProcessor class processes filters on log data.
 *
 * This class reads log data from an input file, applies a set of filters,
 * and writes the filtered results to an output file. It also provides
 * functionality to display help for available filters.
 */
class FilterProcessor {
public:
    FilterProcessor(const std::string&, const std::vector<std::string>&, const std::string&);
    
    /**
    * @brief Processes the filters on the input log data.
    *
    * This function applies the specified filters and writes the filtered logs
    * to the output file.
    */
    void processFilters();

    /**
    * @brief Displays help for the available filters.
    *
    * This static function prints the expected formats for all available filters.
    */
    static void showFilterHelp();

private:
    Logger& logger;                   
    std::string inputFile;            
    std::vector<std::string> filters; 
    std::string outputFile;

    /**
    * @brief Applies filters to the provided FilterFactory.
    *
    * Parses and applies filters based on type (e.g., TimeRange, Cluster) to the given FilterFactory.
    * Throws exceptions for invalid formats or values.
    */
    void applyFilters(FilterFactory& filterFactory);

    static FilterType getFilterType(const string&);
};

#endif
