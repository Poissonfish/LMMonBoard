from ..lib import *
from .__main__ import *
from . import path as PATH

def get_layout(GUI, LO, HT):
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
        row(
            column(LO["data"]),
            Spacer(width=20),
            column(LO["catcon"]),
            Spacer(width=20),
            column(LO["fixrdm"]),
            Spacer(width=20),
            column(LO["var"]),
            # sizing_mode="stretch_width",
            max_width=4000, max_height=715),
        # sizing_mode="stretch_width",
        max_width=4000,
        max_height=800)

    # assemble pedigree
    LO["A"] = column(
        Div(text='<h1 style>Relationship Matrix (Derived from Pedigree)</h1>'),
        # Spacer(width=50),
        HT["A"],
        sizing_mode="stretch_width")

    # assemble incidence matrix
    LO["incidence"] = column(
        Div(text='<h1 style>Incidence Matrix</h1>'),
        row(GUI["img_X"], HT["X"]),
        row(GUI["img_Z"], HT["Z"]))

    # assemble solver
    LO["solver"] = column(
        Div(text='<h1 style>Mixed Model Equations</h1>', max_height=43),
        row(Spacer(width=280), GUI["img_sol"]),
        row(
            HT["lhs"],
            Spacer(width=80, height=100),
            HT["sol"],
            Spacer(width=200, height=100),
            HT["rhs"])
        )

    # finalized layout
    return layout([[column(
                # GUI["bt_JWAS"],
                LO["logger"],
                LO["control"],
                row(
                    LO["A"],
                    Spacer(width=90),
                    LO["incidence"]
                ),
                LO["solver"]
            )]])
