#pragma once
#include <string>
#include <iostream>
#include <unordered_map>
#include "../Models/Cluster.hpp"

namespace Config {
	enum class FilterType {
		TimeRange,
		Time,
		ThreadId,
		Cluster,
		Io,
		Quad,
		Unit,
		Area,
		Unknown
	};

	constexpr auto TIME = "Time";
	constexpr auto TIME_RANGE = "TimeRange";
	constexpr auto TID = "ThreadId";
	constexpr auto CLUSTER = "Cluster";
	constexpr auto IO = "Io";
	constexpr auto QUAD = "Quad";
	constexpr auto UNIT = "Unit";
	constexpr auto AREA = "Area";

	constexpr auto EXIT = "exit";
	constexpr auto YES = 'y';
	constexpr auto NO = 'n';

	static const std::unordered_map<std::string, FilterType> filterMap = {
	   { TIME_RANGE, FilterType::TimeRange },
	   { TIME, FilterType::Time },
	   { TID, FilterType::ThreadId },
	   { CLUSTER, FilterType::Cluster },
	   { IO, FilterType::Io },
	   { QUAD, FilterType::Quad },
	   { UNIT, FilterType::Unit },
	   { AREA, FilterType::Area },
	};
}

namespace std {
	template <>
	struct hash<Cluster> {
		size_t operator()(const Cluster& clusterId) const {
			size_t h1 = hash<int>{}(clusterId.die);
			size_t h2 = hash<int>{}(clusterId.quad);
			size_t h3 = hash<int>{}(clusterId.row);
			size_t h4 = hash<int>{}(clusterId.col);
			size_t h5 = hash<int>{}(clusterId.chip);
			return h1 ^ (h2 << 1) ^ (h3 << 2) ^ (h4 << 3) ^ (h5 << 4);
		}
	};

	template <>
	struct hash<tuple<int, int, int>> {
		size_t operator()(const tuple<int, int, int>& p) const {
			size_t h1 = hash<int>{}(get<0>(p));
			size_t h2 = hash<int>{}(get<1>(p));
			size_t h3 = hash<int>{}(get<2>(p));
			return h1 ^ (h2 << 1) ^ (h3 << 2);
		}
	};

	inline std::ostream& operator<<(std::ostream& os, const std::tuple<int, int, int>& quad) {
		os << "Chip: " << std::get<0>(quad) << ", Die: " << std::get<1>(quad) << ", Quad: " << std::get<2>(quad);
		return os;
	}
}
