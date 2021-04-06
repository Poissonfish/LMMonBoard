from ..lib import *
from .main import *

# define notations (images)
GUI["img_X"] = Div(text="""<img src=%s height=30>""" % PARAM["path_img_X"],
                   style={"width": "60%"}, height=60,
                   align=("center"))
GUI["img_Z"] = Div(text="""<img src=%s height=30>""" % PARAM["path_img_Z"],
                   style={"width": "60%"}, height=60,
                   align=("center"))
GUI["img_sol"] = Div(text="""<img src=%s height=148>""" % PARAM["path_img_eq"]
                    )

# assemble control panel
LO["control"] = column(
    Div(text='<h1>Inputs</h1>', max_height=38),
    row(column(Div(text='<h2>Data</h2>', max_height=40),
               LO["data"],
               sizing_mode="stretch_width",
               max_width=400,
               ),
        # Spacer(width=20),
        column(Div(text='<h2>Equation</h2>', max_height=40),
               GUI["txt_eq"],
               Div(text='<h2>Covariates</h2>', max_height=40),
               LO["catcon"],
               Div(text='<h2>Terms</h2>', max_height=40),
               LO["terms"],
               sizing_mode="stretch_width",
               max_width=400, max_height=610
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
LO["pedigree"] = column(
    Div(text='<h1 style>Relationship Matrix (A)</h1>'),
    # Spacer(width=50),
    HT["ped"],
    sizing_mode="stretch_width")

# assemble solver
LO["solver"] = column(
    Div(text='<h1 style>Solver</h1>', max_height=38),
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
                Spacer(width=50),
                LO["solver"]
            ),
            row(LO["pedigree"],
                Spacer(width=20),
                LO["incidence"])
        )]])
