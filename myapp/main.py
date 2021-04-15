# bokeh serve --show myapp
from .src.lib import *
from .src.lmm.main import page as page_lmm
from .src.about.main import page as page_about

# main
app = Tabs(tabs=[
        Panel(child=page_lmm,   title="Mixed Model"),
        Panel(child=page_about, title="About")])

# app = page_lmm
curdoc().add_root(
    column(
        Div(text="""<h1><center>LMMonBoard</center></h1>""",
            style={"font-size":"150%"},
            align="center"),
        app
    ))
curdoc().title = "MyApp Title"
