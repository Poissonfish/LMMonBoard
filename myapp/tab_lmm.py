# == Imports ==
from lib import *

# == Runtime functions ==
def run_JWAS_wrapper(event):
    GUI["bt_JWAS"].disabled = True
    print("JWAS is running", flush=True)
    curdoc().add_next_tick_callback(run_JWAS)

def run_JWAS():
    # output PED
    pd.DataFrame(SRC["ped"].data).iloc[:, 1:].to_csv(
        PARAM["path_ped"], index=False)

    # take inputs
    ARG = [ PARAM[GUI["sel_data"].value],
            PARAM["path_ped"],
            GUI["txt_eq"].value,
            GUI["mc_con"].value, GUI["mc_rdms"].value, GUI["mc_rdmns"].value,
            GUI["sp_vare"].value, GUI["sp_varu"].value]
    ARG = [re.sub(r'[\[\]\',]', '', str(a)) for a in ARG]
    # pd.DataFrame(ARG).to_csv(PARAM["path_Jparm"], index=False, header=None)

    try:
        # subprocess.check_output('%s %s' % 
        #     (PARAM["path_JL"], PARAM["path_JWAS"]), shell=True)

        # update matrix
        for item in ["sol", "X", "Z", "lhs", "rhs"]:
            dt = pd.read_csv("myapp/out/jwas_%s.csv" % item)
            if item in ["lhs", "rhs"]:
                # borrow fixed indicators from solution column
                dt["isFixed"] = SRC["sol"].data["isFixed"]
            SRC[item].data = dt.round(3)

            if item in ["sol", "rhs"]:
                temp_sol = """
                            <div style = "
                                background:<%=
                                    (function colorfromint() {
                                        if (isFixed == 1) {return('green')}
                                        else {return ('yellow')}}()) %>;
                                color     :<%=
                                    (function colorfromint() {
                                        if (isFixed == 1) {return('white')}
                                        else {return('black')}}()) %>;
                            "><%= value %></font></div>
                           """
                if item == "sol":
                    DT[item].columns = [TableColumn(field="terms",
                            formatter=HTMLTemplateFormatter(template=temp_sol)),
                                        TableColumn(field="effects",
                            formatter=HTMLTemplateFormatter(template=temp_sol))]
                elif item == "rhs":
                    DT[item].columns = [TableColumn(field=c,
                            formatter=HTMLTemplateFormatter(template=temp_sol))
                            for c in dt.columns[:-1]]
            elif item in ["X", "Z"]:
                PARAM["p%s" % item] = dt.shape[1] # could be reduncdent
                DT[item].columns = [
                    TableColumn(field=c,
                                formatter=HTMLTemplateFormatter(template="""
                                    <div style = "
                                        background:<%%= 
                                            (function colorfromint() {
                                                if (%s == 1) {return('yellow')} 
                                                else {return ('white')}}()) %%>;
                                        color     :<%%=
                                            (function colorfromint() {
                                                if (%s == 1) {return('black')} 
                                                else {return('black')}}()) %%>; 
                                    "><%%= value %%></font></div>
                                """ % (c, c))) for c in dt.columns]
            elif item == "lhs":
                DT[item].columns = [
                    TableColumn(field=c,
                                formatter=HTMLTemplateFormatter(template="""
                                    <div style = "
                                        background:<%=
                                            (function colorfromint() {
                                                if (isFixed == 1) {return('green')} 
                                                else {return ('yellow')}}()) %>;
                                        color     :<%=
                                            (function colorfromint() {
                                                if (isFixed == 1) {return('white')} 
                                                else {return('black')}}()) %>; 
                                    "><%= value %></font></div>
                                """)) for c in dt.columns[:PARAM["pX"]]] + [
                    TableColumn(field=c,
                                formatter=HTMLTemplateFormatter(template="""
                                    <div style = "
                                        background:<%=
                                            (function colorfromint() {
                                                if (isFixed == 1) {return('yellow')} 
                                                else {return ('green')}}()) %>;
                                        color     :<%=
                                            (function colorfromint() {
                                                if (isFixed == 1) {return('black')} 
                                                else {return('white')}}()) %>; 
                                    "><%= value %></font></div>
                                """)) for c in dt.columns[PARAM["pX"]:-1]]

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
PARAM["path_ped"] = "myapp/data/customized.ped"
PARAM["path_Jparm"] = "myapp/out/param.csv"
PARAM["demo 1"] = "myapp/data/demo_rosa.csv"
PARAM["demo 1 ped"] = "myapp/data/demo_rosa.ped"
PARAM["path_img_eq"] = "myapp/static/img_eq.png"
PARAM["path_img_X"] = "myapp/static/img_X.png"
PARAM["path_img_Z"] = "myapp/static/img_Z.png"
PARAM["empty_dt"] = pd.DataFrame(dict({"Empty": [0]}))
PARAM["pX"] = 0
PARAM["pZ"] = 0

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
                      editable=True,
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
GUI["mc_rdmns"] = MultiChoice(title="Random Effects (Non-Structured)", 
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
                          sizing_mode="fixed",
                          width=400, height=500)

# == Heat map == 
SRC["PED"] = ColumnDataSource(pd.DataFrame({"x":[0], "y":[0], "ped":[0]}))

colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2",
          "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
mapper = LinearColorMapper(
    # low=dt.rate.min(), high=dt.rate.max(),
    palette=colors)
GUI["img_ped"] = figure(plot_width=330, plot_height=330,
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
W = 350; H = 600
DT["lhs"] = DataTable(source=SRC["lhs"],
                      columns=[TableColumn(field="Empty Data")],
                      index_position=None, header_row=True,
                      width=W+250, height=H, editable=False, fit_columns=True,
                      align=("end", "end"))
DT["sol"] = DataTable(source=SRC["sol"],
                      columns=[TableColumn(field="Empty Data")],
                      index_position=None, header_row=True,
                      width=W-200, height=H, editable=False,
                      align=("end", "end"))
DT["rhs"] = DataTable(source=SRC["rhs"],
                      columns=[TableColumn(field="Empty Data")],
                      index_position=None, header_row=True,
                      width=W-300, height=H, editable=False,
                      align=("end", "end"))
GUI["img_sol"] = Div(text="""<img src=%s height=180>""" % PARAM["path_img_eq"],
                     sizing_mode="fixed")
GUI["spc_lhssol"] = Spacer(width=30, height=100)
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

# == Layout ==
GUI["sec_inputs"] = column(
                        row(column(Div(text='<h1 style>Data</h1>'), GUI["sec_data"]),
                            column(Div(text='<h1 style>Parameters</h1>'), GUI["sec_param"])),
                        GUI["bt_JWAS"]
                    )

layout = layout([[column(
            row(
                GUI["sec_inputs"],
                Spacer(width=30),
                column(Div(text='<h1 style>Design Matrix</h1>'), GUI["sec_design"], 
                       row(Div(text='<h1 style>Pedigree Heatmap</h1>'), Spacer(width=50), GUI["img_ped"]))
            ),
            Div(text='<h1 style>Solver</h1>'),
            GUI["sec_solver"]
        )]], sizing_mode='fixed')

