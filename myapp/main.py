# Host server: bokeh serve --show myapp
#===== imports
from lib import *

#===== runtime functions
def refresh_slider(attr, old, new):
    run(n=args["n"], n_dis=args["n_dis"], m=args["m"], nqtn=sli_nqtn.value,
        eff_mu=sli_effmu.value, eff_sd=sli_effsd.value, h2=sli_h2.value)

def refresh_button(event):
    run(n=args["n"], n_dis=args["n_dis"], m=args["m"], nqtn=sli_nqtn.value,
        eff_mu=sli_effmu.value, eff_sd=sli_effsd.value, h2=sli_h2.value)

def run(n, n_dis, m, nqtn, eff_mu, eff_sd, h2):
    # solve equation
    eff_background = get_glm_eff(
        size=n, nqtn=n, mu=eff_mu, sd=eff_sd)
    eff_samples = get_glm_eff(
        size=m, nqtn=nqtn, mu=eff_mu, sd=eff_sd)
    mat_X = get_glm_x(n=n, m=m)
    y_obs, y_m = get_glm_y(mat_X=mat_X, ls_eff=eff_samples, h2=h2)
    eff_estimated, residuals, y_bv, mse = solve_eq(
        mat_y=y_obs[:n_dis], mat_X=mat_X[:n_dis])

    # sources
    digits=4
    sc_y.data = pd.DataFrame(
                    dict({
                        "p": y_obs,
                        "g": y_m
                    })
                ).round(digits)
    sc_y_s.data = pd.DataFrame(
                        dict({
                            "obs": y_obs[:args["n_dis"]],
                            "bv": y_bv,
                            "res": residuals,
                            "err": str("MSE: %.3f" % mse)
                        })
                    ).round(digits)

    sc_eff.data = pd.DataFrame(
                        dict({
                            "eff": eff_background
                        })
                    ).round(digits)

    sc_eff_s.data = pd.DataFrame(
                    dict({
                        "sample": eff_samples,
                        "estimate": eff_estimated
                    })
                    ).round(digits)

    sc_X.data = mat_to_pd(mat_X, col_prefix="X").round(digits)

    nbins=50
    # hist for y
    hist_yp, edges_yp = np.histogram(sc_y.data["p"], bins=nbins, density=True)
    hist_yg, edges_yg = np.histogram(sc_y.data["g"], bins=nbins, density=True)
    sc_h_y.data = pd.DataFrame(
        dict({
            "yp_hist": hist_yp, "yp_edL": edges_yp[:-1], "yp_edR": edges_yp[1:],
            "yg_hist": hist_yg, "yg_edL": edges_yg[:-1], "yg_edR": edges_yg[1:]
        })
    )

    # hist for M
    hist_m, edges_m = np.histogram(sc_eff.data["eff"], bins=nbins, density=False)
    hist_ms, edges_ms = np.histogram(sc_eff_s.data["sample"], bins=nbins, density=True)
    sc_h_m.data = pd.DataFrame(
        dict({
            "m_hist": hist_m, "m_edL": edges_m[:-1], "m_edR": edges_m[1:],
            "ms_hist": hist_ms, "ms_edL": edges_ms[:-1], "ms_edR": edges_ms[1:]
        })
    )


#===== setups
args = dict(
        n=1000, n_dis=10, m=5, nqtn=3,
        eff_mu=0, eff_sd=1, h2=.8)

#===== build runtime sources
sc_y = ColumnDataSource()
sc_y_s = ColumnDataSource()
sc_eff = ColumnDataSource()
sc_eff_s = ColumnDataSource()
sc_X = ColumnDataSource()
sc_h_y = ColumnDataSource()
sc_h_m = ColumnDataSource()

run(**args)

#===== build displayed matrix
H = 300
W = 200
dt_y = DataTable(source=sc_y_s,
            columns=[TableColumn(field="obs")],
            index_position=None, header_row=False,
            width=W - 150, height=H, editable=False)

