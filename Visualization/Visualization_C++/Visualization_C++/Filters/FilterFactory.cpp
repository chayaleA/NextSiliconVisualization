#include "FilterFactory.hpp"

Logger& logger = Logger::getInstance();

FilterFactory::FilterFactory(string logsFileName) :logger(Logger::getInstance()) {
	isFinish = false;
	chain = logReader = make_shared<LogReader>(logsFileName);
}

void FilterFactory::addFilterToChain(pair<FilterType, Variant> filter) {
	chain = createFilter(filter.first, filter.second);
	filtersData.push_back(filter);
}

void FilterFactory::updateFilterInChain(pair<FilterType, Variant> filter) {
	bool found = false;

	for (auto it = filtersData.begin(); it != filtersData.end(); it++) {
		if (static_cast<int>(it->first) == static_cast<int>(filter.first)) {
			found = true;
			*it = filter;
		}
	}

	if (!found) {
		chain = createFilter(filter.first, filter.second);
		filtersData.push_back(filter);
	}
	else {
		chain = logReader;
		for (auto it = filtersData.begin(); it != filtersData.end(); it++)
			chain = createFilter(it->first, it->second);
	}
}

Variant FilterFactory::getValueOfFilter(FilterType filterType) {
	for (const auto& it : filtersData) {
		if (it.first == filterType) {
			return it.second;
		}
	}

	throw std::runtime_error("FilterType not found.");
}

FilterType FilterFactory::stringToFilterType(string str) {
	auto it = filterMap.find(str);
	if (it != filterMap.end()) {
		return it->second;
	}

	return FilterType::Unknown;
}

void FilterFactory::setStartTime(time_t time) {
	logger.logMessageToFile("FilterFactory::setStartTime - Entering.");
	logReader->setStartTime(time);
}

void FilterFactory::setEndTime(time_t time) {
	logger.logMessageToFile("FilterFactory::setEndTime - Entering. ");
	logReader->setEndTime(time);
}

/**
 * @brief Get the next filtered log.
 * @return A generator yielding filtered logs.
 */
Generator<Log> FilterFactory::getFilteredLogs() {
	return chain->getNext();
}

/**
 * @brief Check if the log processing is finished.
 * @return true if the process is finished, false otherwise.
 */
bool FilterFactory::isFinishProcess() {
	return isFinish;
}

void FilterFactory::reset() {
	logReader->openFile();

	std::lock_guard<std::mutex> lock(logMutex);
	std::queue<Log> emptyQueue;
	std::swap(filteredLogs, emptyQueue);
}

/**
 * @brief Start processing logs by applying the filters asynchronously.
 */
void FilterFactory::startLogs() {
	reset();
	isFinish = false;
	if (filterThread.joinable()) {
		filterThread.join();
	}
	try {
		filterThread = std::thread([this]() {
			for (auto log : chain->getNext()) {
				if (log.timeStamp > 0 && log.timeStamp < 3025236764272) {
					{
						std::lock_guard<std::mutex> lock(logMutex);
						filteredLogs.push(log);
					}
					logCondition.notify_one();
				}
			}
			isFinish = true;
			});
	}
	catch (...) {
		throw ThreadCreationException("Thread creation failed.");
	}
}

/**
 * @brief Join the log processing thread.
 */
void FilterFactory::joinThread() {
	logger.logMessageToFile("FilterFactory::joinThread - Entering.");

	if (filterThread.joinable()) {
		filterThread.join();
		filterThread = std::thread();
	}

	logger.logMessageToFile("FilterFactory::joinThread - Function execution finished.");
}

Log FilterFactory::getLog() {
	std::lock_guard<std::mutex> lock(logMutex);
	if (!filteredLogs.empty()) {
		Log log = filteredLogs.front();
		filteredLogs.pop();
		return log;
	}
	throw runtime_error("FilterFactory::getLog - No logs available.");
}

bool FilterFactory::hasLog() {
	std::lock_guard<std::mutex> lock(logMutex);
	return !filteredLogs.empty();
}

