# Host server: bokeh serve --show myapp

# == imports ==
from lib import *
import tab_glm
import tab_lmm

# == tabs and page ==
tab_glm = Panel(child=tab_glm.layout, title="Fixed Model")
tab_lmm = Panel(child=tab_lmm.layout, title="Mixed Model")
page = Tabs(tabs=[tab_lmm, tab_glm])
curdoc().add_root(page)

# note
# space: &nbsp;