dt_X = DataTable(source=sc_X,
            columns=[TableColumn(field="X%d" % d) for d in range(args["m"])],
            index_position=None, header_row=False,
            width=W, height=H, editable=True)

dt_b = DataTable(source=sc_eff_s,
            columns=[TableColumn(field="estimate")],
            index_position=None, header_row=False,
            width=W - 150, height=H, editable=False)

dt_e = DataTable(source=sc_y_s,
            columns=[TableColumn(field="res")],
            index_position=None, header_row=False,
            width=W - 150, height=H, editable=False)

#===== GUI: equation
txt_reg = PreText(text="""~""", align=("center", "center"))
txt_e = PreText(text="""+""", align=("center", "center"))
col_y = column(PreText(text="""Y (Editable)"""), dt_y)
col_X = column(PreText(text="""X (Editable)"""), dt_X)
col_b = column(PreText(text="""Beta"""), dt_b)
col_e = column(PreText(text="""Residual"""), dt_e)
row_eq = row(col_y, txt_reg, col_X, col_b,
             txt_e, col_e, align=("center", "center"))

#===== GUI: fitted scatter plot
size_fig = 350
p = figure(title="Fitted values by Fixed model", 
           width=size_fig, height=size_fig, 
           tools="",
           toolbar_location=None,
           align=("center", "center"))
p_circle = p.circle('obs', 'bv', source=sc_y_s, fill_alpha=0.2, size=10)
p_line = p.line('obs', 'obs', source=sc_y_s, color='red')
p.xaxis.axis_label = "Phenotype"
p.yaxis.axis_label = "Breeding Values"
p.add_layout(LabelSet(x=15, y=250, text="err",
        source=sc_y_s, text_font_size='14px', text_color='black',
        x_units='screen', y_units='screen', background_fill_color='white'))
p.add_tools(HoverTool(
    tooltips=[
        ('ID', '$index'),
        ('obs', '@obs'),
        ('fit', '@bv')
    ],
    renderers=[p_circle],
    # display a tooltip whenever the cursor is vertically in line with a glyph
    mode='vline'
))

#===== GUI: histogram y
h_y = figure(title="Distribution of Phenotypes and GEBVs", 
             tools='', toolbar_location=None,
             width=800, height=300)
h_y.quad(source=sc_h_y, legend="Phenotypes",
        top="yp_hist", bottom=0, left="yp_edL", right="yp_edR",
        fill_color="red", line_color="black", alpha=0.5)
h_y.quad(source=sc_h_y, legend="Breeding Values",
        top="yg_hist", bottom=0, left="yg_edL", right="yg_edR",
       fill_color="navy", line_color="black", alpha=0.5)

h_m = figure(title="Distribution of Marker Effects", 
             tools='', toolbar_location=None,
             width=800, height=300)
h_m.quad(source=sc_h_m, legend="Effect Distribution",
        top="m_hist", bottom=0, left="m_edL", right="m_edR",
        fill_color="red", line_color="black", alpha=0.5)
h_m.quad(source=sc_h_m, legend="Sampled Effects",
        top="ms_hist", bottom=0, left="ms_edL", right="ms_edR",
       fill_color="navy", line_color="black", alpha=0.5)

# h.line(x, pdf, line_color="#ff8888", line_width=4,
#         alpha=0.7, legend_label="PDF")
# h.line(x, cdf, line_color="orange", line_width=2,
#         alpha=0.7, legend_label="CDF")


#===== GUI: config
bt_shuffle = Button(label="Shuffle")
sli_h2 = Slider(title="Heritability (h2)", value=.8, start=.01, end=1, step=.01)
sli_nqtn = Slider(title="Number of QTNs", value=3, start=1, end=5, step=1)
sli_effmu = Slider(title="Mean of marker effects", value=0, start=-3, end=3, step=.2)
sli_effsd = Slider(title="S.D. of marker effects", value=1, start=0, end=5, step=.2)

pn_config = column(
    PreText(text="""Control Panel""", align=("center", "center")),
    sli_h2,
    sli_nqtn,
    sli_effmu,
    sli_effsd,
    bt_shuffle,
    p,
    width=400,
    align=("center", "start"))

