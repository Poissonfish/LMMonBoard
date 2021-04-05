from ..lib import *
from .main import *

# load data and display
dt_data = pd.read_csv(PARAM["demo 1"])
SRC["data"] = ColumnDataSource(dt_data)
DT["data"] = DataTable(source=SRC["data"],
                       columns=[TableColumn(field=str(s))
                                for s in dt_data.columns],
                       editable=True,
                       height=200, width=300)
DT["ped"] = DataTable(source=SRC["data"],
                      columns=[TableColumn(field="Animal"),
                               TableColumn(field="Sire"),
                               TableColumn(field="Dam")],
                      editable=True,
                      height=200, width=300)

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
    value="Weight = intercept + Animal + Sire + CG",
    sizing_mode="stretch_width")

# continuous vs categorical
GUI["mc_con"] = MultiChoice(
    title="Continuous",
    value=["intercept"],
    options=preoptions,
    sizing_mode="stretch_width")
GUI["mc_cat"] = MultiChoice(
    title="Categorical",
    value=["Animal", "Sire", "CG"],
    options=preoptions,
    sizing_mode="stretch_width")

# fixed, random, random iid
GUI["mc_fix"] = MultiChoice(
    title="Fixed Effects",
    value=["intercept", "CG"],
    options=preoptions,
    sizing_mode="stretch_width")
GUI["mc_rdms"] = MultiChoice(
    title="Random Effects (Structured)",
    value=["Animal", "Sire"],
    options=preoptions,
    sizing_mode="stretch_width")
GUI["mc_rdmns"] = MultiChoice(
    title="Random Effects (Non-Structured)",
    value=[],
    options=preoptions,
    sizing_mode="stretch_width")

# variance components
GUI["sp_vare"] = Spinner(title="VarE", low=5, high=100, value=50,
                         step=5, sizing_mode="stretch_width")
GUI["sp_varu"] = Spinner(title="VarU", low=5, high=100, value=50,
                         step=5, sizing_mode="stretch_width")

# layout
GUI["bt_JWAS"] = Button(
    label="Run JWAS", button_type="success", sizing_mode="stretch_width")

GUI["row_catcon"] = column(GUI["mc_con"], GUI["mc_cat"])
GUI["row_fixrdm"] = column(GUI["mc_fix"], GUI["mc_rdms"], GUI["mc_rdmns"])
GUI["row_var"] = row(GUI["sp_vare"], GUI["sp_varu"],
                     sizing_mode="stretch_width")
LO["param"] = column(GUI["txt_eq"],
                     row(GUI["row_catcon"], GUI["row_fixrdm"],
                         sizing_mode="stretch_both"),
                     GUI["row_var"],
                     sizing_mode="fixed", width=400, height=500)