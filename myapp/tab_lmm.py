# == Imports ==
from lib import *

# == Runtime functions ==
def run_JWAS_wrapper(event):
    bt_JWAS.disabled = True
    print("JWAS is running", flush=True)
    curdoc().add_next_tick_callback(run_JWAS)

def run_JWAS():
    # Take inputs
    # ARG = ["myapp/data/demo_Rosa.csv",
    #     "myapp/data/demo_ped.csv",
    #     "Weight = intercept + Sire + Animal + Dam + CG",
    #     "CG", "Animal Dam", "CG",
    #     "30", "50"]
    ARG = [ PARAM[GUI["sel_data"].value],
            PARAM[GUI["sel_ped"].value],
            GUI["txt_eq"].value,
            GUI["mc_con"].value, GUI["mc_rdms"], GUI["mc_rdmns"],
            GUI["sp_vare"], GUI["sp_varu"]]
    pd.DataFrame(ARG).to_csv(PARAM["path_Jparm"], index=False, header=None)

    try:
        subprocess.check_output('%s %s' % 
            (PARAM["path_JL"], PARAM["path_JWAS"]), shell=True)

        # update matrix
        out = dict({
            "sol": pd.read_csv("myapp/out/jwas_sol.csv"),
            "rdm": pd.read_csv("myapp/out/jwas_rdm.csv"),
            "fix": pd.read_csv("myapp/out/jwas_fix.csv"),
            "lhs": pd.read_csv("myapp/out/jwas_LHS.csv"),
            "rhs": pd.read_csv("myapp/out/jwas_RHS.csv")
        })

        SRC["X"].data = out["fix"]
        SRC["Z"].data = out["rdm"]
        SRC["lhs"].data = out["lhs"].round(3)
        SRC["rhs"].data = out["rhs"].round(3)
        SRC["sol"].data = out["sol"]

        DT["X"].columns = [TableColumn(field=c) for c in out["fix"].columns]
        DT["Z"].columns = [TableColumn(field=c) for c in out["rdm"].columns]
        DT["lhs"].columns = [TableColumn(field=c) for c in out["lhs"].columns]
        DT["rhs"].columns = [TableColumn(field=c) for c in out["rhs"].columns]
        DT["sol"].columns = [TableColumn(field="terms"), 
                             TableColumn(field="effects")]
        print("JWAS Done")

    finally:
        bt_JWAS.disabled = False

def update_terms(attr, old, new):
    ls_options = re.split("[^0-9a-zA-Z*]+", re.sub(".*= ", "", GUI["txt_eq"].value))
    GUI["mc_con"].options = ls_options
    GUI["mc_con"].value = [ls_options[0]]
    GUI["mc_rdms"].options = ls_options
    GUI["mc_rdms"].value = [ls_options[1]]
    GUI["mc_rdmns"].options = ls_options


# == Collection of var. ==
PARAM = dict({})
PARAM["path_JL"] = "/usr/local/bin/julia"
PARAM["path_JWAS"] = "myapp/jwas.jl"
PARAM["path_Jparm"] = "myapp/out/param.csv"
PARAM["demo 1"] = "myapp/data/demo_rosa.csv"
PARAM["ped 1"] = "myapp/data/demo_rosa.ped"
PARAM["size"] = "300%"

GUI = dict({})
SRC = dict({})
DT = dict({})
LO = dict({})

# == Data ==
dt_data = pd.read_csv(PARAM["demo 1"])
SRC["data"] = ColumnDataSource(dt_data)
DT["data"] = DataTable(source=SRC["data"],
                       columns=[TableColumn(field=str(s))
                                for s in dt_data.columns],
                       height=200)

dt_ped = pd.read_csv(PARAM["ped 1"])
SRC["ped"] = ColumnDataSource(dt_ped)
DT["ped"] = DataTable(source=SRC["ped"],
                      columns=[TableColumn(field=str(s))
                               for s in dt_ped.columns],
                      height=200)

GUI["sel_data"] = Select(title="Input data:", value="demo 1", options=[
    "demo 1", "demo 2", "demo 3"])
GUI["sel_ped"] = Select(title="Input pedigree:", value="demo 1", options=[
    "ped 1", "ped 2", "ped 3"])

