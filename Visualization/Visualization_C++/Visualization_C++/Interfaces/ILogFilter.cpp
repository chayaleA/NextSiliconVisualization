#include "ILogFilter.hpp"

/**
 * @brief Retrieves the next log that meets the filtering criteria.
 *
 * This function yields logs from the base IView instance as long as it is open and
 * the logs meet the filtering criteria defined by the isToTake method.
 *
 * @return A generator of filtered logs.
 */
Generator<Log> ILogFilter::getNext() {
	while (base->isOpen())
		for (auto log : base->getNext())
			if (isToTake(log))
				co_yield log;
}

/**
 * @brief Checks if the filter is open for reading logs and logs the status.
 *
 * @return true If the base IView is open.
 * @return false If the base IView is closed.
 */
bool ILogFilter::isOpen() {
	bool isBaseOpen = base->isOpen();
	return isBaseOpen;
}