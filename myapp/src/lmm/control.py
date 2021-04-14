from ..lib import *
from .main import *
from . import path as PATH

# load data and display
H=270
W=320
SRC["data"] = ColumnDataSource()
DT["data"] = DataTable(source=SRC["data"],
                       columns=[],
                       editable=True,
                       height=H, width=W)
SRC["ped"] = ColumnDataSource()
DT["ped"] = DataTable(source=SRC["ped"],
                      columns=[],
                      editable=True,
                      height=H, width=W)

GUI["sel_data"] = Select(title="Input data:",
                         options=PATH.DATA.get_names())

LO["data"] = column(GUI["sel_data"],
                    DT["data"],
                    PreText(text="Pedigree"),
                    DT["ped"])

# JWAS parameters
GUI["txt_eq"] = TextInput(
    title=" ")

# continuous vs categorical
GUI["mc_con"] = MultiChoice(
    title="Continuous",
    delete_button=False,
    height=120)

GUI["mc_cat"] = MultiChoice(
    title="Categorical",
    delete_button=False,
    height=120) # actually we only need mc_con height to be set

# fixed, random, random iid
h = 105
GUI["mc_fix"] = MultiChoice(
    title="Fixed Effects",
    delete_button=False,
    height=h)
GUI["mc_rdms"] = MultiChoice(
    title="Random Effects (Correlated (A))",
    delete_button=False,
    height=h)
GUI["mc_rdmns"] = MultiChoice(
    title="Random Effects (i.i.d.)",
    delete_button=False,
    height=h - 5)

# variance components
h = 110
w = 180
GUI["sp_vare"] = Spinner(title="Residuals (i.i.d.)",
                         low=0.1, high=10, value=4,
                         height=50,
                         step=.01)


SRC["Gres"] =  ColumnDataSource()
DT["Gres"] = DataTable(source=SRC["Gres"],
                        columns=[],
                        editable=True,
                        width=w,
                        height=h-60,
                        index_position=None
                   )

SRC["Gstr"] =  ColumnDataSource()
DT["Gstr"] = DataTable(source=SRC["Gstr"],
                        columns=[],
                        editable=True,
                        width=w,
                        height=h,
                        index_position=None
                   )

SRC["Giid"] =  ColumnDataSource()
DT["Giid"] = DataTable(source=SRC["Giid"],
                        columns=[],
                        editable=True,
                        width=w,
                        height=h,
                        index_position=None
                   )

# JWAS button
GUI["bt_JWAS"] = Button(
    # background="#d8773e",
    label="Run JWAS", button_type="success")

# layout
LO["eq"] = Column(
    Div(text='<h2>Model Equation</h2>', max_height=40),
    GUI["txt_eq"]
)

LO["catcon"] = column(
    Div(text='<h2>Continuous/Categorical Variables</h2>', max_height=40),
    row(GUI["mc_con"], GUI["mc_cat"]),
    sizing_mode="stretch_width"
)

LO["fixrdm"] = column(
    Div(text='<h2>Fixed/Random Effects</h2>', max_height=70),
    GUI["mc_fix"],
    GUI["mc_rdms"],
    GUI["mc_rdmns"],
    sizing_mode="stretch_width")

LO["var"] = column(
    Div(text='<h2>Variance Components</h2>', max_height=70),
    PreText(text="Residuals (i.i.d.)"),
    DT["Gres"],
    PreText(text="Random Effects (Correlated (A))"),
    DT["Gstr"],
    # Spacer(height=50),
    PreText(text="Random Efffects (i.i.d.)"),
    DT["Giid"],
    sizing_mode="stretch_width")

