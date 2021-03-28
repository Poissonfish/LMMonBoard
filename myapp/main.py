# Host server: bokeh serve --show myapp
#===== imports
from lib import *
from tab_glm import *

#===#===#======#===#===# LMM #===#===#======#===#===#
# space: &nbsp;
# arg_file, arg_eq, arg_cov, arg_random = ARGS
os.chdir("myapp")
data = pd.read_csv("data/demo_s.csv")
data = pd.read_csv("data/demo_rosa.csv")

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
l_glm = get_GLM()
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
