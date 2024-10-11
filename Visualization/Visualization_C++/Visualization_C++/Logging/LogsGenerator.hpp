#pragma once
#include <chrono>
#include <fstream>
#include <iomanip>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>
#include "../Models/Cluster.hpp"

using namespace std;

vector<string> areas = {
    "Nfi", "cbu in mem0", "cbu in mem1", "cbu in lcip",
    "mcu gate 0", "mcu gate 1", "ecore req", "ecore rsp",
    "pcie", "host_if", "bmt", "d2d", "hbm"
};

vector<string> units = {
    "BMT", "pcie", "cbus inj", "cbus clt", "nfi inj",
    "nfi clt", "iraq", "eq", "hbm", "tcu", "iqr", "iqd",
    "bin", "lnb"
};

namespace LogsGenerator {
    /**
     * @brief Generates a log file with random log entries.
     *
     * This function creates a log file with the specified name, generating
     * 250,000 log entries. Each log entry contains a timestamp, cluster ID,
     * area, unit, direction (in/out), thread ID, and sample data.
     *
     * @param fileName The name of the file to which the logs will be written.
     * @throws std::runtime_error if the file cannot be opened.
     */
    void GenerateLogsFile(const string& fileName, int numLines) {
        ofstream file(fileName);

        if (!file.is_open()) {
            throw std::runtime_error("Failed to open file");
        }

        auto start = chrono::system_clock::now();
        auto startSec = chrono::duration_cast<chrono::duration<double>>(start.time_since_epoch()).count();

        for (int i = 0; i < numLines; i++) {
            double entryTime = startSec + i;

            Cluster cluster_id;
            cluster_id.row = rand() % 8;
            cluster_id.col = rand() % 8;
            cluster_id.quad = rand() % 4;
            cluster_id.die = rand() % 2;
            cluster_id.chip = 0;

            int indexInAreaArray = rand() % areas.size();
            string nameArea = areas[indexInAreaArray];

            int indexInUnitArray = rand() % units.size();
            string nameUnit = units[indexInUnitArray];

            string io = (rand() % 2 == 0) ? "in" : "out";
            int tid = rand() % 1000;
            string data = "sample data " + to_string(i);

            file << std::fixed << std::setprecision(6)
                << "timestamp:" << entryTime << ","
                << "cluster_id:chip:" << cluster_id.chip
                << ";die:" << cluster_id.die
                << ";quad:" << cluster_id.quad
                << ";row:" << cluster_id.row
                << ";col:" << cluster_id.col << ","
                << "area:" << nameArea << ","
                << "unit:" << nameUnit << ","
                << "in/out:" << io << ","
                << "tid:" << tid << ","
                << "packet/data:" << data << "\n";
        }

        file.close();
    }
};
