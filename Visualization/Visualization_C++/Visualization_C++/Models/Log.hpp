#pragma once
#include <ctime>
#include <string>
#include "Cluster.hpp"

/**
 * @class Log
 * @brief Represents a log entry in the system.
 *
 * This class contains the timestamp, cluster identifier, area, unit, I/O
 * operation, thread ID, and packet data for a log entry.
 */
class Log {
public:
    time_t timeStamp; 
    Cluster clusterId;
    string area;      
    string unit;      
    string io;        
    int tid;          
    string packet;    

    friend ostream& operator<<(ostream& lhs, const Log& rhs) {
        lhs << "timestamp:" << rhs.timeStamp << ", "
            << "cluster_id: " << rhs.clusterId << ", "
            << "area:" << rhs.area << ", "
            << "unit:" << rhs.unit << ", "
            << "in/out:" << rhs.io << ", "
            << "tid:" << rhs.tid << ", "
            << "packet/data:" << rhs.packet << std::endl;
        return lhs;
    }
};