void FilterFactory::removeFilter(FilterType filterToRemove) {
	chain = logReader;
	for (auto it = filtersData.begin(); it != filtersData.end();) {
		if (static_cast<int>(it->first) == static_cast<int>(filterToRemove))
			it = filtersData.erase(it);
		else {
			chain = createFilter(it->first, it->second);
			it++;
		}
	}
}

void FilterFactory::clearFilters() {
	logger.logMessageToFile("FilterFactory::clearFilters - Entering.");

	chain = logReader;
	filtersData.clear();
	filterFunctions.push_back("clear all filters");

	logger.logMessageToFile("FilterFactory::clearFilters - Function execution finished.");
}

IViewPtr FilterFactory::createFilter(FilterType type, Variant& value) {
	logger.logMessageToFile("FilterFactory::createFilter -  Entering.");

	switch (type) {
	case FilterType::ThreadId:
		if (holds_alternative<vector<int>>(value)) {
			return make_shared<ThreadIdFilter>(chain, get<vector<int>>(value));
		}
		else if (holds_alternative<pair<int, int>>(value)) {
			pair<int, int> pairValue = get<pair<int, int>>(value);
			vector<int> temp = { pairValue.first, pairValue.second };
			return make_shared<ThreadIdFilter>(chain, temp);
		}
		else if (holds_alternative<int>(value)) {
			return make_shared<ThreadIdFilter>(chain, get<int>(value));
		}
		break;
	case FilterType::Cluster:
		return make_shared<ClusterIdFilter>(chain, get<Cluster>(value));
	case FilterType::Io:
		return make_shared<IOFilter>(chain, get<string>(value));
	case FilterType::Quad:
	{
		if (holds_alternative<tuple<int, int, int>>(value))
			return make_shared<QuadFilter>(chain, get<tuple<int, int, int>>(value));
		else {
			vector<int> vec = get<vector<int>>(value);
			if (vec.size() == 3) {
				return make_shared<QuadFilter>(chain, make_tuple(vec[0], vec[1], vec[2]));
			}
			throw invalid_argument("Vector size for Quad must be 3.");
		}
	}
	case FilterType::Unit:
		return make_shared<UnitFilter>(chain, get<string>(value));
	case FilterType::Area:
		return make_shared<AreaFilter>(chain, get<string>(value));
	}

	logger.logMessageToFile("FilterFactory::createFilter -  Function execution finished.");
	return chain;
}

FilterFactory::~FilterFactory() {
	logger.logMessageToFile("FilterFactory::~FilterFactory -  Entering.");

	if (filterThread.joinable()) {
		filterThread.join();
	}

	logger.logMessageToFile("FilterFactory::~FilterFactory -  Function execution finished.");
}

