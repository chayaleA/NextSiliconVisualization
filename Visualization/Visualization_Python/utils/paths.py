# directories
IMAGES_DIR = "images"
STYLES_DIR = "styles"

# images
APP_ICON_IMAGE = f"{IMAGES_DIR}/app_icon.ico"
LOADING_ICON_IMAGE = f"{IMAGES_DIR}/loading_icon.gif"
LOADING_DATA_IMAGE = f"{IMAGES_DIR}/loading_data_image.png"
CLUSTERS_DISPLAY_IMAGE = f"{IMAGES_DIR}/clusters_display.png"
DIE_DISPLAY_IMAGE = f"{IMAGES_DIR}/die_display.png"
FILE_SELECTION_WINDOW_DISPLAY_IMAGE = f"{IMAGES_DIR}/file_selection_window_display.png"
FILTER_BY_CLUSTERID_WINDOW_DISPLAY_IMAGE = f"{IMAGES_DIR}/filter_by_clusterId_window_display.png"
FILTERS_MENU_DISPLAY_IMAGE = f"{IMAGES_DIR}/filters_menu_display.png"
FILTERS_SELECTED_IN_MENU_DISPLAY_IMAGE = f"{IMAGES_DIR}/filters_selected_in_menu_display.png"
HOST_INTERFACE_DISPLAY_IMAGE = f"{IMAGES_DIR}/host_interface_display.png"
INSTRUCTIONS_ICON_IMAGE = f"{IMAGES_DIR}/instructions_icon.png"
SEARCH_ICON_IMAGE = f"{IMAGES_DIR}/search_icon.png"

# data files
CHIP_DATA_JSON = "data/chip_data.json"
SL_JSON = "data/sl.json"
LOGS_CSV = "data/logs.csv"

# style files
INFO_WIDGET_CSS = f"{STYLES_DIR}/info_styles.css"
CLUSTER_INFO_WIDGET_CSS = f"{STYLES_DIR}/cluster_info_styles.css"
DIALOG_FILTAR_CSS = f"{STYLES_DIR}/dialog_styles.css"

# c++ directories
INNER = ".."
VISUALIZATION_CPP = "Visualization_C++"
FILTERS = "Filters"
LOGGING = "Logging"
INTERFACES = "Interfaces"
UTILITIES = "Utilities"

# c++ files
LOGGER_CPP = "Logger.cpp"
PERFORMANCE_LOGGER_CPP = "PerformanceLogger.cpp"
I_LOG_FILTER_CPP = "ILogFilter.cpp"
LOG_READER_CPP = "LogReader.cpp"
LOGS_FACTORY_CPP = "LogsFactory.cpp"
FILTER_FACTORY_CPP = "FilterFactory.cpp"

# pybind settings
DUSE_PYBIND = "-DUSE_PYBIND"
STD_17 = "/std:c++17"
STD_20 = "/std:c++20"

# module names
VISUALIZATION_MODULES = "visualization_modules"
LOGS_FACTORY_MODULE = "logs_factory"
FILTER_FACTORY_MODULE = "filter_factory_module"