from setuptools import setup, Extension
import pybind11
import os

from paths import VISUALIZATION_CPP, INNER, UTILITIES, INTERFACES, LOGGING, FILTERS, \
    FILTER_FACTORY_CPP, LOG_READER_CPP, I_LOG_FILTER_CPP, LOGS_FACTORY_CPP, PERFORMANCE_LOGGER_CPP, LOGGER_CPP, \
    VISUALIZATION_MODULES, FILTER_FACTORY_MODULE, LOGS_FACTORY_MODULE, DUSE_PYBIND, STD_20, STD_17

# Define base path for the C++ files
base_path = os.path.join(INNER, VISUALIZATION_CPP, VISUALIZATION_CPP)

# Update the file paths using base_path
filter_cpp_files = [
    os.path.join(base_path, FILTERS, FILTER_FACTORY_CPP),
    os.path.join(base_path, LOGGING, LOGS_FACTORY_CPP),
    os.path.join(base_path, LOGGING, LOG_READER_CPP),
    os.path.join(base_path, INTERFACES, I_LOG_FILTER_CPP),
    os.path.join(base_path, UTILITIES, PERFORMANCE_LOGGER_CPP),
    os.path.join(base_path, UTILITIES, LOGGER_CPP)
]

ext_modules = [
    Extension(
        LOGS_FACTORY_MODULE,
        [os.path.join(base_path, LOGGING, LOGS_FACTORY_CPP), os.path.join(base_path, UTILITIES, LOGGER_CPP)],
        include_dirs=[pybind11.get_include()],
        extra_compile_args=[STD_17, DUSE_PYBIND],
    ),
    Extension(
        FILTER_FACTORY_MODULE,
        filter_cpp_files,  # Use the updated list with base_path
        include_dirs=[pybind11.get_include()],
        extra_compile_args=[STD_20, DUSE_PYBIND],
    ),
]

setup(
    name=VISUALIZATION_MODULES,
    ext_modules=ext_modules,
)
