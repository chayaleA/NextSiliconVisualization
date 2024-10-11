#pragma once

#include <exception>
#include <string>
#include <stdexcept>

class FileOpenException : public std::exception {
public:
    FileOpenException(const std::string& message) : errorMessage(message) {}
    const char* what() const noexcept override {
        return errorMessage.c_str();
    }

private:
    std::string errorMessage;
};

class FileCreatingException : public std::exception {
public:
    FileCreatingException(const std::string& message) : errorMessage(message) {}
    const char* what() const noexcept override {
        return errorMessage.c_str();
    }

private:
    std::string errorMessage;
};

class FileNotFoundException : public std::exception {
public:
    FileNotFoundException(const std::string& message) : errorMessage(message) {}
    const char* what() const noexcept override {
        return errorMessage.c_str();
    }

private:
    std::string errorMessage;
};

class InvalidFormatException : public std::invalid_argument {
public:
    InvalidFormatException(const std::string& message) : std::invalid_argument(message) {}
};

class InvalidParameterCountException : public std::invalid_argument {
public:
    InvalidParameterCountException(const std::string& message) : std::invalid_argument(message) {}
};

class SYCLException : public std::exception {
public:
    SYCLException(const std::string& message) : errorMessage(message) {}

    const char* what() const noexcept override {
        return errorMessage.c_str();
    }

private:
    std::string errorMessage;
};

class ThreadCreationException : public std::exception {
public:
    ThreadCreationException(const std::string& message) : errorMessage(message) {}

    const char* what() const noexcept override {
        return errorMessage.c_str();
    }

private:
    std::string errorMessage;
};

class LogFileRotationException : public std::exception {
public:
    LogFileRotationException(const std::string& message) : message(message) {}

    const char* what() const noexcept override {
        return message.c_str();
    }

private:
    std::string message;
};