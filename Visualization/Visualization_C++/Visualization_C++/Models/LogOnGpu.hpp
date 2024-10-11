#pragma once

#include <ctime>
#include <string>

/**
 * @class LogOnGpu
 * @brief Represents a log entry that is stored on the GPU.
 *
 * This class holds information about a log entry including thread ID,
 * chip, die, quad, row, column, area, and unit.
 */
class LogOnGpu {
public:
    int tid;       
    int chip;      
    int die;       
    int quad;      
    int row;       
    int col;       
    char area[64]; 
    char unit[64]; 

    LogOnGpu() {
        memset(area, 0, sizeof(area));
        memset(unit, 0, sizeof(unit));
    }

    void setArea(const std::string& areaStr) {
        strncpy(area, areaStr.c_str(), sizeof(area) - 1);
    }

    void setUnit(const std::string& unitStr) {
        strncpy(unit, unitStr.c_str(), sizeof(unit) - 1);
    }
};
