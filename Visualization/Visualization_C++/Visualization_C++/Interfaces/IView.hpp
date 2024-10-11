#pragma once
#include <vector>
#include <variant>
#include <tuple>
#include <utility>
#include "../Utilities/Generator.hpp"
#include "../Models/Log.hpp"

using namespace std;

/**
 * @typedef Variant
 * @brief A variant type that can hold multiple types of data.
 *
 * This variant can hold a string, double, int, Cluster, a pair of integers,
 * a vector of integers, or a tuple of three integers.
 */
using Variant = variant<string, double, int, Cluster, pair<int, int>, vector<int>, tuple<int, int, int>>;

/**
 * @interface IView
 * @brief An interface representing a view that can produce log entries.
 */
class IView {
public:
    /**
     * @brief Retrieves the next log entry from the view.
     *
     * @return A generator producing Log entries.
     */
    virtual Generator<Log> getNext() = 0;

    virtual bool isOpen() = 0;

    virtual ~IView() {}
};

typedef shared_ptr<IView> IViewPtr;
