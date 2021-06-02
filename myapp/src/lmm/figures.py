from ..lib import *
from .__main__ import *

def make_heatmap(width, height,
                 show_x_axis=False, show_y_axis=False,
                 show_legend=False, vertical_x=False):
    # instantiate source
    source = ColumnDataSource(
                pd.DataFrame({"x": [0], "y": [0], "tmp": [0]}))

    # color mapper
    anbrew = ['#577c8a', '#587c8a', '#597c89', '#5a7c89', '#5b7c89', '#5c7c88', '#5d7c88', '#5d7c88', '#5e7c87', '#5f7c87', '#607c87', '#617c86', '#627c86', '#637c86', '#637c86', '#647c85', '#657c85', '#667c85', '#677c84', '#677c84', '#687c84', '#697c83', '#6a7c83', '#6b7c83', '#6b7c82', '#6c7c82', '#6d7c82', '#6e7c81', '#6e7c81', '#6f7c81', '#707c80', '#707c80', '#717c80', '#727c7f', '#737c7f', '#737c7f', '#747c7e', '#757c7e', '#757c7e', '#767c7d', '#777c7d', '#787c7d', '#787c7d', '#797c7c', '#7a7c7c', '#7a7c7c', '#7b7c7b', '#7c7c7b', '#7c7c7b', '#7d7c7a', '#7e7c7a', '#7e7c7a', '#7f7c79', '#807c79', '#807c79', '#817c78', '#817c78', '#827c78', '#837c77', '#837c77', '#847c77', '#857c76', '#857c76', '#867c76', '#867c75', '#877c75', '#887c75', '#887c74', '#897c74', '#8a7c74', '#8a7c73', '#8b7c73', '#8b7c73', '#8c7c72', '#8c7c72', '#8d7c72', '#8e7c72', '#8e7c71', '#8f7c71', '#8f7c71', '#907c70', '#917c70', '#917c70', '#927c6f', '#927c6f', '#937c6f', '#937c6e', '#947c6e', '#957c6e', '#957c6d', '#967c6d', '#967c6d', '#977c6c', '#977b6c', '#987b6c', '#987b6b', '#997b6b', '#9a7b6b', '#9a7b6a', '#9b7b6a', '#9b7b6a', '#9c7b69', '#9c7b69', '#9d7b69', '#9d7b68', '#9e7b68', '#9e7b68', '#9f7b67', '#a07b67', '#a07b67', '#a17b66', '#a17b66', '#a27b66', '#a27b65', '#a37b65', '#a37b65', '#a47b64', '#a47b64', '#a57b64', '#a57b63',
              '#a67b63', '#a67b63', '#a77b62', '#a77b62', '#a87b62', '#a87b61', '#a97b61', '#a97b61', '#aa7b60', '#aa7b60', '#ab7b60', '#ac7b5f', '#ac7b5f', '#ad7b5f', '#ad7b5e', '#ae7b5e', '#ae7b5e', '#af7b5d', '#af7a5d', '#b07a5d', '#b07a5c', '#b17a5c', '#b17a5c', '#b27a5b', '#b27a5b', '#b37a5b', '#b37a5a', '#b37a5a', '#b47a5a', '#b47a59', '#b57a59', '#b57a59', '#b67a58', '#b67a58', '#b77a58', '#b77a57', '#b87a57', '#b87a57', '#b97a56', '#b97a56', '#ba7a55', '#ba7a55', '#bb7a55', '#bb7a54', '#bc7a54', '#bc7a54', '#bd7a53', '#bd7a53', '#be7a53', '#be7952', '#bf7952', '#bf7952', '#c07951', '#c07951', '#c07951', '#c17950', '#c17950', '#c27950', '#c2794f', '#c3794f', '#c3794e', '#c4794e', '#c4794e', '#c5794d', '#c5794d', '#c6794d', '#c6794c', '#c7794c', '#c7794c', '#c7794b', '#c8794b', '#c8794a', '#c9794a', '#c9784a', '#ca7849', '#ca7849', '#cb7849', '#cb7848', '#cc7848', '#cc7848', '#cd7847', '#cd7847', '#cd7846', '#ce7846', '#ce7846', '#cf7845', '#cf7845', '#d07845', '#d07844', '#d17844', '#d17843', '#d27843', '#d27843', '#d27742', '#d37742', '#d37742', '#d47741', '#d47741', '#d57740', '#d57740', '#d67740', '#d6773f', '#d6773f', '#d7773e', '#d7773e', '#d8773e', '#d8773d', '#d9773d', '#d9773c', '#da773c', '#da773c', '#da763b', '#db763b', '#db763a', '#dc763a', '#dc763a', '#dd7639', '#dd7639', '#de7638', '#de7638']
    mapper = LinearColorMapper(palette=anbrew)

    # make figure
    fig = figure(plot_width=width, plot_height=height,
                 align=("center"),
                 x_axis_location="above",
                 # x_range=list(dt.index),
                 # y_axis_label="Effects",
                 # y_range=list(reversed(np.unique(dt_heat.y))),
                 toolbar_location=None, tools="")
    fig.y_range.flipped = True
    fig_rect = fig.rect(x="x", y="y",
                        width=1, height=1, source=source,
                        line_color=None,
                        fill_color=transform('value_std', mapper))
    fig.add_layout(LabelSet(x='x', y='y',
                            text='value', text_color="white",
                            text_font_size="12px",
                            text_align="center",
                            source=source))
    fig.add_tools(HoverTool(
        tooltips=[
            ('Value', '@value')
        ],
        renderers=[fig_rect],
        # display a tooltip whenever the cursor is vertically in line with a glyph
        # mode='vline'
    ))

    # remove padding
    fig.min_border = 0
    fig.x_range.range_padding = 0
    fig.y_range.range_padding = 0
    fig.xaxis.axis_line_color = None
    fig.yaxis.axis_line_color = None

    # refine figures
    if not show_x_axis:
        fig.xaxis.visible = False
    if not show_y_axis:
        fig.yaxis.visible = False
    if vertical_x:
        fig.xaxis.major_label_orientation = "vertical"
    if show_legend:
        color_bar = ColorBar(color_mapper=mapper)
        fig.add_layout(color_bar, 'right')

    # outputs
    return source, fig


