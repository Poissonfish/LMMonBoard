from ..lib import *
from .main import *

# load data and display
dt_data = pd.read_csv(PARAM["demo 1"])
SRC["data"] = ColumnDataSource(dt_data)
DT["data"] = DataTable(source=SRC["data"],
                       columns=[TableColumn(field=str(s))
                                for s in dt_data.columns],
                       editable=True,
                       height=200, width=320)
DT["ped"] = DataTable(source=SRC["data"],
                      columns=[TableColumn(field="Animal"),
                               TableColumn(field="Sire"),
                               TableColumn(field="Dam")],
                      editable=True,
                      height=200, width=320)

GUI["sel_data"] = Select(title="Input data:",
                         value="demo 1",
                         options=["demo 1", "demo 2", "demo 3"])
LO["data"] = column(GUI["sel_data"],
                    DT["data"],
                    PreText(text="Pedigree"),
                    DT["ped"])

# JWAS parameters
preoptions = ["intercept", "Animal", "Sire", "CG"]
GUI["txt_eq"] = TextInput(
    title=" ",
    value="Weight = intercept + Animal + Sire + CG")

# continuous vs categorical
GUI["mc_con"] = MultiChoice(
    title="Continuous",
    value=["intercept"],
    height=120,
    options=preoptions)
GUI["mc_cat"] = MultiChoice(
    title="Categorical",
    height=120, # actually we only need mc_con to be set
    value=["Animal", "Sire", "CG"],
    options=preoptions)

# fixed, random, random iid
h = 105
GUI["mc_fix"] = MultiChoice(
    title="Fixed Effects",
    height=h,
    options=preoptions)
GUI["mc_rdms"] = MultiChoice(
    title="Random Effects (Structured)",
    height=h,
    options=preoptions)
GUI["mc_rdmns"] = MultiChoice(
    title="Random Effects (i.i.d.)",
    value=[],
    height=h-5,
    options=preoptions)

# variance components
h = 110
GUI["sp_vare"] = Spinner(title="Residual Variance",
                         low=0.1, high=10, value=4,
                         height=50,
                         step=.01)

SRC["Gstr"] =  ColumnDataSource(pd.DataFrame())
DT["Gstr"] = DataTable(source=SRC["Gstr"],
                        columns=[],
                        editable=True,
                        width=180,
                        height=h,
                        index_position=None
                   )

SRC["Giid"] =  ColumnDataSource(pd.DataFrame())
DT["Giid"] = DataTable(source=SRC["Giid"],
                        columns=[],
                        editable=True,
                        width=180,
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
    GUI["sp_vare"],
    PreText(text="Random Effect (Structured)"),
    DT["Gstr"],
    # Spacer(height=50),
    PreText(text="Random Efffect (i.i.d.)"),
    DT["Giid"],
    sizing_mode="stretch_width")

