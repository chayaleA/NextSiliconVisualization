#include "LogReader.hpp"

LogReader::LogReader(const string& path) : filePath(path) {
	logsFactory.setPath(path);
	openFile();
	startTime = logsFactory.getFirstLogTime();
	endTime = logsFactory.getLastLogTime();
}

/**
 * @brief Retrieves the next log entry from the log file.
 * @return A generator yielding Log objects.
 */
Generator<Log> LogReader::getNext() {
	openFile();
	string line;
	Log log;
	time_t start;
	streampos position = logsFactory.binarySearchTimestamp(startTime);
	fileStream.seekg(position, ios::beg);

	getline(fileStream, line);
	start = logsFactory.getTimeFromLine(line);
	if (start != startTime && startTime == endTime)
		co_return;

	while (!line.empty() && start <= endTime) {
		if (parseCSVLine(line, log)) {
			co_yield log;
		}

		getline(fileStream, line);

		if (!fileStream)
			break;

		start = logsFactory.getTimeFromLine(line);

	}
	closeFile();
}

/**
 * @brief Parses a line from the CSV file and fills a Log object.
 * @param line The line from the file.
 * @param log The Log object to populate.
 * @return True if the line was successfully parsed, false otherwise.
 */
bool LogReader::parseCSVLine(const string& line, Log& log) {
	regex pattern(R"(timestamp:(\d+\.\d+)\s*,cluster_id:chip:(-?\d+);die:(-?\d+);quad:(-?\d+);row:(-?\d+);col:(-?\d+)\s*,area:(.*?),unit:(.*?),in/out:(in|out),tid:(\d+),packet/data:(.*))");
	smatch match;
	if (regex_match(line, match, pattern)) {
		try {
			double timestampDouble = stod(match[1]);
			log.timeStamp = static_cast<time_t>(timestampDouble);
		}
		catch (runtime_error e) {
			throw InvalidFormatException("Error parsing timestamp: " + string(e.what()));
			return false;
		}
		log.clusterId.chip = stoi(match[2]);
		log.clusterId.die = stoi(match[3]);
		log.clusterId.quad = stoi(match[4]);
		log.clusterId.row = stoi(match[5]);
		log.clusterId.col = stoi(match[6]);
		log.area = match[7];
		log.unit = match[8];
		log.io = match[9] == "in" ? "in" : "out";
		log.tid = stoi(match[10]);
		log.packet = match[11];
		return true;
	}
	return false;
}

void LogReader::setPath(const string& path) {
	filePath = path;
	logsFactory.setPath(path);
	openFile();
	startTime = logsFactory.getFirstLogTime();
	endTime = logsFactory.getLastLogTime();
}

void LogReader::setStartTime(time_t start) {
	startTime = start;
}

void LogReader::setEndTime(time_t end) {
	endTime = end;
}

time_t LogReader::getStartTime() {
	return startTime;
}

time_t LogReader::getEndTime() {
	return endTime;
}

size_t LogReader::getFileSize() {
	openFile();
	fileStream.seekg(0, ios::end);
	size_t fileSize = fileStream.tellg();
	closeFile();
	return fileSize;
}

bool LogReader::isOpen() {
	return fileStream.is_open();
}

void LogReader::openFile() {
	if (!isOpen())
		fileStream.open(filePath);
	fileStream.seekg(0, ios::beg);
}

void LogReader::closeFile() {
	if (isOpen())
		fileStream.close();
}

LogReader::~LogReader() {
	fileStream.close();
}