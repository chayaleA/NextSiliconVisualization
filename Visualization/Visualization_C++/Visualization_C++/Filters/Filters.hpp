#pragma once
#include "../Interfaces/ILogFilter.hpp"
#include "../Utilities/PerformanceLogger.hpp"
#include <ctime>

/**
 * @class ThreadIdFilter
 * @brief Filters logs based on specified thread IDs.
 *
 * This filter allows the user to specify a set of thread IDs, and only logs
 * from these threads will be accepted.
 */
class ThreadIdFilter : public ILogFilter {
private:
	vector<int> threadIds;

	/**
	 * @brief Adds a vector of thread IDs to the filter.
	 *
	 * @param vec A vector of thread IDs to add.
	 */
	void addThreadIds(const std::vector<int>& threadIdsVector) {
		logger.logMessageToFile("ThreadIdFilter::addThreadIds");
		threadIds.insert(threadIds.end(), threadIdsVector.begin(), threadIdsVector.end());
	}

	/**
	 * @brief Adds a single thread ID to the filter.
	 *
	 * @param tid The thread ID to add.
	 */
	void addThreadId(int tid) {
		logger.logMessageToFile("ThreadIdFilter::addThreadId");
		threadIds.push_back(tid);
	}

public:
	/**
	 * @brief Constructs a ThreadIdFilter with specified thread IDs.
	 *
	 * Supports both a vector of thread IDs and a single thread ID.
	 *
	 * @tparam T The type of the thread ID(s) being passed.
	 * @param toFilter The IViewPtr object to filter logs from.
	 * @param arg The thread ID(s) to filter.
	 */
	template<typename T>
	ThreadIdFilter(IViewPtr toFilter, T arg)
		: ILogFilter(toFilter) {
		logger.logMessageToFile("ThreadIdFilter::ThreadIdFilter");

		if constexpr (is_same_v<T, vector<int>>) {
			addThreadIds(arg);
		}
		else if constexpr (is_same_v<T, int>) {
			addThreadId(arg);
		}

		if (threadIds.size() == 1) {
			filterFunctions.push_back("ThreadIdFilter: " + to_string(threadIds[0]));
		}
		else {
			std::ostringstream chosenTIDs;
			chosenTIDs << "ThreadIdFilter: multiple THREADIDs - ";
			for (size_t i = 0; i < threadIds.size(); ++i) {
				chosenTIDs << threadIds[i];
				if (i < threadIds.size() - 1)
					chosenTIDs << ", ";
			}
			filterFunctions.push_back(chosenTIDs.str());
		}
	}

	bool isToTake(const Log& log) const override {
		return find(threadIds.begin(), threadIds.end(), log.tid) != threadIds.end();
	}
};

/**
 * @class IOFilter
 * @brief Filters logs based on specified I/O operations.
 *
 * This filter allows the user to specify an I/O operation, and only logs
 * related to this operation will be accepted.
 */
class IOFilter : public ILogFilter {
private:
	string _io;

public:
	IOFilter(IViewPtr toFilter, const string& io) : ILogFilter(toFilter), _io(io) {
		logger.logMessageToFile("IOFilter::IOFilter");
		filterFunctions.push_back("IOFilter: " + _io);
	}

	bool isToTake(const Log& log) const override {
		return log.io == _io;
	}
};

/**
 * @class QuadFilter
 * @brief Filters logs based on specified quad identifiers.
 *
 * This filter allows the user to specify a chip, die, and quad, and only
 * logs from this specific quad will be accepted.
 */
class QuadFilter : public ILogFilter {
private:
	tuple<int, int, int> _quad;

public:
	QuadFilter(IViewPtr toFilter, tuple<int, int, int> quad) : ILogFilter(toFilter), _quad(quad) {
		filterFunctions.push_back("QuadFilter: " + to_string(get<2>(_quad)) +
			" in die: " + to_string(get<1>(_quad)) +
			" in chip: " + to_string(get<0>(_quad)));
	}

	bool isToTake(const Log& log) const override {
		return log.clusterId.chip == get<0>(_quad) &&
			log.clusterId.die == get<1>(_quad) &&
			log.clusterId.quad == get<2>(_quad);
	}
};

/**
 * @class UnitFilter
 * @brief Filters logs based on specified unit identifiers.
 *
 * This filter allows the user to specify a unit, and only logs related to
 * this unit will be accepted.
 */
class UnitFilter : public ILogFilter {
private:
	string _unit;

public:
	UnitFilter(IViewPtr toFilter, const string& unit) : ILogFilter(toFilter), _unit(unit) {
		filterFunctions.push_back("UnitFilter: " + _unit);
	}

	bool isToTake(const Log& log) const override {
		return log.unit == _unit;
	}
};

/**
 * @class ClusterIdFilter
 * @brief Filters logs based on specified cluster identifiers.
 *
 * This filter allows the user to specify a cluster, and only logs from this
 * specific cluster will be accepted.
 */
class ClusterIdFilter : public ILogFilter {
private:
	Cluster clusterId;

public:
	ClusterIdFilter(IViewPtr toFilter, const Cluster& cid) : ILogFilter(toFilter), clusterId(cid) {
		stringstream ss;
		ss << cid;
		filterFunctions.push_back("ClusterIdFilter: " + ss.str());
	}

	bool isToTake(const Log& log) const override {
		return log.clusterId == clusterId;
	}
};

/**
 * @class AreaFilter
 * @brief Filters logs based on specified area identifiers.
 *
 * This filter allows the user to specify an area, and only logs related to
 * this area will be accepted.
 */
class AreaFilter : public ILogFilter {
private:
	string _area;

public:
	AreaFilter(IViewPtr toFilter, const string& area) : ILogFilter(toFilter), _area(area) {
		filterFunctions.push_back("AreaFilter: " + _area);
	}

	bool isToTake(const Log& log) const override {
		return log.area == _area;
	}
};
