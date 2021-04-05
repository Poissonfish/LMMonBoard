from .main import *

GUI["bt_shuffle"] = Button(label="Shuffle")
GUI["sli_h2"] = Slider(title="Heritability (h2)",
                       value=.8, start=.01, end=1, step=.01)
GUI["sli_nqtn"] = Slider(title="Number of QTNs",
                         value=3, start=1, end=5, step=1)
GUI["sli_effmu"] = Slider(title="Mean of marker effects",
                          value=0, start=-3, end=3, step=.2)
GUI["sli_effsd"] = Slider(title="S.D. of marker effects",
                          value=1, start=0, end=5, step=.2)
