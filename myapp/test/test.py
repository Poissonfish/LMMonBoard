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
# if(cola > colb){


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