#ifdef USE_PYBIND
PYBIND11_MODULE(filter_factory_module, m) {
	m.doc() = "FilterFactory module: Provides functionality to apply filters to logs.";

	py::class_<Log>(m, "Log")
		.def(py::init<>())
		.def_readwrite("timeStamp", &Log::timeStamp)
		.def_readwrite("clusterId", &Log::clusterId)
		.def_readwrite("area", &Log::area)
		.def_readwrite("unit", &Log::unit)
		.def_readwrite("io", &Log::io)
		.def_readwrite("tid", &Log::tid)
		.def_readwrite("packet", &Log::packet);

	py::class_<Cluster>(m, "Cluster")
		.def(py::init<int, int, int, int, int>())
		.def(py::init<>())
		.def_readwrite("chip", &Cluster::chip)
		.def_readwrite("die", &Cluster::die)
		.def_readwrite("quad", &Cluster::quad)
		.def_readwrite("row", &Cluster::row)
		.def_readwrite("col", &Cluster::col)
		.def("__eq__", &Cluster::operator==)
		.def("__repr__", [](const Cluster& c) {
		return "<Cluster chip:" + std::to_string(c.chip) + ", die:" + std::to_string(c.die) +
			", quad:" + std::to_string(c.quad) + ", row:" + std::to_string(c.row) +
			", col:" + std::to_string(c.col) + ">";
			})
		.def("__hash__", [](const Cluster& c) {
		std::hash<Cluster> hasher;
		return hasher(c);
			});


	py::enum_<FilterType>(m, "FilterType")
		.value("Time", FilterType::Time, "Filter based on a specific timestamp.")
		.value("ThreadId", FilterType::ThreadId, "Filter based on thread identifier.")
		.value("Cluster", FilterType::Cluster, "Filter based on cluster identifier.")
		.value("TimeRange", FilterType::TimeRange, "Filter based on a range of timestamps.")
		.value("Io", FilterType::Io, "Filter based on IO type.")
		.value("Quad", FilterType::Quad, "Filter based on quadrant identifier.")
		.value("Unit", FilterType::Unit, "Filter based on unit identifier.")
		.value("Area", FilterType::Area, "Filter based on area identifier.");

	py::class_<FilterFactory>(m, "FilterFactory")
		.def(py::init<std::string>(), py::arg("logsFileName"), "Initialize FilterFactory with the given log file name.")
		.def("add_filter_to_chain", [](FilterFactory& self, std::pair<FilterType, Variant> filter) {
		self.addFilterToChain(filter);
			}, py::arg("filter"), "Add a new filter to the chain. The filter is a pair of FilterType and Variant.")
		.def("add_filter_to_chain", [](FilterFactory& self, std::pair<std::string, Variant> filter) {
		FilterType filterType = self.stringToFilterType(filter.first);
		self.addFilterToChain(std::make_pair(filterType, filter.second));
			}, py::arg("filter"), "Add a new filter to the chain. The filter is a pair of string (converted to FilterType) and Variant.")
		.def("update_filter_in_chain", [](FilterFactory& self, std::pair<FilterType, Variant> filter) {
		self.updateFilterInChain(filter);
			}, py::arg("filter"), "Update an existing filter in the chain. If the filter doesn't exist, it will be added.")
		.def("update_filter_in_chain", [](FilterFactory& self, std::pair<std::string, Variant> filter) {
		FilterType filterType = self.stringToFilterType(filter.first);
		self.updateFilterInChain(std::make_pair(filterType, filter.second));
			}, py::arg("filter"), "Update an existing filter in the chain using a string. If the filter doesn't exist, it will be added.")
		.def("get_value_of_filter", [](FilterFactory& self, FilterType filterType) {
		return self.getValueOfFilter(filterType);
			}, py::arg("filter_type"), "Get the value of the filter by its FilterType.")
		.def("get_value_of_filter", [](FilterFactory& self, const std::string& filterTypeStr) {
		FilterType filterType = self.stringToFilterType(filterTypeStr);
		return self.getValueOfFilter(filterType);
			}, py::arg("filter_type"), "Get the value of the filter by its string representation (converted to FilterType).")
		.def("set_end_time", py::overload_cast<time_t>(&FilterFactory::setEndTime), py::arg("time"), "Set the end time for filtering logs.")
		.def("set_start_time", py::overload_cast<time_t>(&FilterFactory::setStartTime), py::arg("time"), "Set the start time for filtering logs.")
		.def("remove_filter", &FilterFactory::removeFilter, py::arg("filterToRemove"), "Remove a specific filter from the chain. The filter to remove is specified as a pair of FilterType and Variant.")
		.def("remove_filter", [](FilterFactory& self, const std::string& filterToRemove) {
		FilterType filterType = self.stringToFilterType(filterToRemove);
		self.removeFilter(filterType);
			}, py::arg("filterToRemove"), "Remove a specific filter from the chain using a string.")
		.def("clear_filters", &FilterFactory::clearFilters, "Clear all filters and reset the filter chain to the initial state.")
		.def("start_logs", &FilterFactory::startLogs, "Apply filters and generate the filtered logs asynchronously.")
		.def("get_log", &FilterFactory::getLog, "Get the next filtered log.")
		.def("has_log", &FilterFactory::hasLog, "Check if there are more filtered logs.")
		.def("is_finished_process", &FilterFactory::isFinishProcess, "Check if the process has finished")
		.def("join_thread", &FilterFactory::joinThread, "Join the logs thread after filtering has completed.");
}

#endif
