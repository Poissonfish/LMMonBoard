# == Imports ==
from lib import *

# == Runtime functions ==
def run_JWAS_wrapper(event):
    GUI["bt_JWAS"].disabled = True
    print("JWAS is running", flush=True)
    curdoc().add_next_tick_callback(run_JWAS)

def run_JWAS():
    # Debug
    # ARG = ["myapp/data/demo_rosa.csv",
    #     "myapp/data/demo_rosa.ped",
    #     "Weight = intercept + Sire + Animal + Dam + CG",
    #     "CG", "Animal Dam", "CG",
    #     "30", "50"]
    ARG = [ PARAM[GUI["sel_data"].value],
            PARAM[GUI["sel_data"].value + " ped"],
            GUI["txt_eq"].value,
            GUI["mc_con"].value, GUI["mc_rdms"].value, GUI["mc_rdmns"].value,
            GUI["sp_vare"].value, GUI["sp_varu"].value]
    ARG = [re.sub(r'[\[\]\',]', '', str(a)) for a in ARG]
    pd.DataFrame(ARG).to_csv(PARAM["path_Jparm"], index=False, header=None)

    try:
        # subprocess.check_output('%s %s' % 
        #     (PARAM["path_JL"], PARAM["path_JWAS"]), shell=True)

        # update matrix
        for item in ["X", "Z", "lhs", "rhs", "sol"]:
            dt = pd.read_csv("myapp/out/jwas_%s.csv" % item)
            SRC[item].data = dt.round(3)
            if item != "sol":
                DT[item].columns = [TableColumn(field=c)
                                    for c in dt.columns]
            else:
                DT["sol"].columns = [TableColumn(field="terms"),
                                     TableColumn(field="effects")]
        
        # update ped heatmap
        dt = pd.read_csv("myapp/out/jwas_ped.csv", header=None)
        dt_heat = pd.melt(dt.reset_index(), id_vars="index")
        dt_heat.columns = ["y", "x", "ped"]
        dt_heat["x"] += 1
        dt_heat["y"] += 1
        SRC["PED"].data = dt_heat


        print("JWAS Done")

    finally:
        GUI["bt_JWAS"].disabled = False

def update_terms(attr, old, new):
    ls_options = re.split("[^0-9a-zA-Z*]+", re.split("\s*=\s*", GUI["txt_eq"].value)[1])
    GUI["mc_cat"].options = ls_options
    GUI["mc_con"].options = ls_options
    GUI["mc_fix"].options = ls_options
    GUI["mc_rdms"].options = ls_options
    GUI["mc_rdmns"].options = ls_options

    GUI["mc_cat"].value = ls_options
    GUI["mc_rdms"].value = ls_options

def choose_con(attr, old, new):
    GUI["mc_cat"].value = list(set(GUI["mc_cat"].value) - set(new))
def choose_cat(attr, old, new):
    GUI["mc_con"].value = list(set(GUI["mc_con"].value) - set(new))
def choose_fix(attr, old, new):
    GUI["mc_rdms"].value = list(set(GUI["mc_rdms"].value) - set(new))
    GUI["mc_rdmns"].value = list(set(GUI["mc_rdmns"].value) - set(new))
def choose_rdms(attr, old, new):
    GUI["mc_fix"].value = list(set(GUI["mc_fix"].value) - set(new))
    GUI["mc_rdmns"].value = list(set(GUI["mc_rdmns"].value) - set(new))
def choose_rdmns(attr, old, new):
    GUI["mc_rdms"].value = list(set(GUI["mc_rdms"].value) - set(new))
    GUI["mc_fix"].value = list(set(GUI["mc_fix"].value) - set(new))

