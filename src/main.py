from random import randint
from datetime import date
from bokeh.models import ColumnDataSource, TableColumn, DateFormatter, DataTable, PreText
from bokeh.models import Div, Select, Slider, RangeSlider, TextInput, Button, Label, LabelSet, HoverTool
from bokeh.layouts import column, row, layout
from bokeh.models.widgets import Tabs, Panel, TextInput
from bokeh.plotting import figure, output_file, show, curdoc
import numpy as np
import pandas as pd

# dataA = dict(dates=[date(2014, 3, i + 1) for i in range(10)],
#             downloads=[randint(0, 100) for i in range(10)],
#             identities=['id_' + str(x) for x in range(10)])
# dataB = dict(dates=["?" for i in range(10)],
#              downloads=["?" for i in range(10)],
#              identities=["?" for x in range(10)])

def solve_eq(mat_y, mat_X):
    mat_b = np.round(np.linalg.lstsq(mat_X, mat_y, rcond=None)[0], 2)
    pre_y = np.round(mat_X @ mat_b, 2)
    mat_e = np.round(mat_y - pre_y, 2)
    return mat_b, mat_e, pre_y

def get_pd_from_np(mat, col):
    """convert np matrix to valid pandas data frame"""
    try:
        n, m = np.array(mat).shape
    except Exception as e:
        # if mat is a vector
        m = 1
    return pd.DataFrame(mat, columns=["%s%d" % (col, i) for i in range(m)])

def get_mat_from_src(source):
    """extract numpy matrix from source"""
    ls_data = source.data
    return np.transpose([ls_data[k] for k in ls_data.keys()][1:])


PARAM = dict(n=5, m=3)

mat_y = np.random.randint(0, 100, PARAM["n"]).reshape((-1, 1))
mat_X = np.random.randint(0, 3, PARAM["n"]*PARAM["m"]).reshape((PARAM["n"], PARAM["m"]))
mat_b, mat_e, pre_y = solve_eq(mat_y, mat_X)

err = np.round(np.mean((pre_y[:, 0] - mat_y[:, 0])**2), 2)

sc_plot = ColumnDataSource(pd.DataFrame(
    dict({"pre": pre_y[:, 0],
          "obs": mat_y[:, 0],
          "err": "MSE: " + str(err)})))

sc_X = ColumnDataSource(get_pd_from_np(mat_X, "x"))
sc_y = ColumnDataSource(get_pd_from_np(mat_y, "y"))
sc_b = ColumnDataSource(get_pd_from_np(mat_b, "b"))
sc_e = ColumnDataSource(get_pd_from_np(mat_e, "e"))

H = 130
W = 200
dt_y = DataTable(source=sc_y,
            columns=[TableColumn(field="y0")],
            index_position=None, header_row=False,
            width=W - 150, height=H, editable=True)

dt_X = DataTable(source=sc_X,
            columns=[TableColumn(field="x%d" % d) for d in range(PARAM["m"])],
            index_position=None, header_row=False,
            width=W, height=H, editable=True)

dt_b = DataTable(source=sc_b,
            columns=[TableColumn(field="b0")],
            index_position=None, header_row=False,
            width=W - 150, height=H, editable=False)

dt_e = DataTable(source=sc_e,
            columns=[TableColumn(field="e0")],
            index_position=None, header_row=False,
            width=W - 150, height=H, editable=False)

def update_sol():
    mat_X = get_mat_from_src(sc_X)
    mat_y = get_mat_from_src(sc_y)
    mat_b, mat_e, pre_y = solve_eq(mat_y, mat_X)

    err = np.round(np.mean(abs(pre_y[:, 0] - mat_y[:, 0])), 2)

    sc_b.data = get_pd_from_np(mat_b, "b")
    sc_e.data = get_pd_from_np(mat_e, "e")

    sc_plot.data = pd.DataFrame(
        dict({"pre": pre_y[:, 0],
              "obs": mat_y[:, 0],
              "err": "MSE: " + str(err)}))

def change_val(attr, old, new):
    update_sol()

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


def update_y(attr, old, new):
    mat_y = np.random.randint(
        sli_y.value[0], sli_y.value[1], PARAM["n"]).reshape((-1, 1))
    sc_y.data = get_pd_from_np(mat_y, "y")
    update_sol()

def shuffle(event):
    mat_y = np.random.randint(
        sli_y.value[0], sli_y.value[1], PARAM["n"]).reshape((-1, 1))
    mat_X = np.random.randint(
        0, 3, PARAM["n"]*PARAM["m"]).reshape((PARAM["n"], PARAM["m"]))
    sc_X.data = get_pd_from_np(mat_X, "x")
    sc_y.data = get_pd_from_np(mat_y, "y")
    update_sol()


# # source.selected.on_change('indices', function_source)
sc_y.selected.on_change('indices', change_val)
sc_X.selected.on_change('indices', change_val)

txt_reg = PreText(text="""~""", align=("center", "center"))
txt_e = PreText(text="""+""", align=("center", "center"))

col_y = column(PreText(text="""Y (Editable)"""), dt_y)
col_X = column(PreText(text="""X (Editable)"""), dt_X)
col_b = column(PreText(text="""Beta"""), dt_b)
col_e = column(PreText(text="""Residual"""), dt_e)

row_eq = row(col_y, txt_reg, col_X, col_b,
             txt_e, col_e, align=("center", "center"))

size_fig = 350
p = figure(title="Fitted values by Fixed model", 
           width=size_fig, height=size_fig, 
           tools="",
           toolbar_location=None,
           align=("center", "center"))
p_circle = p.circle('obs', 'pre', source=sc_plot, fill_alpha=0.2, size=10)
p_line = p.line('obs', 'obs', source=sc_plot, color='red')
p.xaxis.axis_label = "Observed Y"
p.yaxis.axis_label = "Fitted Y"

p.add_layout(LabelSet(x=15, y=250, text="err",
        source=sc_plot, text_font_size='14px', text_color='black',
      x_units='screen', y_units='screen', background_fill_color='white'))

p.add_tools(HoverTool(
    tooltips=[
        ('ID', '$index'),
        ('obs', '@obs'),
        ('fit', '@pre')
    ],
    renderers=[p_circle],
    # display a tooltip whenever the cursor is vertically in line with a glyph
    mode='vline'
))

pn_main = column(row_eq, p)

#==== Controll

bt_shuffle = Button(label="Shuffle")
bt_shuffle.on_click(shuffle)

sli_y = RangeSlider(title="Phenotype range",
    start=0, end=100, value=(0, 100), step=1)
sli_y.on_change("value", update_y)


pn_controll = column(
    PreText(text="""Control Panel""", align=("center", "center")),
    sli_y,
    Slider(title="param 2", value=80, start=10, end=300, step=10),
    Slider(title="param 3", value=80, start=10, end=300, step=10),
    Select(title="param 4", value="A", options=["A", "B", "C"]),
    bt_shuffle,
    width=200,
    align=("center", "center"))

# ====


# curdoc().add_root(row(pn_controll, pn_main))


l1 = layout([[row(pn_controll, pn_main)]], sizing_mode='fixed')
l2 = layout([[]], sizing_mode='fixed')

tab1 = Panel(child=l1, title="Fixed Model")
tab2 = Panel(child=l2, title="Mixed Model")
tabs = Tabs(tabs=[tab1, tab2])


# # plot it
# fig = figure()
# fig.circle(x, y)
# fig.line(x, y_predicted, color='red', legend='y=' +
#          str(round(slope, 2))+'x+'+str(round(intercept, 2)))
# show(fig)

# output_file("index.html")
curdoc().add_root(tabs)

# show(tabs)
