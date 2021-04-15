from .__main__ import *

H = 300
W = 200

DT["y"] = DataTable(source=SRC["y_s"],
                    columns=[TableColumn(field="obs")],
                    index_position=None, header_row=False,
                    width=W - 150, height=H, editable=False)
DT["X"] = DataTable(source=SRC["X"],
                    columns=[TableColumn(field="X%d" % d)
                             for d in range(ARG["m"])],
                    index_position=None, header_row=False,
                    width=W, height=H, editable=True)
DT["b"] = DataTable(source=SRC["eff_s"],
                    columns=[TableColumn(field="estimate")],
                    index_position=None, header_row=False,
                    width=W - 150, height=H, editable=False)
DT["e"] = DataTable(source=SRC["y_s"],
                    columns=[TableColumn(field="res")],
                    index_position=None, header_row=False,
                    width=W - 150, height=H, editable=False)

GUI["txt_reg"] = PreText(text="""~""", align=("center", "center"))
GUI["txt_e"] = PreText(text="""+""", align=("center", "center"))
GUI["col_y"] = column(PreText(text="""Y (Editable)"""), DT["y"])
GUI["col_X"] = column(PreText(text="""X (Editable)"""), DT["X"])
GUI["col_b"] = column(PreText(text="""Beta"""), DT["b"])
GUI["col_e"] = column(PreText(text="""Residual"""), DT["e"])
GUI["row_eq"] = row(GUI["col_y"], GUI["txt_reg"],
                    GUI["col_X"], GUI["col_b"],
                    GUI["txt_e"], GUI["col_e"],
                    align=("center", "center"))
