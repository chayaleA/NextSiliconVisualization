from PyQt5.QtCore import Qt
from utils.type_names import BMT, H2G, G2H, PCIE, CBU, TCU, ECORE, DIE, QUAD, CBUS_INJ, CBUS_CLT, NFI_INJ, NFI_CLT, EQ, \
    IRQA, IQR, IQD, BIN

CHIP = "chip"
DIES = "DIES"
QUADS = "QUADS"
ECORES = "Ecores"
CBUS = "CBUs"
TCUS = "TCUs"
EQS = "EQs"
ID = "id"
ENABLED_CLUSTERS = "enabled_clusters"
TOP = "Top"
COL = "col"
COLUMN = "Column"
ROW = "row"
DID = "did"
GRID = "GRID"
NAME = "name"
FILTER = "Filter"

CLUSTER_ID = "cluster_id"
TID = "tid"
PACKET = "packet"
UNIT = "unit"
AREA = "area"
TIMESTAMP = "timeStemp"

OBJECT_COLORS = {
    BMT: "lightblue",
    H2G: "pink",
    G2H: "coral",
    PCIE: "yellow",
    CBU: "blue",
    TCU: "red",
    ECORE: "#32CD32",
    DIE: "orange",
    QUAD: "cyan",
    CBUS_INJ: "#4682B4",  # SteelBlue
    CBUS_CLT: "#B0C4DE",  # LightSteelBlue
    NFI_INJ: "#5F9EA0",  # CadetBlue
    NFI_CLT: "#87CEEB",  # SkyBlue
    EQ: "red",
    IRQA: "#AAAAAA",
    IQR: "DeepPink",
    IQD: "coral",
    BIN: "Magenta",
}

# titles
CLOSE = "Close"
UNKNOWN = "Unknown"
SIMULATOR_INSTRUCTIONS = "Simulator Instructions"
SIMULATOR = "HW Simulator"
MAIN_TOOLBAR = "Main Toolbar"
DIE2DIE_LOGS = "DIE2DIE Logs"
HOST_INTERFACE_Logs = "Host Interface Logs"
QUAD_LOGS = "Quad Logs"
HBM_LOGS = "HBM Logs"
X_BUTTON = "X"
COMPONENT_LOGS = "{component} Logs"
EMPTY = "Empty"
VIEW_LOGS = "View Logs"

# colors
BLACK = "black"
WHITE = "white"
LIGHTGRAY = "lightgray"
GREEN = "green"
RED = "red"
GRAY = "gray"

# open_files
READ = "r"

# settings
NUM_QUADS_PER_SIDE = 2
NUM_CLUSTERS_PER_SIDE = 8
NUM_DIES = 2

#CURSOR
ARROW_CURSOR = Qt.ArrowCursor
FORBIDDEN_CURSOR = Qt.ForbiddenCursor
POINTING_CURSOR = Qt.PointingHandCursor