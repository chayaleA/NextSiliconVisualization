#pragma once
#include <vector>
#include <chrono>
#include <iomanip>
#include <unordered_map>
#include <queue>
#include "../Interfaces/IView.hpp"
#include "../Utilities/CustomExceptions.hpp"
#include "LogsFactory.hpp"

using namespace std;

/**
 * @class LogReader
 * @brief A concrete implementation of the IView interface for reading and parsing log data from a CSV file.
 *
 * This class is part of the Decorator design pattern, where both LogReader and various filter classes
 * inherit from the IView interface. Each class implements the getNext() method differently, allowing
 * the log reading process to be extended with filters or additional functionality.
 *
 * The purpose of LogReader is to manage the basic functionality of opening, reading, and parsing logs
 * from a file, while still allowing for further decoration (e.g., filtering) by other classes
 * in the chain.
 */
class LogReader : public IView {
public:
	LogReader(const string& path);

	/**
	* @brief Retrieves the next log entry from the file.
	* @return A generator yielding Log objects.
	*/
	Generator<Log> getNext() override;

	void setPath(const string&);

	void setStartTime(time_t);

	void setEndTime(time_t);

	time_t getStartTime();

	time_t getEndTime();

	size_t getFileSize();

	bool isOpen() override;

	void openFile();

	~LogReader();

protected:
	ifstream fileStream;    
	string filePath;        
	LogsFactory logsFactory;
	time_t startTime;       
	time_t endTime;         

	/**
	* @brief Parses a line from the CSV file and fills a Log object.
	* @param line The line from the file.
	* @param log The Log object to populate.
	* @return True if the line was successfully parsed, false otherwise.
	*/
	bool parseCSVLine(const string& line, Log& log);

	void closeFile();
};