#===== interactive functions
sc_X.selected.on_change('indices', refresh_slider)
sli_h2.on_change("value", refresh_slider)
sli_nqtn.on_change("value", refresh_slider)
sli_effmu.on_change("value", refresh_slider)
sli_effsd.on_change("value", refresh_slider)
bt_shuffle.on_click(refresh_button)


#===#===#======#===#===# LMM #===#===#======#===#===#
# space: &nbsp;
# arg_file, arg_eq, arg_cov, arg_random = ARGS
os.chdir("myapp")
data = pd.read_csv("res/demo_s.csv")
data = pd.read_csv("res/demo_rosa.csv")

# lmm_obj = dict({
#     "y":   pd.read_csv("out/jwas_y.csv"),
#     "id":  pd.read_csv("out/jwas_names.csv"),
#     "inc": pd.read_csv("out/jwas_designMat.csv"),
#     "lhs": pd.read_csv("out/jwas_LHS.csv"),
#     "rhs": pd.read_csv("out/jwas_RHS.csv")
# })

size = "300%"
# Equation (Top)
# div_eq_top = Div(text="<pre> β</pre>",
#                  style={'font-size': size, "height": "30%", 'color': 'blue'})
# div_eq_bot = Div(text="<pre> u</pre>",
#                  style={'font-size': size, "height": "70%", 'color': 'blue'})
# col_eq = column(div_eq_top, div_eq_bot)

# row_lmmEqTp = row(
#     Div(text="<pre>y = [X  Z][</pre>",
#         style={'font-size': size, 
#                "width": "90%", 'color': 'blue'},
#         align=("end", "center")),
#     col_eq,
#     Div(text="<pre>]</pre>",
#         style={'font-size': size, 
#                "width": "100%", 'color': 'blue'},
#         align=("end", "center"))
# )

# Matrix (Top)
sc_X_lmm = ColumnDataSource()
sc_Z_lmm = ColumnDataSource()
# sc_X_lmm.data = mat_to_pd(lmm_obj["inc"].iloc[:, 1], col_prefix="X")
# sc_Z_lmm.data = mat_to_pd(lmm_obj["inc"].iloc[:, 2:], col_prefix="Z")

dt_X_lmm = DataTable(source=sc_X_lmm,
                   columns=[TableColumn(field="X%d" % d)
                            for d in range(len(sc_X_lmm.data) - 1)],
                     index_position=None, header_row=True,
                   width=100, height=250, editable=False,
                   align=("center", "end"))

dt_Z_lmm = DataTable(source=sc_Z_lmm,
                   columns=[TableColumn(field="Z%d" % d)
                            for d in range(len(sc_Z_lmm.data) - 1)],
                     index_position=None, header_row=True,
                   width=300, height=250, editable=False,
                   align=("center", "center"))

row_lmmEqTp = row(
    Div(text="<pre>X=</pre>",
        style={'font-size': size,
               "width": "60%", 'color': 'blue'},
        align=("end", "center")),
    dt_X_lmm,
    Div(text="<pre>Z=</pre>",
        style={'font-size': size,
               "width": "60%", 'color': 'blue'},
        align=("end", "center")),
    dt_Z_lmm
)

# Equation (Bottom)
div_lhs_top = Div(text="<pre> X<sup>T</sup>X X<sup>T</sup>Z </pre>",
                  style={'font-size': size, "height":"30%", 'color': 'blue'})
div_lhs_bot = Div(text="<pre> Z<sup>T</sup>X Z<sup>T</sup>Z+G<sup>-1</sup></pre>",
                  style={'font-size': size, "height":"70%", 'color': 'blue'})

div_sol_top = Div(text="<pre>  β<sup>^</sup></pre>",
                  style={'font-size': size, "height": "30%", 'color': 'blue'})
div_sol_bot = Div(text="<pre>  u<sup>^</sup></pre>",
                  style={'font-size': size, "height": "70%", 'color': 'blue'})

