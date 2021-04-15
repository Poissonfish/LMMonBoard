from ..lib import *
from .__main__ import *
from . import path as PATH

# define notations (images)
GUI["img_X"] = Div(text="""<img src=%s height=30>""" % PATH.IMG.X.value,
                   style={"width": "60%"}, height=60,
                   align=("center"))
GUI["img_Z"] = Div(text="""<img src=%s height=30>""" % PATH.IMG.Z.value,
                   style={"width": "60%"}, height=60,
                   align=("center"))
GUI["img_sol"] = Div(text="""<img src=%s height=148>""" % PATH.IMG.EQ.value)

# assemble control panel
LO["control"] = column(
    Div(text='<h1>Inputs</h1>', max_height=38),
    row(column(Div(text='<h2>Data</h2>', max_height=40),
               LO["data"],
               sizing_mode="stretch_width",
               max_width=360,
               ),
        # Spacer(width=20),
        column(
               LO["eq"],
               LO["catcon"],
                row(LO["fixrdm"], Spacer(width=0), LO["var"]),
               sizing_mode="stretch_width",
               max_width=450, max_height=715
               ),
        ),
    GUI["bt_JWAS"],
    sizing_mode="stretch_width",
    max_width=1000,
    max_height=800)

# assemble incidence matrix
LO["incidence"] = column(
    Div(text='<h1 style>Incidence Matrix</h1>'),
    row(GUI["img_X"],
        HT["X"],
        GUI["img_Z"],
        HT["Z"]))

# assemble pedigree
LO["A"] = column(
    Div(text='<h1 style>Relationship Matrix (A)</h1>'),
    # Spacer(width=50),
    HT["A"],
    sizing_mode="stretch_width")

# assemble solver
LO["solver"] = column(
    Div(text='<h1 style>Mixed Model Equations</h1>', max_height=43),
    GUI["img_sol"],
    row(
        HT["lhs"],
        Spacer(width=30, height=100),
        HT["sol"],
        Spacer(width=60, height=100),
        HT["rhs"])
    )

# finalized layout
page = layout([[column(
            row(
                LO["control"],
                Spacer(width=90),
                LO["solver"]
            ),
            row(
                LO["A"],
                Spacer(width=20),
                LO["incidence"])
        )]])
