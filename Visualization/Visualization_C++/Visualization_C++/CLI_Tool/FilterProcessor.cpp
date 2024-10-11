#include "FilterProcessor.hpp"

FilterProcessor::FilterProcessor(const std::string& inputFile, const std::vector<std::string>& filters, const std::string& outputFile)
	: inputFile(inputFile), filters(filters), outputFile(outputFile), logger(Logger::getInstance()) {}

/**
 * @brief Processes the filters on the input log data.
 *
 * This function logs the start of the filtering process, applies the filters
 * using the FilterFactory, and writes the filtered logs to the output file.
 */
void FilterProcessor::processFilters() {
	logger.logMessageToFile("FilterProcessor::processFilters - entering");

	FilterFactory filterFactory(inputFile);
	applyFilters(filterFactory);

	std::ofstream outFile(outputFile);
	if (!outFile) {
		throw FileOpenException("opening output file : " + outputFile);
		return;
	}

	std::cout << "Starting to write filtered logs..." << std::endl;
	int logCount = 0;

	for (auto log : filterFactory.getFilteredLogs()) {
		if (log.timeStamp > 0) {
			outFile << log;
			logCount++;
		}
	}

	cout << "Total logs written: " << logCount << std::endl;

	outFile.close();

	cout << "Filtering complete. Results saved to " << outputFile << std::endl;

	logger.logMessageToFile("FilterProcessor::processFilters - entering");
}

/**
* @brief Applies filters to the provided FilterFactory.
*
* Parses and applies filters based on type (e.g., TimeRange, Cluster) to the given FilterFactory.
* Throws exceptions for invalid formats or values.
*/
void FilterProcessor::applyFilters(FilterFactory& filterFactory) {
	for (const auto& filter : filters) {
		size_t pos = filter.find('=');
		if (pos != string::npos) {
			string type = filter.substr(0, pos);
			string value = filter.substr(pos + 1);

			FilterType filterType = getFilterType(type);

			switch (filterType) {
			case FilterType::TimeRange: {
				size_t commaPos = value.find(',');
				if (commaPos != string::npos) {
					string startTimeStr = value.substr(0, commaPos);
					string endTimeStr = value.substr(commaPos + 1);

					try {
						double startTimeDouble = stod(startTimeStr);
						double endTimeDouble = stod(endTimeStr);

						time_t startTime = static_cast<time_t>(startTimeDouble);
						time_t endTime = static_cast<time_t>(endTimeDouble);

						filterFactory.setStartTime(startTime);
						filterFactory.setEndTime(endTime);
					}
					catch (const std::invalid_argument& e) {
						throw InvalidFormatException("Invalid TimeRange format. Could not parse time as a number.");
					}
					catch (const std::out_of_range& e) {
						throw invalid_argument( "Time value out of range.");
					}
				}
				else {
					throw InvalidFormatException("Invalid TimeRange format. Expected 'TimeRange=start,end'");
				}
				break;
			}
			case FilterType::Time: {
				try {
					double timestampDouble = stod(value);

					time_t timestamp = static_cast<time_t>(timestampDouble);

					filterFactory.setStartTime(timestamp);
					filterFactory.setEndTime(timestamp);
				}
				catch (const std::invalid_argument& e) {
					throw InvalidFormatException("Invalid Time format. Could not parse time as a number.");
				}
				catch (const std::out_of_range& e) {
					throw invalid_argument("Time value out of range.");
				}
				break;
			}
			case FilterType::Cluster: {
				auto extractValue = [](const string& str) -> int {
					size_t colonPos = str.find(':');
					if (colonPos != string::npos) {
						return stoi(str.substr(colonPos + 1));
					}
					throw invalid_argument("Invalid format");
					};

				try {
					vector<string> parts;
					stringstream ss(value);
					string part;
					while (getline(ss, part, ',')) {
						parts.push_back(part);
					}

					if (parts.size() != 5) {
						throw invalid_argument("Invalid number of parameters");
					}
					int chip = extractValue(parts[0]);
					int die = extractValue(parts[1]);
					int quad = extractValue(parts[2]);
					int row = extractValue(parts[3]);
					int col = extractValue(parts[4]);

					filterFactory.addFilterToChain({ filterType, Cluster(chip, die, quad, row, col) });
				}
				catch (const std::exception& e) {
					throw InvalidFormatException("Invalid Cluster format. Expected 'Cluster=chip:<value>,die:<value>,quad:<value>,row:<value>,col:<value>'. Error: " + string(e.what()) );
				}
				break;
			}
			case FilterType::Io:
			case FilterType::Unit:
			case FilterType::Area:
				filterFactory.addFilterToChain({ filterType, value });
				break;
			case FilterType::Quad: {
				auto extractValue = [](const string& str) -> int {
					size_t colonPos = str.find(':');
					if (colonPos != string::npos) {
						return stoi(str.substr(colonPos + 1));
					}
					throw invalid_argument("Invalid format");
					};

				try {
					vector<string> parts;
					stringstream ss(value);
					string part;
					while (getline(ss, part, ',')) {
						parts.push_back(part);
					}

					if (parts.size() != 3) {
						throw InvalidParameterCountException("Invalid number of parameters");
					}

					int chip = extractValue(parts[0]);
					int die = extractValue(parts[1]);
					int quad = extractValue(parts[2]);

					filterFactory.addFilterToChain({ filterType, make_tuple(chip, die, quad) });
				}
				catch (const std::exception& e) {
					throw InvalidFormatException("Invalid Quad format. Expected 'Quad=Chip:<value>,Die:<value>,Quad:<value>'. Error: "+ string(e.what()));
				}
				break;
			}
			case FilterType::ThreadId: {
				try {
					vector<int> tids;
					stringstream ss(value);
					string tid;
					while (getline(ss, tid, ',')) {
						tids.push_back(stoi(tid));
					}
					if (!tids.empty()) {
						filterFactory.addFilterToChain({ filterType, tids });
					}
				}
				catch (const std::exception& e) {
					throw InvalidFormatException( "Invalid ThreadId format. Expected 'ThreadId=value1,value2,...'. Error: " + string(e.what()) );
				}
				break;
			}
			default:
				throw invalid_argument( "Unknown filter type: " + type );
				break;
			}
		}
	}
}

/**
 * @brief Displays help for the available filters.
 *
 * This static function prints the expected formats for all available filters.
 */
void FilterProcessor::showFilterHelp() {
	cout << "Available filters and their expected formats:\n"
		<< "  TimeRange: TimeRange=start,end (e.g., ""TimeRange = 1726671491.525302, 1726671531.525302"")\n"
		<< "  Time: Time=value (e.g., Time=1723972947.9661083)\n"
		<< "  Quad: Quad=Chip:<value>,Die:<value>,Quad:<value> (e.g., Quad=Chip:0,Die:1,Quad:2)\n"
		<< "  ThreadId: ThreadId=value1,value2,... (e.g., ThreadId=7,10,15)\n"
		<< "  Unit: Unit=value (e.g., Unit=iqr)\n"
		<< "  Area: Area=value (e.g., Area=bmt)\n"
		<< "  Cluster: Cluster=chip:<value>,die:<value>,quad:<value>,row:<value>,col:<value> (e.g., Cluster=chip:0,die:1,quad:2,row:3,col:-1)\n"
		<< std::endl;
}

FilterType FilterProcessor::getFilterType(const string& type) {
	auto it = filterMap.find(type);
	if (it != filterMap.end()) {
		return it->second;
	}

	return FilterType::Unknown;
}