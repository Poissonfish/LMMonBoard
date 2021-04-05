from ..lib import *
from .main import *

# define notations (images)
GUI["img_X"] = Div(text="""<img src=%s height=30>""" % PARAM["path_img_X"],
                   style={"width": "60%"}, height=60,
                   sizing_mode="fixed", align=("center"))
GUI["img_Z"] = Div(text="""<img src=%s height=30>""" % PARAM["path_img_Z"],
                   style={"width": "60%"}, height=60,
                   sizing_mode="fixed", align=("center"))
GUI["img_sol"] = Div(text="""<img src=%s height=220>""" % PARAM["path_img_eq"],
                     sizing_mode="fixed")

# assemble control panel
LO["control"] = column(
    row(column(Div(text='<h1 style>Data</h1>'),
               LO["data"]),
        column(Div(text='<h1 style>Parameters</h1>'),
               LO["param"])),
    GUI["bt_JWAS"])

# assemble incidence matrix
LO["incidence"] = column(
    Div(text='<h1 style>Incidence Matrix</h1>'),
    row(GUI["img_X"],
        HT["X"],
        GUI["img_Z"],
        HT["Z"]))

# assemble pedigree
LO["pedigree"] = row(
    Div(text='<h1 style>Relationship Matrix</h1>'),
    Spacer(width=50),
    HT["ped"])

# assemble solver
LO["solver"] = column(
    Div(text='<h1 style>Solver</h1>'),
    GUI["img_sol"],
    row(
        HT["lhs"],
        Spacer(width=30, height=100),
        HT["sol"],
        Spacer(width=70, height=100),
        HT["rhs"]))

# finalized layout
page = layout([[column(
            row(
                LO["control"],
                Spacer(width=30),
                column(LO["incidence"],
                       LO["pedigree"])
            ),
            LO["solver"]
        )]], sizing_mode='fixed')
