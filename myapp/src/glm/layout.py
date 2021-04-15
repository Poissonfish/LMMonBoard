from ..lib import *
from .__main__ import *

# left panel: configuration
pn_config = column(
    PreText(text="""Control Panel""", align=("center", "center")),
    GUI["sli_h2"],
    GUI["sli_nqtn"],
    GUI["sli_effmu"],
    GUI["sli_effsd"],
    GUI["bt_shuffle"],
    GUI["fig_scatterFit"],
    width=400, align=("center", "start"))

# right panel: results
pn_main = column(GUI["row_eq"], GUI["fig_hisGEBV"], GUI["fig_hisMarker"])

# assemble to page
page = layout([[row(pn_config, pn_main)]], sizing_mode='fixed')
