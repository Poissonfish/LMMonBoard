# == Imports ==
from lib import *

# import julia
# from julia import Julia
# Julia()

# julia.install()               # install PyCall.jl etc.
# from julia import Base        # short demo
# Base.sind(90)

# == Runtime functions ==
def run_JWAS_wrapper(event):
    GUI["bt_JWAS"].disabled = True
    print("JWAS is running", flush=True)
    curdoc().add_next_tick_callback(run_JWAS)

def run_JWAS():
    # output PED
    pd.DataFrame(SRC["ped"].data).iloc[:, 1:].to_csv(
        PARAM["path_cusped"], index=False)

    # take inputs
    ARG = [ PARAM[GUI["sel_data"].value],
            PARAM["path_cusped"],
            GUI["txt_eq"].value,
            GUI["mc_con"].value, GUI["mc_rdms"].value, GUI["mc_rdmns"].value,
            GUI["sp_vare"].value, GUI["sp_varu"].value]
    ARG = [re.sub(r'[\[\]\',]', '', str(a)) for a in ARG]
    # pd.DataFrame(ARG).to_csv(PARAM["path_Jparm"], index=False, header=None)

    try:
        # subprocess.check_output('%s %s' % 
        #     (PARAM["path_JL"], PARAM["path_JWAS"]), shell=True)

        # update matrix
        for item in ["X", "Z", "sol", "lhs", "rhs"]:
            print(item)
            DT[item] = pd.read_csv("myapp/out/jwas_%s.csv" % item).round(2)
            if item in ["X", "Z"]:
                dt_raw = wide_to_long(DT[item])
                dt_std = wide_to_long(
                    (DT[item] - DT[item].mean()) / DT[item].std())
                dt_raw["value_std"] = dt_std["value"]
                SRC[item].data = dt_raw["value_std"]
                specify_tickers(
                    HT[item], DT[item], xticks=DT[item].columns)
                try:
                    PARAM["p%s" % item] = DT[item].shape[1]
                except:
                    # when the dt with only one column
                    PARAM["p%s" % item] = 1
            elif item == "sol":
                hline = Span(location=PARAM["pX"] + PARAM["sep_offset"],
                             dimension='width', line_color='black',
                             line_dash='dashed', line_width=3)
                HT[item].add_layout(hline)
                SRC[item].data = wide_to_long(DT[item].iloc[:, 1])
                specify_tickers(HT[item], DT[item], yticks=DT[item].terms.values)
            elif item == "lhs":
                # add seperators
                vline = Span(location=PARAM["pX"] + PARAM["sep_offset"],
                             dimension='height', line_color='black',
                             line_dash='dashed', line_width=3)
                hline = Span(location=PARAM["pX"] + PARAM["sep_offset"],
                             dimension='width', line_color='black',
                             line_dash='dashed', line_width=3)
                HT[item].add_layout(vline)
                HT[item].add_layout(hline)
                # high_box = BoxAnnotation(bottom=180, fill_alpha=0.1, fill_color='red')
                # HT[item].add_layout(high_box)
                SRC[item].data = wide_to_long(DT[item])
                specify_tickers(
                    HT[item], DT[item], yticks=DT["sol"]["terms"].values)
            elif item == "rhs":
                # add seperators
                hline = Span(location=PARAM["pX"] + PARAM["sep_offset"],
                             dimension='width', line_color='black',
                             line_dash='dashed', line_width=3)
                HT[item].add_layout(hline)
                SRC[item].data = wide_to_long(DT[item])
                specify_tickers(
                    HT[item], DT[item], yticks=DT["sol"]["terms"].values)

        # update ped heatmap
        DT["PED"] = pd.read_csv(PARAM["path_A"], header=None).round(2)
        SRC["PED"].data = wide_to_long(DT["PED"])

    finally:
        print("JWAS Done")
        GUI["bt_JWAS"].disabled = False


def get_std_dt(dt):
    dt2 = dt.copy()
    np_dt = np.array(dt2)
    if np_dt.std() == 0:
        dt2.iloc[:, :] = 0
    else:
        dt2.iloc[:, :] = (np_dt - np_dt.mean()) / (np_dt.std())
    return dt2


def wide_to_long(dt_org):
    dt = dt_org.copy()
    try:
        n, m = dt.shape
        dt.columns = range(1, m + 1)
    except:
        # when the dt with only one column
        dt = dt.rename(1)
    dt_heat = pd.melt(dt.reset_index(), id_vars="index")
    dt_heat.columns = ["y", "x", "value"]
    dt_heat["x"].astype(int)
    dt_heat["y"] += 1
    return dt_heat


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
PARAM["path_cusped"] = "myapp/data/customized.ped"
PARAM["path_Jparm"] = "myapp/out/param.csv"
PARAM["path_A"] = "myapp/out/jwas_ped.csv"
PARAM["demo 1"] = "myapp/data/demo_rosa.csv"
PARAM["demo 1 ped"] = "myapp/data/demo_rosa.ped"
PARAM["path_img_eq"] = "myapp/static/img_eq.png"
PARAM["path_img_X"] = "myapp/static/img_X.png"
PARAM["path_img_Z"] = "myapp/static/img_Z.png"
PARAM["empty_dt"] = pd.DataFrame(dict({"Empty": [0]}))
PARAM["pX"] = 0
PARAM["pZ"] = 0
PARAM["sep_offset"] = .49
PARAM["size"] = "300%"
PARAM["heatmap_color"] = ["#2c7bb6", "#00a6ca", "#00ccbc", "#90eb9d",
               "#ffff8c", "#f9d057", "#f29e2e", "#e76818", "#d7191c"]

# ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2",
#  "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]

GUI = dict({})
SRC = dict({})
DT = dict({})
HT = dict({})
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
def make_heatmap(item, width, height, 
    show_x_axis=False, show_y_axis=False,
    show_legend=False, vertical_x=False):
    source = ColumnDataSource(pd.DataFrame({"x": [0], "y": [0], "tmp": [0]}))
    mapper = LinearColorMapper(
        # low=dt.rate.min(), high=dt.rate.max(), 
        palette=PARAM["heatmap_color"])
    fig = figure(plot_width=width, plot_height=height,
                    align=("center"),
                    y_axis_label="Effects",
                    #    x_range=list(dt.index),
                    #    y_range=list(reversed(np.unique(dt_heat.y))),
                    toolbar_location=None, tools="", x_axis_location="above")
    fig.y_range.flipped = True
    fig.rect(x="x", y="y", width=1, height=1, source=source, 
             line_color=None, fill_color=transform('value', mapper))
    fig.add_layout(LabelSet(x='x', y='y', text='value',
                                text_font_size="12px",
                                text_align="center",
                                source=source))
    # remove padding
    fig.min_border = 0
    fig.x_range.range_padding = 0
    fig.y_range.range_padding = 0

    if not show_x_axis:
        fig.xaxis.visible = False
    if not show_y_axis:
        fig.yaxis.visible = False
    if vertical_x:
        fig.xaxis.major_label_orientation = "vertical"
    if show_legend:
        color_bar = ColorBar(color_mapper=mapper)
        fig.add_layout(color_bar, 'right')

    return source, fig

def specify_tickers(fig, dt, xticks=None, yticks=None):
    if xticks is not None:
        ticks_int = range(1, dt.shape[1] + 1)
        fig.xaxis.ticker = list(ticks_int)
        dt_key = pd.DataFrame({
            "k": ticks_int,
            "v": xticks})
        fig.xaxis.major_label_overrides = dict(
            [(key, value) for key, value in zip(dt_key.k, dt_key.v)])
    if yticks is not None:
        ticks_int = range(1, dt.shape[0] + 1)
        fig.yaxis.ticker = list(ticks_int)
        dt_key = pd.DataFrame({
            "k": ticks_int,
            "v": yticks})
        fig.yaxis.major_label_overrides = dict(
            [(key, value) for key, value in zip(dt_key.k, dt_key.v)])


SRC["PED"], HT["PED"] = make_heatmap("PED", 300, 300, 
    show_x_axis=True, show_y_axis=True)
SRC["X"], HT["X"] = make_heatmap(
    "X", 300, 300, show_x_axis=True, vertical_x=True)
SRC["Z"], HT["Z"] = make_heatmap(
    "Z", 600, 300, show_x_axis=True, vertical_x=True)
SRC["lhs"], HT["lhs"] = make_heatmap("lhs", 1000, 1000, show_y_axis=True)
SRC["rhs"], HT["rhs"] = make_heatmap("rhs", 200, 1000, show_y_axis=True)
SRC["sol"], HT["sol"] = make_heatmap("sol", 200, 1000, show_y_axis=True)

# == Design Matrix ==
GUI["img_X"] = Div(text="""<img src=%s height=30>""" % PARAM["path_img_X"],
                   style={"width": "60%"},
                   height=60, sizing_mode="fixed", align=("center"))
GUI["img_Z"] = Div(text="""<img src=%s height=30>""" % PARAM["path_img_Z"],
                   style={"width": "60%"},
                   height=60, sizing_mode="fixed", align=("center"))

GUI["sec_design"] = row(GUI["img_X"], HT["X"], GUI["img_Z"], HT["Z"])

# == Solver ==
GUI["img_sol"] = Div(text="""<img src=%s height=180>""" % PARAM["path_img_eq"],
                     sizing_mode="fixed")
GUI["spc_lhssol"] = Spacer(width=30, height=100)
GUI["spc_solrhs"] = Spacer(width=70, height=100)
GUI["row_sol"] = row(
            HT["lhs"],
            GUI["spc_lhssol"], 
            HT["sol"],
            GUI["spc_solrhs"],
            HT["rhs"])
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
                column(Div(text='<h1 style>Incidence Matrix</h1>'), GUI["sec_design"], 
                       row(Div(text='<h1 style>Relationship Matrix</h1>'), Spacer(width=50), HT["PED"]))
            ),
            Div(text='<h1 style>Solver</h1>'),
            GUI["sec_solver"]
        )]], sizing_mode='fixed')


# dt = pd.read_csv("out/jwas_X.csv").round(1)
# SRC["X"].data = wide_to_long(dt)
# specify_tickers(
#     HT[item], dt, xticks=dt.columns)


# if xticks is not None:
#     ticks_int = range(1, dt.shape[1] + 1)
#     fig.xaxis.ticker = list(ticks_int)
#     dt_key = pd.DataFrame({
#         "k": ticks_int,
#         "v": xticks})
#     fig.xaxis.major_label_overrides = dict(
#         [(key, value) for key, value in zip(dt_key.k, dt_key.v)])
# if yticks is not None:
#     ticks_int = range(1, dt.shape[0] + 1)
#     fig.yaxis.ticker = list(ticks_int)
#     dt_key = pd.DataFrame({
#         "k": ticks_int,
#         "v": yticks})
#     fig.yaxis.major_label_overrides = dict(
#         [(key, value) for key, value in zip(dt_key.k, dt_key.v)])

