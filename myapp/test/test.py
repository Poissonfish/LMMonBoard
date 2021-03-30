from bokeh.models.widgets import DataTable, DateFormatter, TableColumn, HTMLTemplateFormatter
from bokeh.models import ColumnDataSource
from bokeh.layouts import widgetbox
from bokeh.io import output_file, show
from random import randint
from bokeh.io import output_notebook, show
output_notebook()


output_file("data_table.html")

data = dict(
    cola=[3, 6, 7, 3, 7, 2, 3, 4, 5],
    colb=[4, 3, 1, 6, 5, 3, 4, 5, 1],
    z = [1, 0, 0, 0, 1, 0, 1, 0, 0]
)
source = ColumnDataSource(data)

template = """
            <div style="background:<%= 
                (function colorfromint(){
                    if(z==1){
                        return("green")}
                    }()) %>; 
                color: black"> 
            <%= value %>
            </div>
            """


template = """
<div style="background:<%= 
    (function colorfromint(){
        if(value == 1){
            return("blue")}
        else{return("red")}
        }()) %>; 
    color: white"> 
<%= value %></div>
"""
"""
<div style = "
    background:<%=
        (function colorfromint() {
            if (cola > colb) {
                return("green")
            } else {
                return ("white")
            }}()) %>;
    color     :<%=
        (function colorfromint() {
            if (cola > colb) {
                return('yellow')
            } else {
                return
            }}()) %>; 
    ">
    <%=value%>
    </font>
</div>
"""




formatter = HTMLTemplateFormatter(template=template)

columns = [TableColumn(field="cola", title="CL1", width=100),
           TableColumn(field='colb', title='CL2', formatter=formatter, width=100)]
data_table = DataTable(source=source,
                       columns=columns,
                       fit_columns=True,
                       selectable=True,
                       sortable=True,
                       width=400, height=400)

show(widgetbox(data_table))

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
