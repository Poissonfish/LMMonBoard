from ..lib import *
from . import path as PATH

def set_control(GUI, SRC, DT, LO):
    # load data and display
    H=270
    W=380
    SRC["data"] = ColumnDataSource()
    DT["data"] = DataTable(source=SRC["data"],
                        columns=[],
                        editable=True,
                        height=H, width=W)
    SRC["ped"] = ColumnDataSource()
    DT["ped"] = DataTable(source=SRC["ped"],
                        columns=[],
                        editable=True,
                        height=H, width=W - 110)

    GUI["sel_data"] = Select(title="",
                             options=PATH.DATA.get_names())


    GUI["txt_eq"] = TextInput(title="Model Equation")

    LO["data"] = column(
        Div(text='<h3>Data</h3>', max_height=40),
        GUI["sel_data"],
        GUI["txt_eq"],
        row(column(PreText(text="Trial Records"), DT["data"]),
            column(PreText(text="Pedigree"), DT["ped"])))

    # continuous vs categorical
    GUI["mc_con"] = MultiChoice(
        title="Continuous",
        delete_button=False,
        height=120)

    GUI["mc_cat"] = MultiChoice(
        title="Categorical",
        delete_button=False,
        height=120) # actually we only need mc_con height to be set

    # fixed, random, random iid
    h = 105
    GUI["mc_fix"] = MultiChoice(
        title="Fixed Effects",
        delete_button=False,
        height=h)
    GUI["mc_rdms"] = MultiChoice(
        title="Random Effects (Correlated)",
        delete_button=False,
        height=h)
    GUI["mc_rdmns"] = MultiChoice(
        title="Random Effects (i.i.d.)",
        delete_button=False,
        height=h - 5)

    # variance components
    h = 110
    w = 180
    GUI["sp_vare"] = Spinner(title="Residuals (i.i.d.)",
                            low=0.1, high=10, value=4,
                            height=50,
                            step=.01)


    SRC["Gres"] =  ColumnDataSource()
    DT["Gres"] = DataTable(source=SRC["Gres"],
                            columns=[],
                            editable=True,
                            width=w,
                            height=h-60,
                            index_position=None
                    )

    SRC["Gstr"] =  ColumnDataSource()
    DT["Gstr"] = DataTable(source=SRC["Gstr"],
                            columns=[],
                            editable=True,
                            width=w,
                            height=h,
                            index_position=None
                    )

    SRC["Giid"] =  ColumnDataSource()
    DT["Giid"] = DataTable(source=SRC["Giid"],
                            columns=[],
                            editable=True,
                            width=w,
                            height=h,
                            index_position=None
                    )

    # JWAS button
    GUI["bt_JWAS"] = Button(
        # background="#d8773e",
        label="Update LMM Results", button_type="success")

    # JWAS Console
    # GUI["logger"] = Div(text=""" """,
    #                     style={'overflow-y': 'scroll', 'height': '50px'},
    #                     width=2000, height=300)
    GUI["logger"] = Paragraph(text=""" """,
                        width=1300, height=300)
    LO["logger"] = row(GUI["bt_JWAS"], GUI["logger"])

    # layout
    # LO["eq"] = Column(
    #     Div(text='<h3>Model Equation</h3>', max_height=40),
    #     GUI["txt_eq"]
    # )

    LO["catcon"] = column(
        Div(text='<h3>Continuous / Categorical Variables</h3>', max_height=150),
        GUI["mc_con"],
        GUI["mc_cat"],
        sizing_mode="stretch_width",
        max_width=300)

    LO["fixrdm"] = column(
        Div(text='<h3>Fixed / Random Effects</h3>', max_height=70),
        GUI["mc_fix"],
        GUI["mc_rdms"],
        GUI["mc_rdmns"],
        sizing_mode="stretch_width",
        max_width=300)

    LO["var"] = column(
        Div(text='<h3>Variance Components</h3>', max_height=70),
        PreText(text="Residuals (i.i.d.)"),
        DT["Gres"],
        PreText(text="Random Effects (Correlated)"),
        DT["Gstr"],
        # Spacer(height=50),
        PreText(text="Random Effects (i.i.d.)"),
        DT["Giid"],
        sizing_mode="stretch_width",
        max_width=300)