GUI["col_data"] = column(GUI["sel_data"], DT["data"])
GUI["col_ped"] = column(GUI["sel_ped"], DT["ped"])
GUI["sec_data"] = row(GUI["col_data"], GUI["col_ped"])

# == Parameters ==
GUI["txt_eq"] = TextInput(value="", title="Equation")
GUI["mc_con"] = MultiChoice(title="Continuos", value=[], options=[])
GUI["mc_cat"] = MultiChoice(title="Categorical", value=[], options=[])
GUI["mc_fix"] = MultiChoice(title="Fixed Effects", value=[], options=[])
GUI["mc_rdms"] = MultiChoice(title="Random Effects (Structured)", value=[], options=[])
GUI["mc_rdmns"] = MultiChoice(title="Random Effects (Non-structured)", value=[], options=[])
GUI["sp_vare"] = Spinner(low=5, high=100, value=50, step=5, title="VarE")
GUI["sp_varu"] = Spinner(low=5, high=100, value=50, step=5, title="VarU")
GUI["bt_JWAS"] = Button(label="Run JWAS", button_type="success")

GUI["row_catcon"] = row(GUI["mc_con"], GUI["mc_cat"])
GUI["row_fixrdm"] = row(GUI["mc_fix"], GUI["mc_rdms"], GUI["mc_rdmns"])
GUI["row_var"] = row(GUI["sp_vare"], GUI["sp_varu"])
GUI["sec_param"] = column(GUI["txt_eq"], 
                          GUI["row_catcon"], 
                          GUI["row_fixrdm"],
                          GUI["row_var"],
                          GUI["bt_JWAS"])

# == Design Matrix ==
SRC["X"] = ColumnDataSource()
SRC["Z"] = ColumnDataSource()
DT["X"] = DataTable(source=SRC["X"],
                    index_position=None, header_row=True,
                    width=100, height=250, editable=False,
                    align=("center", "end"))
DT["Z"] = DataTable(source=SRC["Z"],
                    index_position=None, header_row=True,
                    width=300, height=250, editable=False,
                    align=("center", "center"))

GUI["img_X"] = Div(text="""<img src="/static/img_x.png">""",
                   height=100, sizing_mode="fixed")
GUI["img_Z"] = Div(text="""<img src="/static/img_z.png">""",
                   height=100, sizing_mode="fixed")

GUI["sec_design"] = row(GUI["img_X"], DT["X"], 
                        GUI["img_Z"], DT["Z"])

# == Solver ==
SRC["lhs"] = ColumnDataSource()
SRC["rhs"] = ColumnDataSource()
SRC["sol"] = ColumnDataSource()
W = 250; H = 300
DT["lhs"] = DataTable(source=SRC["lhs"],
                      index_position=None, header_row=True,
                      width=W+85, height=H, editable=False,
                      align=("end", "end"))
DT["rhs"] = DataTable(source=SRC["rhs"],
                      index_position=None, header_row=True,
                      width=W-100, height=H, editable=False,
                      align=("end", "end"))
DT["sol"] = DataTable(source=SRC["sol"],
                      index_position=None, header_row=True,
                      width=W-150, height=H, editable=False,
                      align=("end", "end"))

GUI["img_sol"] = Div(text="""<img src="/static/img_eq.png">""",
                    height=100, sizing_mode="fixed")
GUI["spc_lhssol"] = Spacer(width=50, height=100)
GUI["spc_solrhs"] = Spacer(width=100, height=100)
GUI["row_sol"] = row(
            DT["lhs"],
            GUI["spc_lhssol"], 
            DT["sol"],
            GUI["spc_solrhs"],
            DT["rhs"])
GUI["sec_solver"] = column(GUI["img_sol"], GUI["row_sol"])

# == Layout ==
GUI["txt_eq"].on_change("value", update_terms)
GUI["bt_JWAS"].on_click(run_JWAS_wrapper)
layout = layout([[column(
            Div(text='<h1 style>Data</h1>'),
            GUI["sec_data"],
            Div(text='<h1 style>Parameters</h1>'),
            GUI["sec_param"],
            Div(text='<h1 style>Design Matrix</h1>'),
            GUI["sec_design"],
            Div(text='<h1 style>Solver</h1>'),
            GUI["sec_solver"]
        )]], sizing_mode='fixed')

