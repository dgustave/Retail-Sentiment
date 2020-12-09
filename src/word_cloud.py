import chart_studio.plotly as py
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go


# matplotlib library
import pandas as pd
import random





def Word_Cloud(): 

    timesData = pd.read_csv('../data/raw/word_test.csv')

    weights = [random.randint(1, 50) for i in range(len(timesData.country.value_counts()))]
    data = go.Scatter(x=[random.random() for i in range(20)],
                    y=[random.random() for i in range(20)],
                    mode='text',
                    text=timesData.country.unique(),
                    marker={'opacity': 0.3},
                    textfont={'size': weights,
                            'color': [
        "#636EFA","#EF553B","#00CC96","#AB63FA","#19D3F3",
        "#E763FA", "#FECB52","#FFA15A","#FF6692","#B6E880", "teal"
    ]})
    layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                        'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False}})
    fig = go.Figure(data=[data], layout=layout)
    fig.update_layout(
    title="Requested Stock Info",
    yaxis_title=f"Most Talked About",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
    )

    fig.write_html('templates/word.html')


   