# == Collection of var. ==
PARAM = dict({})
PARAM["path_JL"] = "/usr/local/bin/julia"
PARAM["path_JWAS"] = "myapp/jwas.jl"
PARAM["path_Jparm"] = "myapp/out/param.csv"
PARAM["demo 1"] = "myapp/data/demo_rosa.csv"
PARAM["demo 1 ped"] = "myapp/data/demo_rosa.ped"
PARAM["path_img_eq"] = "myapp/static/img_eq.png"
PARAM["path_img_X"] = "myapp/static/img_X.png"
PARAM["path_img_Z"] = "myapp/static/img_Z.png"
PARAM["empty_dt"] = pd.DataFrame(dict({"Empty": [0]}))

PARAM["size"] = "300%"

GUI = dict({})
SRC = dict({})
DT = dict({})
LO = dict({})

# == Data ==
W_data = 300
dt_data = pd.read_csv(PARAM["demo 1"])
SRC["data"] = ColumnDataSource(dt_data)
DT["data"] = DataTable(source=SRC["data"],
                       columns=[TableColumn(field=str(s))
                                for s in dt_data.columns],
                       height=200, width=W_data)

dt_ped = pd.read_csv(PARAM["demo 1 ped"])
SRC["ped"] = ColumnDataSource(dt_ped)
DT["ped"] = DataTable(source=SRC["ped"],
                      columns=[TableColumn(field=str(s))
                               for s in dt_ped.columns],
                      height=200, width=W_data)

GUI["sel_data"] = Select(title="Input data:", value="demo 1", options=[
    "demo 1", "demo 2", "demo 3"])
GUI["sec_data"] = column(GUI["sel_data"], DT["data"],
                         PreText(text="Pedigree"), DT["ped"])

# == Parameters ==
GUI["txt_eq"] = TextInput(title="Equation", value="",
                          sizing_mode="stretch_width")
GUI["mc_con"] = MultiChoice(title="Continuous", 
                            value=[], options=[], sizing_mode="stretch_width")
GUI["mc_cat"] = MultiChoice(title="Categorical",
                            value=[], options=[], sizing_mode="stretch_width")
GUI["mc_fix"] = MultiChoice(title="Fixed Effects",
                            value=[], options=[],  sizing_mode="stretch_width")
GUI["mc_rdms"] = MultiChoice(title="Random Effects (Structured)", 
                             value=[], options=[], sizing_mode="stretch_width")
GUI["mc_rdmns"] = MultiChoice(title="Random Effects (Non-structured)", 
                              value=[], options=[], sizing_mode="stretch_width")
GUI["sp_vare"] = Spinner(title="VarE", low=5, high=100, value=50,
                         step=5, sizing_mode="stretch_width")
GUI["sp_varu"] = Spinner(title="VarU", low=5, high=100, value=50,
                         step=5, sizing_mode="stretch_width")
GUI["bt_JWAS"] = Button(
    label="Run JWAS", button_type="success", sizing_mode="stretch_width")

GUI["row_catcon"] = column(GUI["mc_con"], GUI["mc_cat"])
GUI["row_fixrdm"] = column(GUI["mc_fix"], GUI["mc_rdms"], GUI["mc_rdmns"])
GUI["row_var"] = row(GUI["sp_vare"], GUI["sp_varu"], sizing_mode="stretch_width")
GUI["sec_param"] = column(GUI["txt_eq"], 
                          row(GUI["row_catcon"], GUI["row_fixrdm"], sizing_mode="stretch_both"),
                          GUI["row_var"],
                          GUI["bt_JWAS"], 
                          sizing_mode="fixed",
                          width=400, height=500)

# == Heat map == 
SRC["PED"] = ColumnDataSource(pd.DataFrame({"x":[0], "y":[0]}))

colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2",
          "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
mapper = LinearColorMapper(
    # low=dt.rate.min(), high=dt.rate.max(),
    palette=colors)
GUI["img_ped"] = figure(plot_width=300, plot_height=300,
           align=("center"),
           #    x_range=list(dt.index),
           #    y_range=list(reversed(np.unique(dt_heat.y))),
           toolbar_location=None, tools="", x_axis_location="above")