def specify_tickers(fig, dt, xticks=None, yticks=None):
    ''' rename tickers names'''

    if xticks is not None:
        ticks_int = range(1, dt.shape[1] + 1)
        fig.xaxis.ticker = list(ticks_int)
        dt_key = pd.DataFrame({
            "k": ticks_int,
            "v": xticks})
        fig.xaxis.major_label_overrides = dict(
            [(key, value) for key, value in zip(dt_key.k, dt_key.v)])
    if yticks is not None:
        ticks_int = range(1, dt.shape[0] + 1)
        fig.yaxis.ticker = list(ticks_int)
        dt_key = pd.DataFrame({
            "k": ticks_int,
            "v": yticks})
        fig.yaxis.major_label_overrides = dict(
            [(key, value) for key, value in zip(dt_key.k, dt_key.v)])


def set_figures(SRC, HT):
    # incidence matrix
    SRC["X"], HT["X"] = make_heatmap(
        600, 300, show_x_axis=True, vertical_x=True)
    SRC["Z"], HT["Z"] = make_heatmap(
        600, 300, show_x_axis=True, vertical_x=True)
    SRC["A"], HT["A"] = make_heatmap(
        600, 600, show_x_axis=True, show_y_axis=True)

    # LHS
    H = 800
    W = 120+60
    SRC["lhs"], HT["lhs"] = make_heatmap(
        H + 100, H, show_y_axis=True)
    HT["lhs"].add_layout(Span(location=0, name="vline",
                            dimension='height', line_color='white',
                            line_dash='dashed', line_width=2))
    HT["lhs"].add_layout(Span(location=0, name="hline",
                            dimension='width', line_color='white',
                            line_dash='dashed', line_width=2))

    # SOL
    SRC["sol"], HT["sol"] = make_heatmap(
        W, H, show_y_axis=True)
    HT["sol"].add_layout(Span(location=0, name="hline",
                            dimension='width', line_color='white',
                            line_dash='dashed', line_width=2))

    # RHS
    SRC["rhs"], HT["rhs"] = make_heatmap(
        W, H, show_y_axis=True)
    HT["rhs"].add_layout(Span(location=0, name="hline",
                            dimension='width', line_color='white',
                            line_dash='dashed', line_width=2))



# from bokeh import palettes
# palettes.brewer["YlGnBu"]
# palettes.brewer["Cividis"]
# palettes.Cividis256[:240]
# palettes.Viridis256[:240]
# mapper = LinearColorMapper(palette="Viridis256", low=0)
# mapper = LinearColorMapper(palette="Turbo256", low=0)
# mapper = LinearColorMapper(palette=palettes.Viridis256[:240], low=0)
# mapper = LinearColorMapper(palette=palettes.Magma256[:240], low=0)
# mapper = LinearColorMapper(palette=palettes.Plasma256[:220], low=0)
# , low=-3, high=3)
# mapper = LinearColorMapper(palette=PARAM["heatmap_color"])
# mapper = LinearColorMapper(palette=palettes.Inferno256[:220])
