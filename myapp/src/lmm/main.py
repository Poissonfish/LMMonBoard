from ..lib import *

# define variables
PARAM = dict({})
PARAM["path_JL"] =      "/usr/local/bin/julia"
PARAM["path_JWAS"] =    "myapp/jwas.jl"
PARAM["path_JWAS_param"] =   "myapp/out/param.csv"
PARAM["demo 1"] =       "myapp/data/demo_rosa.csv"
PARAM["demo 1 ped"] =   "myapp/data/demo_rosa.ped"
PARAM["path_cusdata"] =  "myapp/data/customized.csv"
PARAM["path_cusped"] =  "myapp/data/customized.ped"
PARAM["path_img_eq"] =  "myapp/static/img_eq2.png"
PARAM["path_img_X"] =   "myapp/static/img_X.png"
PARAM["path_img_Z"] =   "myapp/static/img_Z.png"
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

# main
page = layout.page
