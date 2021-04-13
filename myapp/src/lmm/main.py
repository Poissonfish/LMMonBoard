from ..lib import *

# define variables
PARAM = dict({})
PARAM["pX"] = 0
PARAM["pZ"] = 0
PARAM["sep_offset"] = .49

GUI = dict({})
SRC = dict({})
DT = dict({})
HT = dict({})
LO = dict({})

# compile each components
from . import control
from . import figures
from . import runtime
from . import layout
from . import path as PATH

# preload
GUI["sel_data"].value = PATH.DATA.DEMO_1.value["name"]

# main
page = layout.page
