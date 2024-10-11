#pragma once
#ifdef USE_PYBIND
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#endif
#include <queue>
#include <thread>
#include <mutex>
#include <chrono>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <condition_variable>
#include "../Utilities/Config.hpp"
#include "../Filters/Filters.hpp"
#include "../Utilities/Logger.hpp"
#include "../Utilities/CustomExceptions.hpp"

using namespace std;
using namespace Config;

#ifdef USE_PYBIND
namespace py = pybind11;
#endif

/**
 * @class FilterFactory
 * @brief A factory class for creating and managing a chain of filters applied to log data.
 */

class FilterFactory {
public:
	FilterFactory(string logsFileName);

	void addFilterToChain(pair<FilterType, Variant> filter);

	void updateFilterInChain(pair<FilterType, Variant> filter);

	Variant getValueOfFilter(FilterType filterType);

	FilterType stringToFilterType(string);

	void setStartTime(time_t);

	void setEndTime(time_t);

	/**
	 * @brief Start processing logs by applying the filters asynchronously.
	 */
	void startLogs();

	/**
	 * @brief Join the log processing thread.
	 */
	void joinThread();

	/**
	 * @brief Get the next filtered log.
	 * @return A generator yielding filtered logs.
	 */
	Generator<Log> getFilteredLogs();

	Log getLog();

	bool hasLog();

	/**
	 * @brief Check if the log processing is finished.
	 * @return true if the process is finished, false otherwise.
	 */
	bool isFinishProcess();

	void removeFilter(FilterType);

	void clearFilters();

	~FilterFactory();

private:
	Logger& logger;									

	IViewPtr chain;									
	shared_ptr<LogReader> logReader;			
	LogsFactory logsFactory;					
	bool isFinish;								

	std::queue<Log> filteredLogs;				
	std::thread filterThread;					

	std::mutex logMutex;						
	std::condition_variable logCondition;		

	vector<pair<FilterType, Variant>> filtersData; 

	IViewPtr createFilter(FilterType, Variant&);

	void reset();
};
