# Host server: bokeh serve --show myapp
#===== imports
from lib import *
from tab_glm import *
from tab_lmm import *

#=====layout
l_glm = get_GLM()
l_lmm = get_LMM()

#===== tabs and page
tab_glm = Panel(child=l_glm, title="Fixed Model")
tab_lmm = Panel(child=l_lmm, title="Mixed Model")
page = Tabs(tabs=[tab_lmm, tab_glm])
curdoc().add_root(page)




# Spacer(width=400, height=400, sizing_mode='scale_width'),



# # plot it
# fig = figure()
# fig.circle(x, y)
# fig.line(x, y_predicted, color='red', legend='y=' +
#          str(round(slope, 2))+'x+'+str(round(intercept, 2)))
# show(fig)

# output_file("index.html")

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
