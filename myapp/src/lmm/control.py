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
    title="Equation",
    value="Weight = intercept + Animal + Sire + CG")

# continuous vs categorical
GUI["mc_con"] = MultiChoice(
    title="Continuous",
    value=["intercept"],
    options=preoptions)
GUI["mc_cat"] = MultiChoice(
    title="Categorical",
    value=["Animal", "Sire", "CG"],
    options=preoptions)

# fixed, random, random iid
GUI["mc_fix"] = MultiChoice(
    title="Fixed Effects",
    value=["intercept", "CG"],
    options=preoptions)
GUI["mc_rdms"] = MultiChoice(
    title="Random Effects (Structured)",
    value=["Animal", "Sire"],
    options=preoptions)
GUI["mc_rdmns"] = MultiChoice(
    title="Random Effects (i.i.d.)",
    value=[],
    options=preoptions)

# variance components
SRC["varG"] =  ColumnDataSource(pd.DataFrame())
DT["varG"] = DataTable(source=SRC["varG"],
                   columns=[],
                   editable=True,
                   width=180,
                   index_position=None
                   )

GUI["sp_vare"] = Spinner(title="Residual Variance", low=5, high=100, value=50,
                         step=5)

# JWAS button
GUI["bt_JWAS"] = Button(
    # background="#d8773e",
    label="Run JWAS", button_type="success")

# layout
LO["catcon"] = row(GUI["mc_con"], GUI["mc_cat"]
                   )
GUI["col_fixrdm"] = column(GUI["mc_fix"], GUI["mc_rdms"], GUI["mc_rdmns"])
GUI["col_var"] = column(GUI["sp_vare"],
                        Spacer(height=50),
                        PreText(text="Covariance/Variance \n(Random i.i.d.)"),
                        DT["varG"])
LO["terms"] = row(GUI["col_fixrdm"], GUI["col_var"],
                  sizing_mode="stretch_width",
                  width=400, height=500,
                  )
