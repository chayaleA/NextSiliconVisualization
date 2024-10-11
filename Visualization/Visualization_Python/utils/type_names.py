DIE = "die"
DIE1 = "DIE 1"
DIE2 = "DIE 2"
QUAD = "quad"

CBU = "Cbu"
TCU = "Tcu"
ECORE = "Ecore"

MCU = "MCU"
LNB = "lnb"

HOST_INTERFACE = "Host Interface"
H2G = "H2G"
G2H = "G2H"
BMT = "bmt"
PCIE = "pcie"

CBUS_INJ = "cbus inj"
CBUS_CLT = "cbus clt"
NFI_INJ = "nfi inj"
NFI_CLT = "nfi clt"

HBM = "hbm"

IQR = "iqr"
IQD = "iqd"
IRQA = "irqa"
D2D = "d2d"
DIE2DIE = "Die 2 Die"
EQ = "eq"
BIN = "bin"

HI = "host if"
ECORE_RSP_CIP = "ecore rsp cip"
ECORE_REQ_CIP = "ecore req cip"
MCU_GATE_1 = "mcu gate 1"
MCU_GATE_0 = "mcu gate 0"
MEM_0 = "mem0"
MEM_1 = "mem1"
LCIP = "lcip"
NFI = "nfi"

AREAS = {
    HBM: HBM,
    D2D: D2D,
    BMT: BMT,
    HI: HOST_INTERFACE,
    PCIE: PCIE,
    ECORE_REQ_CIP: ECORE,
    ECORE_RSP_CIP: ECORE,
    MCU_GATE_1: MCU,
    MCU_GATE_0: MCU,
    MEM_0: CBU,
    MEM_1: CBU,
    LCIP: CBU,
    NFI: LNB
}

UNITS = [
    BMT,
    PCIE,
    CBUS_INJ,
    CBUS_CLT,
    NFI_INJ,
    NFI_CLT,
    EQ,
    HBM,
    IQR,
    IQD,
    BIN,
    LNB
]

FCB2 = "fcb2"
LCB1 = "lcb1"
LCB2 = "lcb2"
MEP0 = "mep0"
LCEP = "lcep"
ULCEP = "ulcep"
MMU_COMPLEX = "mmu_complex"
MEPS_SATP = "meps_satp"
MEP1 = "mep1"
CBUE_XBAR_WRAP = "cbue_xbar_wrap"
CBUE_TLM_WRAP = "cbue_tlm_wrap"
LCB0 = "lcb0"
FCB0 = "fcb0"
FCB1 = "fcb1"
CBUI_XBAR_WRAP = "cbui_xbar_wrap"
MEMCIP0 = "memcip0"
MEMCIP1 = "memcip1"
LCIP = "lcip"
ULCIP = "ulcip"
BIG_RS = "big_rs"
CBUI_TLM_WRAP = "cbui_tlm_wrap"
CFG_MNGR = "cfg_mngr"

SUBUNITS = [
    FCB0,
    FCB1,
    FCB2,
    LCB0,
    LCB1,
    LCB2,
    MMU_COMPLEX,
    MEPS_SATP,
    MEP0,
    MEP1,
    MEMCIP0,
    MEMCIP1,
    CBUI_XBAR_WRAP,
    CBUE_XBAR_WRAP,
    CBUE_TLM_WRAP,
    CBUI_TLM_WRAP,
    LCEP,
    LCIP,
    ULCEP,
    ULCIP,
    BIG_RS,
    CFG_MNGR
]