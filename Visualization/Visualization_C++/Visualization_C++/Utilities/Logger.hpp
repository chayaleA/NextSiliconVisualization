#ifndef LOGGER_H
#define LOGGER_H

#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <chrono>
#include <ctime>
#include "../Utilities/CustomExceptions.hpp"

/**
 * @class Logger
 * @brief A singleton class for logging messages to files and the console.
 *
 * The Logger class provides methods to log messages, errors, and warnings
 * both to a log file and to the console. It manages log file rotation
 * when the log file size exceeds a specified limit.
 */
class Logger {
public:
    /**
     * @brief Gets the instance of the Logger.
     * @return A reference to the Logger instance.
     */
    static Logger& getInstance();

    void logWarningToFile(const std::string& message, const std::vector<std::string>& params = {});

    void logErrorToFile(const std::string& message, const std::vector<std::string>& params = {});

    void logMessageToFile(const std::string& message, const std::vector<std::string>& params = {});

    void logMessageToConsole(const std::string& message, const std::vector<std::string>& params = {});

    void logErrorToConsole(const std::string& message, const std::vector<std::string>& params = {});

    void logWarningToConsole(const std::string& message, const std::vector<std::string>& params = {});

    /**
    * @brief Rotates the log files when the current log file exceeds the size limit.
    */
    void rotateLogFile();
private:

    Logger();

    ~Logger();

    /**
     * @brief Formats the log message with parameters.
     * @param message The message to format.
     * @param ss The stringstream to store the formatted message.
     * @param params Additional parameters to format the message.
     */
    void formatLogMessage(const std::string& message, std::stringstream& ss, const std::vector<std::string>& param = {});

    /**
     * @brief Formats the log message without parameters.
     * @param message The message to format.
     * @param ss The stringstream to store the formatted message.
     */
    void formatLogMessage(const std::string& message, std::stringstream& ss);

    /**
     * @brief Gets the current timestamp.
     * @return A string representing the current time in "YYYY-MM-DD HH:MM:SS" format.
     */
    std::string getCurrentTime();
    void logToFile(const std::string& message, const std::string& level, const std::vector<std::string>& params = {});
    void logToConsole(const std::string& message, const std::string& level, const std::vector<std::string>& params = {});


    std::string logDirectory;       ///< Directory where log files are stored.
    std::string logFilePath;        ///< Path to the current log file.
    std::string currentLogFileName; ///< Name of the current log file.
    int currentLogFileSize;         ///< Current size of the log file in bytes.
    int maxLogFileSize;             ///< Maximum size of the log file in bytes before rotation.
    int maxLogFiles;                ///< Maximum number of log files to retain.
};

#endif
