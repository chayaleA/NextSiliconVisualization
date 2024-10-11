#include "PerformanceLogger.hpp"

// Global vector for filter functions.
vector<string> filterFunctions;

/**
 * @brief Construct a new Performance Logger object.
 *
 * Initializes the output file. If the "Performance" directory does not exist,
 * it will be created. The start time is recorded upon construction.
 */
PerformanceLogger::PerformanceLogger() {
    const std::string directory = "Performance";
    const std::string filename = "run_metadata.txt";
    const std::string fullPath = directory + "/" + filename;

    if (!std::filesystem::exists(directory)) {
        std::filesystem::create_directory(directory);
    }

    if (std::filesystem::exists(fullPath)) {
        outputFile.open(fullPath, std::ios::app);
        if (!outputFile.is_open()) {
            throw FileOpenException("Error opening existing file for writing metadata.");
        }
    }

    else {
        outputFile.open(fullPath);
        if (!outputFile.is_open()) {
            throw FileCreatingException("Error creating new file for writing metadata.");
        }
    }

    start = std::chrono::high_resolution_clock::now();
}

/**
 * @brief Destroy the Performance Logger object.
 *
 * Records the end time, calculates the total duration of the performance
 * measurement, and logs the duration along with the filter functions to the
 * output file.
 */
PerformanceLogger::~PerformanceLogger() {
    end = high_resolution_clock::now();
    std::chrono::duration<double> duration = end - start;

    int totalSeconds = static_cast<int>(duration.count());
    int minutes = totalSeconds / 60;
    int seconds = totalSeconds % 60;

    if (outputFile.is_open()) {
        outputFile << "Date: ";
        time_t now = system_clock::to_time_t(system_clock::now());
        tm* ltm = localtime(&now);
        outputFile << ltm->tm_hour << ":" << ltm->tm_min << ":" << ltm->tm_sec;
        outputFile << " " << ltm->tm_mday << "/" << 1 + ltm->tm_mon << "/" << 1900 + ltm->tm_year << endl;

        if (minutes > 0) {
            outputFile << "Duration: " << minutes << " minutes and " << seconds << " seconds" << endl;
        }
        else {
            outputFile << "Duration: " << seconds << " seconds" << endl;
        }

        outputFile << "Filter Functions: " << endl;
        for (auto& function : filterFunctions) {
            outputFile << function << endl;
        }
        outputFile << "------------------------------------------" << endl;
        outputFile.close();
    }
    else {
        FileOpenException("Error writing metadata. File not open.");
    }
}
