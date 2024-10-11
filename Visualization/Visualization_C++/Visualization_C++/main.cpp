#ifndef USE_TESTS
#include "Logging/LogsGenerator.hpp"
#include "Utilities/PerformanceLogger.hpp"
#include "CLI_Tool/CLIHandler.hpp"
#include "Filters/FilterFactory.hpp"

#define NUM_LINES 250000

using namespace std;
using namespace LogsGenerator;

int main(int argc, char** argv)
{
	Logger& logger = Logger::getInstance();
	try
	{
		logger.logMessageToFile("main is starting");

		if (argc > 1) {
			logger.logMessageToConsole("Running CLI");
			logger.logMessageToFile("Running CLI");

			CLIHandler cliHandler(argc, argv);
			cliHandler.execute();
		}
		else {
			GenerateLogsFile("logs.csv", NUM_LINES);
		}
	}
	catch (std::exception e) {
		logger.logErrorToConsole(e.what());
		logger.logErrorToFile(e.what());
	}
	return 0;
}

#else

#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "Utilities/doctest.hpp"
#include "Filters/FilterFactory.hpp"
#include "Logging/LogsFactory.hpp"
#include <iostream>

using namespace std;

constexpr auto FILE_NAME = "tests_logs.csv";

void GenerateLogsFile() {
	ofstream file(FILE_NAME);

	if (!file.is_open())
		throw std::runtime_error("Failed to open file");

	file << "timestamp:1726671833.525302,cluster_id:chip:0;die:0;quad:0;row:1;col:1,area:mcu gate 1,unit:BMT,in/out:in,tid:117,packet/data:sample data 0\n"
		<< "timestamp:1726671845.525302,cluster_id:chip:0;die:1;quad:2;row:2;col:2,area:hbm,unit:lnb,in/out:out,tid:7,packet/data:sample data 1\n"
		<< "timestamp:1726671855.525302,cluster_id:chip:0;die:0;quad:3;row:3;col:3,area:host_if,unit:hbm,in/out:in,tid:5,packet/data:sample data 2\n"
		<< "timestamp:1726671865.525302,cluster_id:chip:0;die:1;quad:1;row:0;col:0,area:hbm,unit:lnb,in/out:in,tid:117,packet/data:sample data 3\n"
		<< "timestamp:1726671875.525302,cluster_id:chip:0;die:1;quad:0;row:1;col:1,area:host_if,unit:BMT,in/out:in,tid:7,packet/data:sample data 4\n"
		<< "timestamp:1726671885.525302,cluster_id:chip:0;die:1;quad:1;row:2;col:2,area:host_if,unit:hbm,in/out:in,tid:7,packet/data:sample data 5\n"
		<< "timestamp:1726671895.525302,cluster_id:chip:0;die:1;quad:2;row:3;col:3,area:hbm,unit:hbm,in/out:in,tid:117,packet/data:sample data 6\n"
		<< "timestamp:1726671905.525302,cluster_id:chip:0;die:0;quad:1;row:0;col:0,area:host_if,unit:hbm,in/out:in,tid:7,packet/data:sample data 7\n"
		<< "timestamp:1726671915.525302,cluster_id:chip:0;die:0;quad:3;row:1;col:1,area:host_if,unit:hbm,in/out:in,tid:117,packet/data:sample data 8\n"
		<< "timestamp:1726671925.525302,cluster_id:chip:0;die:0;quad:1;row:3;col:3,area:hbm,unit:BMT,in/out:in,tid:117,packet/data:sample data 9";

	file.close();
}

TEST_CASE("FilterFactory TimeRange Filter Test") {
    vector<Log> logs;
    GenerateLogsFile();
    FilterFactory filterFactory(FILE_NAME);
    filterFactory.setStartTime(1726671833.525302);
    filterFactory.setEndTime(1726671915.525302);

    int count = 0;

    filterFactory.startLogs();
    while (!filterFactory.isFinishProcess() || filterFactory.hasLog()) {
        if (filterFactory.hasLog()) {
            logs.push_back(filterFactory.getLog());
            count++;
        }
    }
    filterFactory.joinThread();

    CHECK(count == 9);
}

TEST_CASE("FilterFactory Cluster Filter Test") {
    vector<Log> logs;
    GenerateLogsFile();
    FilterFactory filterFactory(FILE_NAME);
    filterFactory.setStartTime(1726671833.525302);
    filterFactory.setEndTime(1726671915.525302);

    Cluster cluster_id(0, 0, 0, 1, 1);
    filterFactory.addFilterToChain({ FilterType::Cluster, cluster_id });

    int count = 0;

    filterFactory.startLogs();
    while (!filterFactory.isFinishProcess() || filterFactory.hasLog()) {
        if (filterFactory.hasLog()) {
            logs.push_back(filterFactory.getLog());
            count++;
        }
    }
    filterFactory.joinThread();

    CHECK(count == 1);
    for (const auto& log : logs)
        CHECK(log.clusterId == cluster_id);

    filterFactory.removeFilter(FilterType::Cluster);
    count = 0;

    filterFactory.startLogs();
    while (!filterFactory.isFinishProcess() || filterFactory.hasLog()) {
        if (filterFactory.hasLog()) {
            logs.push_back(filterFactory.getLog());
            count++;
        }
    }
    filterFactory.joinThread();

    CHECK(count == 9);
}

