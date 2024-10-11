from enum import Enum


class ErrorMessages(Enum):
    ERROR = "Error: ",
    FAILED_TO_RETIEVE_ATTRIBUTE = "Failed to retrieve attribute '{attribute}': {error}"
    OBJECT_IS_NONE = "{object} is None"
    SHOWING_WIDGET = "showing {widget}"
    ADJUSTING_SIZES_WIDGET = "adjusting {widget} sizes"
    ERROR_OCCURRED = "An error occurred {error}"
    FILE_NOT_FOUND = "The file {filename} was not found."
    JSON_NOT_VALID = "The file {filename} is not a valid JSON. Original error: {e}"
    INDEX_OUT_OF_RANGE = "The index {index} is out of range in {object}"

class WarningMessages(Enum):
    WARNING = "Warning",
    WARNING_MISSING_DATA = "Missing data for component: {component}"
    INVALID_DATA = "Invalid {component} data: {data}"
    STYLE_SHEET_FILE_NOT_FOUND = "Stylesheet file '{filename}' not found."
    UNKNOWN_FILTER = "Unknown filter: {filter_type}"