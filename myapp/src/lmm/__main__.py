from ..lib import *

def page_lmm():
    # define variables
    PARAM = dict({})
    PARAM["pX"] = 0
    PARAM["pZ"] = 0
    PARAM["sep_offset"] = .49
    PARAM["enable_JWAS"] = True

    GUI = dict({})
    SRC = dict({})
    DT = dict({})
    HT = dict({})
    LO = dict({})

    # compile each components
    from . import control
    control.set_control(GUI, SRC, DT, LO)

    from . import figures
    figures.set_figures(SRC, HT)

    from . import runtime
    runtime.set_runtime(SRC, GUI, PARAM, DT, HT)

    from . import layout
    page = layout.get_layout(GUI, LO, HT)

    from . import path as PATH

    # preload
    GUI["sel_data"].value = PATH.DATA.DEMO_3.value["name"]

    # main
    return page


# p110
# 7-2 maternal trait
