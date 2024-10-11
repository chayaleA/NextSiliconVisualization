#pragma once
#include "../Logging/LogReader.hpp"
#include "../Utilities/Logger.hpp"
#include <string>

/**
 * @class ILogFilter
 * @brief Represents an abstract base class for filtering logs.
 *
 * This class is designed to provide an interface for filtering logs based on specific criteria.
 * It inherits from the IView class and contains a reference to a Logger instance for logging purposes.
 */
class ILogFilter : public IView {
public:
    ILogFilter(IViewPtr toFilter) : base(toFilter), logger(Logger::getInstance()) {}

    /**
     * @brief Abstract method to determine if a log should be taken based on the implemented criteria.
     *
     * @param log The log to evaluate.
     * @return true If the log meets the criteria.
     * @return false If the log does not meet the criteria.
     */
    virtual bool isToTake(const Log&) const = 0;

    /**
     * @brief Retrieves the next log that meets the filtering criteria.
     *
     * @return A generator of filtered logs.
     */
    Generator<Log> getNext() override;

    bool isOpen() override;

    void banan() {
        cout << "fdsfsd";
    }

protected:
    Logger& logger;

    IViewPtr base; 
};
