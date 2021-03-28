#===== imports
from lib import *

#===== runtime functions
def refresh_slider(attr, old, new):
    run(n=args["n"], n_dis=args["n_dis"], m=args["m"], nqtn=sli_nqtn.value,
        eff_mu=sli_effmu.value, eff_sd=sli_effsd.value, h2=sli_h2.value)


def refresh_button(event):
    run(n=args["n"], n_dis=args["n_dis"], m=args["m"], nqtn=sli_nqtn.value,
        eff_mu=sli_effmu.value, eff_sd=sli_effsd.value, h2=sli_h2.value)


def run(n, n_dis, m, nqtn, eff_mu, eff_sd, h2):
    # solve equation
    eff_background = get_glm_eff(
        size=n, nqtn=n, mu=eff_mu, sd=eff_sd)
    eff_samples = get_glm_eff(
        size=m, nqtn=nqtn, mu=eff_mu, sd=eff_sd)
    mat_X = get_glm_x(n=n, m=m)
    y_obs, y_m = get_glm_y(mat_X=mat_X, ls_eff=eff_samples, h2=h2)
    eff_estimated, residuals, y_bv, mse = solve_eq(
        mat_y=y_obs[:n_dis], mat_X=mat_X[:n_dis])

    # sources
    digits = 4
    sc_y.data = pd.DataFrame(
        dict({
            "p": y_obs,
            "g": y_m
        })
    ).round(digits)
    sc_y_s.data = pd.DataFrame(
        dict({
            "obs": y_obs[:args["n_dis"]],
            "bv": y_bv,
            "res": residuals,
            "err": str("MSE: %.3f" % mse)
        })
    ).round(digits)

    sc_eff.data = pd.DataFrame(
        dict({
            "eff": eff_background
        })
    ).round(digits)

    sc_eff_s.data = pd.DataFrame(
        dict({
            "sample": eff_samples,
            "estimate": eff_estimated
        })
    ).round(digits)

    sc_X.data = mat_to_pd(mat_X, col_prefix="X").round(digits)

    nbins = 50
    # hist for y
    hist_yp, edges_yp = np.histogram(sc_y.data["p"], bins=nbins, density=True)
    hist_yg, edges_yg = np.histogram(sc_y.data["g"], bins=nbins, density=True)
    sc_h_y.data = pd.DataFrame(
        dict({
            "yp_hist": hist_yp, "yp_edL": edges_yp[:-1], "yp_edR": edges_yp[1:],
            "yg_hist": hist_yg, "yg_edL": edges_yg[:-1], "yg_edR": edges_yg[1:]
        })
    )

    # hist for M
    hist_m, edges_m = np.histogram(
        sc_eff.data["eff"], bins=nbins, density=False)
    hist_ms, edges_ms = np.histogram(
        sc_eff_s.data["sample"], bins=nbins, density=True)
    sc_h_m.data = pd.DataFrame(
        dict({
            "m_hist": hist_m, "m_edL": edges_m[:-1], "m_edR": edges_m[1:],
            "ms_hist": hist_ms, "ms_edL": edges_ms[:-1], "ms_edR": edges_ms[1:]
        })
    )