GUI["img_ped"].y_range.flipped = True
GUI["img_ped"].rect(x="x", y="y", width=1, height=1, source=SRC["PED"],
       line_color=None, fill_color=transform('ped', mapper))
color_bar = ColorBar(color_mapper=mapper)
GUI["img_ped"].add_layout(color_bar, 'right')


# == Design Matrix ==
SRC["X"] = ColumnDataSource()
SRC["Z"] = ColumnDataSource()
DT["X"] = DataTable(source=SRC["X"],
                    columns=[TableColumn(field="Empty Data")],
                    header_row=True, editable=False,
                    width=300, height=200, align=("center"))
DT["Z"] = DataTable(source=SRC["Z"],
                    columns=[TableColumn(field="Empty Data")],
                    header_row=True, editable=False,
                    width=400, height=200, align=("center"))

GUI["img_X"] = Div(text="""<img src=%s height=30>""" % PARAM["path_img_X"],
                   style={"width": "60%"},
                   height=60, sizing_mode="fixed", align=("center"))
GUI["img_Z"] = Div(text="""<img src=%s height=30>""" % PARAM["path_img_Z"],
                   style={"width": "60%"},
                   height=60, sizing_mode="fixed", align=("center"))

GUI["sec_design"] = row(GUI["img_X"], DT["X"], GUI["img_Z"], DT["Z"])

# == Solver ==
SRC["lhs"] = ColumnDataSource()
SRC["rhs"] = ColumnDataSource()
SRC["sol"] = ColumnDataSource()
W = 350; H = 500
DT["lhs"] = DataTable(source=SRC["lhs"],
                      columns=[TableColumn(field="Empty Data")],
                      index_position=None, header_row=True,
                      width=W+150, height=H, editable=False,
                      align=("end", "end"))
DT["sol"] = DataTable(source=SRC["sol"],
                      columns=[TableColumn(field="Empty Data")],
                      index_position=None, header_row=True,
                      width=W-150, height=H, editable=False,
                      align=("end", "end"))
DT["rhs"] = DataTable(source=SRC["rhs"],
                      columns=[TableColumn(field="Empty Data")],
                      index_position=None, header_row=True,
                      width=W-300, height=H, editable=False,
                      align=("end", "end"))
GUI["img_sol"] = Div(text="""<img src=%s height=180>""" % PARAM["path_img_eq"],
                     sizing_mode="fixed")
GUI["spc_lhssol"] = Spacer(width=70, height=100)
GUI["spc_solrhs"] = Spacer(width=70, height=100)
GUI["row_sol"] = row(
            DT["lhs"],
            GUI["spc_lhssol"], 
            DT["sol"],
            GUI["spc_solrhs"],
            DT["rhs"])
GUI["sec_solver"] = column(GUI["img_sol"], GUI["row_sol"])

# == Interactive ==
GUI["txt_eq"].on_change("value", update_terms)
GUI["bt_JWAS"].on_click(run_JWAS_wrapper)
GUI["mc_con"].on_change("value", choose_con)
GUI["mc_cat"].on_change("value", choose_cat)
GUI["mc_fix"].on_change("value", choose_fix)
GUI["mc_rdms"].on_change("value", choose_rdms)
GUI["mc_rdmns"].on_change("value", choose_rdmns)

# option_tmp = GUI["mc_cat"].options
# option_tmp.remove(new)
# GUI["mc_cat"].options = option_tmp



# == Layout ==
layout = layout([[column(
            row(
                column(Div(text='<h1 style>Data</h1>'), GUI["sec_data"]),
                column(Div(text='<h1 style>Parameters</h1>'), GUI["sec_param"]),
                Spacer(width=50),
                column(Div(text='<h1 style>Design Matrix</h1>'), GUI["sec_design"], 
                       row(Div(text='<h1 style>Pedigree Heatmap</h1>'), GUI["img_ped"]))
            ),
            Div(text='<h1 style>Solver</h1>'),
            GUI["sec_solver"]
        )]], sizing_mode='fixed')

