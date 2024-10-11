#include "LogsFactory.hpp"

void LogsFactory::setPath(const string& path) {
	this->filePath = path;
}

time_t LogsFactory::getFirstLogTime() {
	openFile();
	string line;
	fileStream.seekg(ios::beg);
	getline(fileStream, line);
	return getTimeFromLine(line);
}

time_t LogsFactory::getLastLogTime() {
	openFile();

	fileStream.seekg(-3, ios::end);
	char ch;
	string line;

	while (fileStream.tellg() > 1) {
		fileStream.get(ch);
		if (ch == '\n') {
			break;
		}
		fileStream.seekg(-2, std::ios::cur);
	}

	getline(fileStream, line);
	return getTimeFromLine(line);
}

time_t LogsFactory::getTimeFromLine(const string& line) {
	size_t pos = line.find("timestamp:");
	if (pos != string::npos) {
		size_t start = pos + 10;
		size_t end = line.find(',', start);

		if (end != string::npos) {
			string timestampStr = line.substr(start, end - start);
			try {
				return stringToTime_t(timestampStr);
			}
			catch (const std::invalid_argument& e) {
				throw InvalidFormatException("Invalid timestamp format: " + string(e.what()));
			}
			catch (const std::out_of_range& e) {
				throw InvalidFormatException("Timestamp value out of range: " + string(e.what()));
			}
		}
	}
	return -1;
}

string LogsFactory::time_tToString(time_t time) {
	struct tm* tm_info;
	tm_info = localtime(&time);
	char buffer[80];
	strftime(buffer, 80, "%d/%m/%Y %H:%M:%S", tm_info);
	return string(buffer);
}

time_t LogsFactory::stringToTime_t(const string& timestampStr) {
	try {
		double timestampDouble = stod(timestampStr); 
		return static_cast<time_t>(timestampDouble);  
	}
	catch (const std::invalid_argument& e) {
		throw InvalidFormatException ( "Invalid timestamp format:" + string(e.what()) );
		return -1;
	}
}

/**
 * @brief Performs a binary search for a specific timestamp in the log file.
 * @param targetTimestamp The timestamp to search for.
 * @return The position of the closest timestamp in the file.
 */
streampos LogsFactory::binarySearchTimestamp(const time_t& targetTimestamp) {
	openFile();
	streampos left = 0;
	fileStream.seekg(0, std::ios::end);
	streampos right = fileStream.tellg();
	streampos result = -1;
	streampos closestGreater = -1;

	while (left <= right) {
		streamoff mid = left + (streamoff)((right - left) / 2);
		fileStream.seekg(mid);

		if (mid > 0) {
			std::string dummy;
			getline(fileStream, dummy);
		}

		streampos currentPos = fileStream.tellg();
		std::string line;
		getline(fileStream, line);

		if (line.empty()) {
			break;
		}

		time_t midTimestamp = getTimeFromLine(line);

		if (compareTimestamps(midTimestamp, targetTimestamp) == 0) {
			result = currentPos;
			closeFile();
			return result;
		}
		else if (compareTimestamps(midTimestamp, targetTimestamp) > 0) {
			closestGreater = currentPos;
			right = mid - 1;
		}
		else {
			result = currentPos;
			left = mid + 1;
		}
	}
	closeFile();
	return (closestGreater != -1) ? closestGreater : result;
}

int LogsFactory::compareTimestamps(time_t ts1, time_t ts2) {
	return (ts1 > ts2) - (ts1 < ts2);
}

void LogsFactory::openFile() {
	if (!fileStream.is_open())
		fileStream.open(filePath);
	fileStream.seekg(0, ios::beg);
}

void LogsFactory::closeFile() {
	if (fileStream.is_open())
		fileStream.close();
}

LogsFactory::~LogsFactory() {
	fileStream.close();
}

/**
 * @brief Python module definition for LogsFactory.
 */
#ifdef USE_PYBIND
PYBIND11_MODULE(logs_factory, m) {
 m.doc() = "LogsFactory module: Provides functionality to read log timestamps from a file.";

 py::class_<LogsFactory>(m, "LogsFactory")
 .def(py::init<const std::string&>(), py::arg("path"), "Initialize LogsFactory with the given file path.")
 .def("get_first_log_time", &LogsFactory::getFirstLogTime, "Get the timestamp of the first log entry in the file.")
 .def("get_last_log_time", &LogsFactory::getLastLogTime, "Get the timestamp of the last log entry in the file.");
}
#endif