div_rhs_top = Div(text="<pre> X<sup>T</sup>y</pre>",
                  style={'font-size': size, "height": "30%", 'color': 'blue'})
div_rhs_bot = Div(text="<pre> Z<sup>T</sup>y</pre>",
                  style={'font-size': size, "height": "70%", 'color': 'blue'})

col_lhs = column(div_lhs_top, div_lhs_bot)
col_sol = column(div_sol_top, div_sol_bot)
col_rhs = column(div_rhs_top, div_rhs_bot)
row_lmmEqBt = row(
    Div(text="<pre>[</pre>",
        style={'font-size': "400%",
               "width": "20%", 'color': 'blue'},
        align=("end", "center")),
    col_lhs,
    Div(text="<pre>][</pre>",
        style={'font-size': "400%",
               "width": "20%", 'color': 'blue'},
        align=("end", "center")),
    col_sol,
    Div(text="<pre>]</pre>",
        style={'font-size': "400%",
               "width": "20%", 'color': 'blue'},
        align=("start", "center")),
    Div(text="<pre> =</pre>",
        style={'font-size': "400%", 'color': 'blue'},
        align=("end", "end")),
    Div(text="<pre>[</pre>",
        style={'font-size': "400%",
               "width": "20%", 'color': 'blue'},
        align=("end", "center")),
    col_rhs,
    Div(text="<pre>]</pre>",
        style={'font-size': "400%",
               "width": "20%", 'color': 'blue'},
        align=("start", "center")),
)

# Matrix (Bottom)
sc_lhs = ColumnDataSource()
sc_rhs = ColumnDataSource()
# sc_lhs.data = mat_to_pd(lmm_obj["lhs"], col_prefix="L").round(3)
# sc_rhs.data = mat_to_pd(lmm_obj["rhs"], col_prefix="R").round(3)

W = 250
H = 300
dt_lhs = DataTable(source=sc_lhs,
            # columns=[TableColumn(field="L%d" % d) for d in range(len(sc_lhs.data) - 1)],
                   index_position=None, header_row=True,
            width=W+85, height=H, editable=False,
            align=("end", "end"))
dt_rhs = DataTable(source=sc_rhs,
            # columns=[TableColumn(field="R%d" % d) for d in range(len(sc_rhs.data) - 1)],
                   index_position=None, header_row=True,
            width=W-100, height=H, editable=False)
row_lmmMatBt = row(dt_lhs, 
                   Spacer(width=200, height=100),
                   dt_rhs)

# Input matrix
sc_input = ColumnDataSource(data)
dt_input = DataTable(source=sc_input, 
            columns=[TableColumn(field=str(s)) for s in data.columns],
            height=200)

# Control
input_eq = TextInput(value="",
                     title="Equation: ")
ls_options = []

# (model, "ID dam",

# drop_cov = Select(title="Covariates", value="x1", 
#                   options=list(map(str, data.columns)))
# drop_rdm = Select(title="Random Effect", value="x2",
#                   options=list(map(str, data.columns)))

drop_cov = MultiChoice(title="Covariates", value=[],
                  options=ls_options)
drop_rdm = MultiChoice(title="Random Effect", value=[],
                  options=ls_options)
bt_JWAS = Button(label="Run JWAS",
                 button_type="success")

row_control = row(drop_cov, drop_rdm)
lmm_control = column(dt_input, input_eq, row_control, bt_JWAS)

# control function
def run_JWAS_wrapper(event):
    bt_JWAS.disabled = True
    print("JWAS is running", flush=True)
    curdoc().add_next_tick_callback(run_JWAS)
    