TEST_CASE("FilterFactory Quad Filter Test") {
    vector<Log> logs;
    GenerateLogsFile();
    FilterFactory filterFactory(FILE_NAME);
    filterFactory.setStartTime(1726671833.525302);
    filterFactory.setEndTime(1726671915.525302);

    filterFactory.addFilterToChain({ FilterType::Quad, std::make_tuple(0, 1, 1) });

    int count = 0;

    filterFactory.startLogs();
    while (!filterFactory.isFinishProcess() || filterFactory.hasLog()) {
        if (filterFactory.hasLog()) {
            logs.push_back(filterFactory.getLog());
            count++;
        }
    }
    filterFactory.joinThread();

    CHECK(count == 2);
    bool allLogsMatch = true;
    for (const auto& log : logs) {
        if (log.clusterId.chip != 0 || log.clusterId.die != 1 || log.clusterId.quad != 1) {
            allLogsMatch = false;
            break;
        }
    }
    CHECK(allLogsMatch);
}

TEST_CASE("FilterFactory Area Filter Test") {
    vector<Log> logs;
    GenerateLogsFile();
    FilterFactory filterFactory(FILE_NAME);
    filterFactory.setStartTime(1726671833.525302);
    filterFactory.setEndTime(1726671915.525302);

    filterFactory.addFilterToChain({ FilterType::Area, "host_if" });

    int count = 0;

    filterFactory.startLogs();
    while (!filterFactory.isFinishProcess() || filterFactory.hasLog()) {
        if (filterFactory.hasLog()) {
            logs.push_back(filterFactory.getLog());
            count++;
        }
    }
    filterFactory.joinThread();

    CHECK(count == 5);
    for (const auto& log : logs)
        CHECK(log.area == "host_if");
}

TEST_CASE("FilterFactory Unit Filter Test") {
    vector<Log> logs;
    GenerateLogsFile();
    FilterFactory filterFactory(FILE_NAME);
    filterFactory.setStartTime(1726671833.525302);
    filterFactory.setEndTime(1726671915.525302);

    filterFactory.addFilterToChain({ FilterType::Unit, "lnb" });

    int count = 0;

    filterFactory.startLogs();
    while (!filterFactory.isFinishProcess() || filterFactory.hasLog()) {
        if (filterFactory.hasLog()) {
            logs.push_back(filterFactory.getLog());
            count++;
        }
    }
    filterFactory.joinThread();

    CHECK(count == 2);
    for (const auto& log : logs)
        CHECK(log.unit == "lnb");
}

TEST_CASE("FilterFactory Io Filter Test") {
    vector<Log> logs;
    GenerateLogsFile();
    FilterFactory filterFactory(FILE_NAME);
    filterFactory.setStartTime(1726671833.525302);
    filterFactory.setEndTime(1726671915.525302);

    filterFactory.addFilterToChain({ FilterType::Io, "in" });

    int count = 0;

    filterFactory.startLogs();
    while (!filterFactory.isFinishProcess() || filterFactory.hasLog()) {
        if (filterFactory.hasLog()) {
            logs.push_back(filterFactory.getLog());
            count++;
        }
    }
    filterFactory.joinThread();

    CHECK(count == 8);
    for (const auto& log : logs)
        CHECK(log.io == "in");
}

TEST_CASE("FilterFactory ThreadId Filter Test") {
    vector<Log> logs;
    GenerateLogsFile();
    FilterFactory filterFactory(FILE_NAME);
    filterFactory.setStartTime(1726671833.525302);
    filterFactory.setEndTime(1726671915.525302);

    vector<int> threadIds = { 117 };
    filterFactory.addFilterToChain({ FilterType::ThreadId, threadIds });

    int count = 0;

    filterFactory.startLogs();
    while (!filterFactory.isFinishProcess() || filterFactory.hasLog()) {
        if (filterFactory.hasLog()) {
            logs.push_back(filterFactory.getLog());
            count++;
        }
    }
    filterFactory.joinThread();

    CHECK(count == 4);
    for (const auto& log : logs)
        CHECK(log.tid == 117);
}

TEST_CASE("LogsFactory tests") {
    LogsFactory logsFactory(FILE_NAME);

    CHECK(logsFactory.getFirstLogTime() == 1726671833);
    CHECK(logsFactory.getLastLogTime() == 1726671925);
}
#endif