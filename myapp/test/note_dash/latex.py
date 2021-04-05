# https://community.plotly.com/t/mathjax-latex-in-dash/6653/6
import dash
import dash_html_components as html

# mathjax = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML'
mathjax = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_HTMLorMML'
# mathjax = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?delayStartupUntil=configured&config=TeX-MML-AM_HTMLorMML'

app = dash.Dash(
    __name__,
    external_scripts=[
        mathjax
    ]
)
app.layout = html.Div(id='main', children=[
    html.P(children='Delicious \(\pi\) is inline with my goals.'),
    html.P(children='$$ \lim_{t \\rightarrow \infty} \pi = 0$$'),
    html.P(style={'text-align': 'left'}, children='\(\\leftarrow \pi\)'),
    html.P(style={'text-align': 'left'}, children='not much left.'),
    html.P(style={'text-align': 'right'}, children='\(\pi \\rightarrow\)'),
    html.P(style={'text-align': 'right'}, children='but it feels so right.'),
    html.Div(id='dynamic', children=''),
    html.Button('Add Math', id='button'),
])


@app.callback(
    dash.dependencies.Output('dynamic', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')]
)
def addmath(n_clicks):
  if n_clicks:
    return '$$ x=1 $$'
  else:
    return None


if __name__ == '__main__':
  app.run_server(debug=True, port=8888)