def run_JWAS():
    # take args and run JWAS
    # PATH_JL = "/Applications/Julia-1.5.app/Contents/Resources/julia/bin/julia"
    PATH_JL = "/usr/local/bin/julia"
    # args_file = "myapp/res/demo_s.csv"
    args_file = "myapp/res/demo_Rosa.csv"
    args_eq = input_eq.value
    args_cov = " ".join(drop_cov.value)
    args_rdm = " ".join(drop_rdm.value)

    try:
        subprocess.check_output('%s myapp/jwas.jl "%s" "%s" "%s" "%s"' %
                    (PATH_JL, args_file, args_eq, args_cov, args_rdm),
                    shell=True)

        # update matrix
        lmm_obj = dict({
            "y":   pd.read_csv("myapp/out/jwas_y.csv"),
            "id":  pd.read_csv("myapp/out/jwas_names.csv"),
            "inc": pd.read_csv("myapp/out/jwas_designMat.csv"),
            "lhs": pd.read_csv("myapp/out/jwas_LHS.csv"),
            "rhs": pd.read_csv("myapp/out/jwas_RHS.csv")
        })
        idx_cov = [args_cov in s for s in lmm_obj["id"].values[:, 0]]
        idx_rdm = [args_rdm in s for s in lmm_obj["id"].values[:, 0]]

        sc_X_lmm.data = mat_to_pd(lmm_obj["inc"].loc[:, idx_cov], "X")
        sc_Z_lmm.data = mat_to_pd(lmm_obj["inc"].loc[:, idx_rdm], "Z")
        sc_lhs.data = mat_to_pd(lmm_obj["lhs"], "L").round(3)
        sc_rhs.data = mat_to_pd(lmm_obj["rhs"], "R").round(3)

        dt_X_lmm.columns = [TableColumn(field="X%d" % d)
                            for d in range(len(sc_X_lmm.data) - 1)]
        dt_Z_lmm.columns = [TableColumn(field="Z%d" % d)
                            for d in range(len(sc_Z_lmm.data) - 1)]
        dt_lhs.columns = [TableColumn(field="L%d" % d)
                        for d in range(len(sc_lhs.data) - 1)]
        dt_rhs.columns = [TableColumn(field="R%d" % d)
                        for d in range(len(sc_rhs.data) - 1)]
        # sleep(3)
        print("JWAS Done")
    finally:
        bt_JWAS.disabled = False


def update_terms(attr, old, new):
    ls_options = re.split("[^0-9a-zA-Z*]+", re.sub(".*= ", "", input_eq.value))
    drop_cov.options = ls_options
    drop_cov.value = [ls_options[0]]
    drop_rdm.options = ls_options
    drop_rdm.value = [ls_options[1]]
    # display the remaining


input_eq.on_change("value", update_terms)
bt_JWAS.on_click(run_JWAS_wrapper)

#===== overall layout
pn_main = column(row_eq, h_y, h_m)
l_glm = layout([[row(pn_config, pn_main)]], sizing_mode='fixed')
l_lmm = layout([[column(lmm_control, row_lmmEqTp, row_lmmEqBt, row_lmmMatBt)]],
               sizing_mode='fixed')


#===== tabs and page
tab_glm = Panel(child=l_glm, title="Fixed Model")
tab_lmm = Panel(child=l_lmm, title="Mixed Model")
# page = Tabs(tabs=[tab_glm, tab_lmm])
page = Tabs(tabs=[tab_lmm, tab_glm])

# Spacer(width=400, height=400, sizing_mode='scale_width'),



# # plot it
# fig = figure()
# fig.circle(x, y)
# fig.line(x, y_predicted, color='red', legend='y=' +
#          str(round(slope, 2))+'x+'+str(round(intercept, 2)))
# show(fig)

# output_file("index.html")
curdoc().add_root(page)

# show(page)


#===== Reference
# sli_nqtn = RangeSlider(title="Number of QTN",
#     start=0, end=5, value=(0, 100), step=1)

# try:
#     selected_index = source.selected.indices[0]
#     table_row.value = str(selected_index)
#     table_cell_column_1.value = str(source.data["dates"][selected_index])
#     table_cell_column_2.value = str(source.data["downloads"][selected_index])
# except IndexError:
#     pass

# if source.data["dates"][0]!="?":
#     source.data = dataB
# else:
#     source.data = dataA
