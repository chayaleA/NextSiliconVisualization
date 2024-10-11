#pragma once
#include <iostream>

using namespace std;

/**
 * @class Cluster
 * @brief Represents a cluster of chips in a multi-chip architecture.
 *
 * This class encapsulates the properties of a cluster, including its location
 * within the chip architecture using various identifiers such as chip, die,
 * quad, row, and column.
 */
class Cluster {
public:
	int chip;
	int die; 
	int quad;
	int row; 
	int col; 

	Cluster(int chip, int die, int quad, int row, int col) : chip(chip), die(die), quad(quad), row(row), col(col) {}

	Cluster() {}

	bool operator==(const Cluster& other) const {
		return chip == other.chip && die == other.die && quad == other.quad && row == other.row && col == other.col;
	}

	friend ostream& operator<<(ostream& os, const Cluster& cluster) {
		os << "chip:" << cluster.chip << ", die:" << cluster.die << ", quad:" << cluster.quad
			<< ", row:" << cluster.row << ", col:" << cluster.col;
		return os;
	}

	Cluster& operator=(const Cluster& other) {
		if (this != &other) {
			chip = other.chip;
			die = other.die;
			quad = other.quad;
			row = other.row;
			col = other.col;
		}
		return *this;
	}
};
