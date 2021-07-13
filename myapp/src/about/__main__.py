from ..lib import *

def page_about():
    text = Div(text="""
    <h1> About </h1>

    <h2> Authors </h2>
    Chunpeng James Chen: niche@ucdavis.edu <br>
    Hao Cheng: qtlcheng@ucdavis.edu

    <h2> Examples </h2>
    Example datasets in this app are collected from the book
    "Mrode,R.A. (2013) Linear models for the prediction of animal breeding values 3rd ed. CABI, Boston, MA".

    """, width=1000, style={'font-size': '200%'})

    return column(text)


# <h1 > LMMonBoard < /h1 >
# <h2 > header 2 < /h2 >
# abstjkljioej lj
# salkdjf ij
# alskdj
# <ul >
# <li>Coffee</li>
# <li>Tea</li>
# <li>Milk</li>
# </ul>
