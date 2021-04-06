# bokeh serve --show myapp
from .src.lib import *
from .src.lmm.main import page as page_lmm
from .src.glm.main import page as page_glm

# main
app = Tabs(tabs=[
        Panel(child=page_lmm, title="Mixed Model"),
        Panel(child=page_glm, title="Fixed Model")])
# app = page_lmm
curdoc().add_root(app)
