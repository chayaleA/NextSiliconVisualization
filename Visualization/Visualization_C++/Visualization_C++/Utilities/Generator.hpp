#include <coroutine>
#include <iostream>

/**
 * @class Generator
 * @brief A coroutine-based generator for producing a sequence of values.
 *
 * This class uses C++20 coroutines to generate values on demand.
 * It supports yielding values and iterating through them using an iterator.
 *
 * @tparam T The type of values produced by the generator.
 */
template<typename T>
class Generator {
public:
    struct promise_type;
    using handle_type = std::coroutine_handle<promise_type>;

    struct promise_type {
        T value;

        /**
         * @brief Creates the generator from the promise.
         *
         * @return A Generator object.
         */
        auto get_return_object() {
            return Generator{ handle_type::from_promise(*this) };
        }

        /**
         * @brief Defines the initial suspension point of the coroutine.
         *
         * @return A suspension point that always suspends.
         */
        auto initial_suspend() {
            return std::suspend_always{};
        }

        /**
         * @brief Defines the final suspension point of the coroutine.
         *
         * @return A suspension point that always suspends.
         */
        auto final_suspend() noexcept {
            return std::suspend_always{};
        }

        /**
         * @brief Yields a value from the generator.
         *
         * @param v The value to yield.
         * @return A suspension point that always suspends.
         */
        auto yield_value(T v) {
            value = v;
            return std::suspend_always{};
        }

        /**
         * @brief Finalizes the coroutine without a return value.
         */
        void return_void() {
        }

        /**
         * @brief Handles exceptions that are not caught within the coroutine.
         *
         * This function terminates the program if an unhandled exception occurs.
         */
        void unhandled_exception() {
            std::terminate();
        }
    };

    handle_type coro; ///< The coroutine handle.

    /**
     * @brief Constructs a Generator from a coroutine handle.
     *
     * @param h The coroutine handle.
     */
    Generator(handle_type h) : coro(h) {
    }

    /**
     * @brief Destroys the generator and cleans up the coroutine.
     */
    ~Generator() {
        if (coro && coro.done()) {
            coro.destroy();
            coro = nullptr;
        }
    }

    /**
     * @brief Checks if the generator has finished producing values.
     *
     * @return true if the generator is done; false otherwise.
     */
    bool done() const {
        return coro.done();
    }

    /**
     * @brief Resumes the coroutine and retrieves the next value.
     *
     * @return The next value produced by the generator.
     */
    T next() {
        coro.resume();
        return coro.promise().value;
    }

    struct iterator {
        handle_type coro; ///< The coroutine handle for the iterator.
        bool done; ///< Indicates if the iteration is complete.

        /**
         * @brief Constructs an iterator from a coroutine handle.
         *
         * @param h The coroutine handle.
         */
        iterator(handle_type h) : coro(h), done(!h || h.done()) {
        }

        /**
         * @brief Compares the iterator with the default sentinel.
         *
         * @param sentinel The default sentinel for comparison.
         * @return true if the iterator is not done; false otherwise.
         */
        bool operator!=(std::default_sentinel_t) const {
            return !done;
        }

        /**
         * @brief Advances the iterator to the next value.
         *
         * @return A reference to the iterator.
         */
        iterator& operator++() {
            coro.resume();
            done = coro.done();
            return *this;
        }

        /**
         * @brief Dereferences the iterator to retrieve the current value.
         *
         * @return The current value produced by the generator.
         */
        T operator*() const {
            return coro.promise().value;
        }
    };

    /**
     * @brief Returns an iterator to the beginning of the generated values.
     *
     * @return An iterator pointing to the first value.
     */
    iterator begin() {
        return iterator{ coro };
    }

    /**
     * @brief Returns a sentinel to mark the end of iteration.
     *
     * @return A default sentinel object.
     */
    std::default_sentinel_t end() {
        return {};
    }
};
