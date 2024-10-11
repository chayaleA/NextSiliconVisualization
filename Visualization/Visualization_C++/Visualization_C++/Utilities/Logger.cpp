#include "Logger.hpp"
#include <filesystem>

Logger::Logger() {
    logDirectory = "log_files";
    if (!std::filesystem::exists(logDirectory)) {
        std::filesystem::create_directory(logDirectory);
    }

    // Get the current date and time to include in the log file name
    std::time_t now = std::time(nullptr);
    std::tm* localTime = std::localtime(&now);

    char dateTimeBuffer[80];
    std::strftime(dateTimeBuffer, 80, "%d.%m.%y.%H.%M", localTime);

    std::string currentDateTime(dateTimeBuffer);

    logFilePath = currentLogFileName = logDirectory + "/log_" + currentDateTime + ".log";
    currentLogFileSize = 0;
    maxLogFileSize = 4000;
    maxLogFiles = 3;
}

/**
 * @brief Gets the instance of the Logger.
 *
 * @return A reference to the Logger instance.
 */
Logger& Logger::getInstance() {
    static Logger loggerInstance;
    return loggerInstance;
}

void Logger::logToFile(const std::string& message, const std::string& level, const std::vector<std::string>& params) {
    std::ofstream file(logFilePath, std::ios_base::app);
    if (file.is_open()) {
        std::stringstream ss;
        ss << getCurrentTime() << " [" << level << "] ";
        formatLogMessage(message, ss, params);
        file << ss.str() << std::endl;
        currentLogFileSize += ss.str().size();

        if (currentLogFileSize >= maxLogFileSize) {
            rotateLogFile();
        }

        file.close();
    }
}

void Logger::logMessageToFile(const std::string& message, const std::vector<std::string>& params) {
    logToFile(message, "INFO", params);
}

void Logger::logErrorToFile(const std::string& message, const std::vector<std::string>& params) {
    logToFile(message, "ERROR", params);
}

void Logger::logWarningToFile(const std::string& message, const std::vector<std::string>& params) {
    logToFile(message, "WARNING", params);
}

void Logger::logToConsole(const std::string& message, const std::string& level, const std::vector<std::string>& params) {
    std::stringstream ss;
    ss << getCurrentTime() << " [" << level << "] ";
    formatLogMessage(message, ss, params);

    if (level == "ERROR") {
        std::cerr << ss.str() << std::endl;
    }
    else {
        std::cout << ss.str() << std::endl;
    }
}

void Logger::logMessageToConsole(const std::string& message, const std::vector<std::string>& params) {
        logToConsole(message, "INFO", params);
    }

void Logger::logErrorToConsole(const std::string& message, const std::vector<std::string>& params) {
        logToConsole(message, "ERROR", params);
    }

void Logger::logWarningToConsole(const std::string& message, const std::vector<std::string>& params) {
        logToConsole(message, "WARNING", params);
    }
/**
 * @brief Formats the log message with parameters.
 *
 * @param message The message to format.
 * @param ss The stringstream to store the formatted message.
 * @param params Additional parameters to format the message.
 */
void Logger::formatLogMessage(const std::string& message, std::stringstream& ss, const std::vector<std::string>& params) {
    ss << message;
    for (const auto& param : params) {
        ss << " " << param;
    }
}

/**
 * @brief Formats the log message without parameters.
 *
 * @param message The message to format.
 * @param ss The stringstream to store the formatted message.
 */
//void Logger::formatLogMessage(const std::string& message, std::stringstream& ss) {
 /*   ss << message;
}*/

/**
 * @brief Gets the current timestamp.
 *
 * @return A string representing the current time in "YYYY-MM-DD HH:MM:SS" format.
 */
std::string Logger::getCurrentTime() {
    auto now = std::chrono::system_clock::now();
    std::time_t now_c = std::chrono::system_clock::to_time_t(now);
    char buffer[20];
    std::strftime(buffer, 20, "%Y-%m-%d %H:%M:%S", std::localtime(&now_c));
    return std::string(buffer);
}

/**
 * @brief Rotates the log files when the current log file exceeds the size limit.
 */
void Logger::rotateLogFile() {
    currentLogFileSize = 0;

    std::string logFilePrefix = logDirectory + "/log_";
    std::string logFileExtension = ".log";

    std::time_t now = std::time(nullptr);
    std::tm* localTime = std::localtime(&now);

    char dateTimeBuffer[80];
    std::strftime(dateTimeBuffer, 80, "%d.%m.%y.%H.%M", localTime);

    std::string currentDateTime(dateTimeBuffer);

    std::filesystem::rename(logFilePath, logFilePrefix + currentDateTime + logFileExtension);

    for (int i = maxLogFiles - 1; i > 1; --i) {
        std::string currentFile = logFilePrefix + currentDateTime + logFileExtension;

        std::time_t previousTime = now - (60 * (maxLogFiles - i)); // Each file is named based on the time of creation
        std::tm* previousLocalTime = std::localtime(&previousTime);

        char previousDateTimeBuffer[80];
        std::strftime(previousDateTimeBuffer, 80, "%d.%m.%y.%H.%M", previousLocalTime);

        std::string previousDateTime(previousDateTimeBuffer);

        std::string nextFile = logFilePrefix + previousDateTime + logFileExtension;

        if (std::filesystem::exists(currentFile)) {
            std::error_code ec;
            std::filesystem::rename(currentFile, nextFile, ec);
            if (ec) {
                throw LogFileRotationException("Error rotating log file: " + ec.message());
            }
        }
    }

    std::error_code ec;
    std::filesystem::rename(logFilePrefix + currentDateTime + logFileExtension, logFilePath, ec);
    if (ec) {
        throw LogFileRotationException("Error rotating log file: " + ec.message());
    }
}

Logger::~Logger() {}