def get_GLM():
    #===== setups
    args = dict(
        n=1000, n_dis=10, m=5, nqtn=3,
        eff_mu=0, eff_sd=1, h2=.8)

    #===== build runtime sources
    sc_y = ColumnDataSource()
    sc_y_s = ColumnDataSource()
    sc_eff = ColumnDataSource()
    sc_eff_s = ColumnDataSource()
    sc_X = ColumnDataSource()
    sc_h_y = ColumnDataSource()
    sc_h_m = ColumnDataSource()

    run(**args)

    #===== build displayed matrix
    H = 300
    W = 200
    dt_y = DataTable(source=sc_y_s,
                    columns=[TableColumn(field="obs")],
                    index_position=None, header_row=False,
                    width=W - 150, height=H, editable=False)

    dt_X = DataTable(source=sc_X,
                    columns=[TableColumn(field="X%d" % d)
                            for d in range(args["m"])],
                    index_position=None, header_row=False,
                    width=W, height=H, editable=True)

    dt_b = DataTable(source=sc_eff_s,
                    columns=[TableColumn(field="estimate")],
                    index_position=None, header_row=False,
                    width=W - 150, height=H, editable=False)

    dt_e = DataTable(source=sc_y_s,
                    columns=[TableColumn(field="res")],
                    index_position=None, header_row=False,
                    width=W - 150, height=H, editable=False)

    #===== GUI: equation
    txt_reg = PreText(text="""~""", align=("center", "center"))
    txt_e = PreText(text="""+""", align=("center", "center"))
    col_y = column(PreText(text="""Y (Editable)"""), dt_y)
    col_X = column(PreText(text="""X (Editable)"""), dt_X)
    col_b = column(PreText(text="""Beta"""), dt_b)
    col_e = column(PreText(text="""Residual"""), dt_e)
    row_eq = row(col_y, txt_reg, col_X, col_b,
                txt_e, col_e, align=("center", "center"))

    #===== GUI: fitted scatter plot
    size_fig = 350
    p = figure(title="Fitted values by Fixed model",
            width=size_fig, height=size_fig,
            tools="",
            toolbar_location=None,
            align=("center", "center"))
    p_circle = p.circle('obs', 'bv', source=sc_y_s, fill_alpha=0.2, size=10)
    p_line = p.line('obs', 'obs', source=sc_y_s, color='red')
    p.xaxis.axis_label = "Phenotype"
    p.yaxis.axis_label = "Breeding Values"
    p.add_layout(LabelSet(x=15, y=250, text="err",
                        source=sc_y_s, text_font_size='14px', text_color='black',
                        x_units='screen', y_units='screen', background_fill_color='white'))
    p.add_tools(HoverTool(
        tooltips=[
            ('ID', '$index'),
            ('obs', '@obs'),
            ('fit', '@bv')
        ],
        renderers=[p_circle],
        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode='vline'
    ))

    #===== GUI: histogram y
    h_y = figure(title="Distribution of Phenotypes and GEBVs",
                tools='', toolbar_location=None,
                width=800, height=300)
    h_y.quad(source=sc_h_y, legend="Phenotypes",
            top="yp_hist", bottom=0, left="yp_edL", right="yp_edR",
            fill_color="red", line_color="black", alpha=0.5)
    h_y.quad(source=sc_h_y, legend="Breeding Values",
            top="yg_hist", bottom=0, left="yg_edL", right="yg_edR",
            fill_color="navy", line_color="black", alpha=0.5)

    h_m = figure(title="Distribution of Marker Effects",
                tools='', toolbar_location=None,
                width=800, height=300)
    h_m.quad(source=sc_h_m, legend="Effect Distribution",
            top="m_hist", bottom=0, left="m_edL", right="m_edR",
            fill_color="red", line_color="black", alpha=0.5)
    h_m.quad(source=sc_h_m, legend="Sampled Effects",
            top="ms_hist", bottom=0, left="ms_edL", right="ms_edR",
            fill_color="navy", line_color="black", alpha=0.5)

    #===== GUI: config
    bt_shuffle = Button(label="Shuffle")
    sli_h2 = Slider(title="Heritability (h2)", value=.8,
                    start=.01, end=1, step=.01)
    sli_nqtn = Slider(title="Number of QTNs", value=3, start=1, end=5, step=1)
    sli_effmu = Slider(title="Mean of marker effects",
                    value=0, start=-3, end=3, step=.2)
    sli_effsd = Slider(title="S.D. of marker effects",
                    value=1, start=0, end=5, step=.2)

    pn_config = column(
        PreText(text="""Control Panel""", align=("center", "center")),
        sli_h2,
        sli_nqtn,
        sli_effmu,
        sli_effsd,
        bt_shuffle,
        p,
        width=400,
        align=("center", "start"))

    #===== interactive functions
    sc_X.selected.on_change('indices', refresh_slider)
    sli_h2.on_change("value", refresh_slider)
    sli_nqtn.on_change("value", refresh_slider)
    sli_effmu.on_change("value", refresh_slider)
    sli_effsd.on_change("value", refresh_slider)
    bt_shuffle.on_click(refresh_button)

    # return 
    pn_main = column(row_eq, h_y, h_m)
    l_glm = layout([[row(pn_config, pn_main)]], sizing_mode='fixed')

    return l_glm
