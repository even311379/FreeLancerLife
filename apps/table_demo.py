import os
import json
import pandas as pd

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash
import plotly.graph_objs as go
import plotly.io as pio
from dash.dependencies import Input, Output, Event

from random import randint

b4_css = 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css'

name = ['A','A','A','A','A','A','B','B','B','B','B','B','C','C','C','C','C','C',]
location = ['L1','L2','L3']*6
season = ['S1','S1','S1','S2','S2','S2']*3
num = [randint(0,30) for i in range(18)]
df = pd.DataFrame(dict(name=name,location=location,season=season,num=num))

# app = dash.Dash(__name__)
app = DjangoDash('demo_app')
app.css.append_css({"external_url":b4_css})

# style: light, dark, outdoors,

# fig = dict(data=data, layout=layout)

app.layout  = html.Div([
    html.Div('Example Div', style={'padding': '5rem 0', 'fontSize': 14}),
    html.Div([
        html.Div(
            dash_table.DataTable(
            id='demo_table',
            data=df.to_dict('rows'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            n_fixed_rows=1,
            style_cell={'whiteSpace': 'normal'},
            virtualization=True,
            filtering=True,
            sorting=True,
            ),
            className="col"),
        html.Div(id='demo_graphs',className="col"),
    ],className="row")
])


@app.callback(
    Output('demo_graphs','children'),
    [Input('demo_table', 'derived_virtual_data')]
)
def update_graph(rows):
    if rows is None:
        dff = df
    else:
        dff = pd.DataFrame(rows)
    
    data = go.Bar(
        x=dff['name'].unique(),
        y=dff.groupby(['name']).mean().num.tolist(),
        error_y=dict(
            type='data',
            array=dff.groupby(['name']).std().num.tolist(),
            visible=True
        )
    )
    this_fig = go.Figure(data=[data])
    this_fig.layout.template = 'plotly_dark'
    graph = html.Div(
        dcc.Graph(figure = this_fig)
    )
    return graph


# if __name__ == '__main__':
#     app.run_server(debug=True)