from ..lib import *

# define variables
ARG = dict(
    n=1000, n_dis=10, m=5, nqtn=3,
    eff_mu=0, eff_sd=1, h2=.8
)

ls_objs = ["y", "y_s", "eff", "eff_s", "X", "h_y", "h_m"]
SRC = dict()
for obj in ls_objs:
    SRC[obj] = ColumnDataSource()
DT = dict()
GUI = dict()

# compile each components
from . import control
from . import figures
from . import runtime
from . import tables
from . import layout

# main
runtime.run(**ARG)
page = layout.page

