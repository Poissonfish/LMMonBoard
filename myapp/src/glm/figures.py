from .__main__ import *

size_fig = 350

p = figure(title="Fitted values by Fixed model",
           width=size_fig, height=size_fig,
           tools="",
           toolbar_location=None,
           align=("center", "center"))
p_circle = p.circle('obs', 'bv', source=SRC["y_s"], fill_alpha=0.2, size=10)
p_line = p.line('obs', 'obs', source=SRC["y_s"], color='red')
p.xaxis.axis_label = "Phenotype"
p.yaxis.axis_label = "Breeding Values"
p.add_layout(LabelSet(x=15, y=250, text="err",
                      source=SRC["y_s"],
                      text_font_size='14px', text_color='black',
                      x_units='screen', y_units='screen',
                      background_fill_color='white'))
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

GUI["fig_scatterFit"] = p

##
h_y = figure(title="Distribution of Phenotypes and GEBVs",
             tools='', toolbar_location=None,
             width=800, height=300)
h_y.quad(source=SRC["h_y"], legend="Phenotypes",
         top="yp_hist", bottom=0, left="yp_edL", right="yp_edR",
         fill_color="red", line_color="black", alpha=0.5)
h_y.quad(source=SRC["h_y"], legend="Breeding Values",
         top="yg_hist", bottom=0, left="yg_edL", right="yg_edR",
         fill_color="navy", line_color="black", alpha=0.5)

h_m = figure(title="Distribution of Marker Effects",
             tools='', toolbar_location=None,
             width=800, height=300)
h_m.quad(source=SRC["h_m"], legend="Effect Distribution",
         top="m_hist", bottom=0, left="m_edL", right="m_edR",
         fill_color="red", line_color="black", alpha=0.5)
h_m.quad(source=SRC["h_m"], legend="Sampled Effects",
         top="ms_hist", bottom=0, left="ms_edL", right="ms_edR",
         fill_color="navy", line_color="black", alpha=0.5)

GUI["fig_hisGEBV"] = h_y
GUI["fig_hisMarker"] = h_m
