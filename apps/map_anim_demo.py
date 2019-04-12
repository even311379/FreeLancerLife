import os
import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash
import plotly.graph_objs as go
from dash.dependencies import Input, Output, Event, State
from apps.utils import parse_my_geoj

'''
The performance issue is so huge that maybe I'll skip the animation functions in dash.
In dash applications, animation is achieved by update whole figure, however, in plotly, you just switch between 
frames.
The frames function is not supproted in dash.

The dash way to achieve simple task in plotly animation is so difficult. I have to hack many stuff.
The functions is also buggy. (ex. can't reset n_intervals when I have to reset interval)

'''

# b4_css = 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css'
app = DjangoDash('demo_map_anim')
# app = dash.Dash(__name__)

mapbox_access_token = 'pk.eyJ1IjoiZXZlbjMxMTM3OSIsImEiOiJjamFydGVtOHk0bHo1MnFyejhneGowaG1sIn0.gyK3haF84TD-oxioghabsQ'
name, clats, clons = parse_my_geoj('media/documents/MyFarmerField.json')

max_season = 4
amount = [np.random.randint(low=10,high=45,size=17).tolist() for i in range(4)]

data = [
        go.Scattermapbox(
            lat=[str(i) for i in clats],
            lon=[str(i) for i in clons],
            mode='markers',
            marker=dict(
                size=amount[0]
            ),
            # text=name,
            hoverinfo = 'text',
            hovertext=name,
        ) 
        ]

layout = go.Layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        layers=[
            dict(
                sourcetype = 'geojson',
                source = '/media/documents/MyFarmerField.json',
                type = 'fill',
                color = "rgba(255,240,100,1)",
                fill = {'outlinecolor':"rgba(0,0,0,0)"},
                below = 'national_park' 
                # this layer id is coming from mapbox, so I have to check the style I choose
                # https://community.plot.ly/t/solved-show-points-above-choropleth-layer/6552
            )
        ],
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=24.656583,
            lon=121.720779
        ),
        pitch=0,
        zoom=15,
        # style='satellite',
        style='outdoors',
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    modebar=dict(bgcolor='#F8F9FA')
)
demo_map = go.Figure(data=data, layout=layout)

app.layout = html.Div([
    html.Div(dcc.Graph(id='test_map',figure=demo_map,animate=True,style={'height': '800px',})),
    html.Button('Play', id='PlayButton',className='btn btn-primary'),
    dcc.Slider(
        id='season_slider',
        min=0,
        max=3,
        marks={
            0: '春',
            1: '夏',
            2: '秋',
            3: '冬',
        },
        value=0
        ),
    html.Div(id='empty', style={'display':'none'}),
    html.Div('0', id='GS_VALUE', style={'display': 'none'}),
    html.Div(dcc.Interval(
        id='graph-update',
        interval=60*60*1000, # interval unit is milli sec., so 1000 means 1 sec
        ),id='my_output_interval'
        ),
    ],
    className='container bg-light',
    )


#set text for play anim button
@app.callback(
    Output('PlayButton', 'children'),
    [Input('PlayButton', 'n_clicks')])
def clicks(n_clicks):
    if n_clicks:
        if n_clicks % 2:
            return 'Pause'
        else:
            return 'Play'
    else:
        return 'Play'

# set global var same value as slider value
@app.callback(
    Output('GS_VALUE','children'),
    [Input('season_slider', 'value')])
def update_GS_VALUE(value):
    if value > 2:
        return 3
    else:
    # global GS_VALUE
    # GS_VALUE = value
        print(value)
        return value


# Update graph by changing slider value
@app.callback(
    Output('test_map','figure'),
    [Input('GS_VALUE', 'children')])
def update_graph(gs_value):
    value = int(gs_value)
    data = [
        go.Scattermapbox(
            lat=[str(i) for i in clats],
            lon=[str(i) for i in clons],
            mode='markers',
            marker=dict(
                size=amount[value]
            ),
            # text=name,
            hoverinfo = 'text',
            hovertext=name,
        ) 
    ]
    u_fig = go.Figure(data=data, layout=layout)
    return u_fig

# turn on/off update by set update interval very long or short
@app.callback(
    Output('my_output_interval','children'),
    [Input('PlayButton', 'n_clicks'),
    Input('GS_VALUE', 'children')])
def anim_switcher(n_clicks,gs_value):
    gs_value = int(gs_value)
    if gs_value > 2:
        print('stop!!')
        return dcc.Interval(id='graph-update',interval=36000000)
    else: 
        if n_clicks:
            if n_clicks % 2:
                return dcc.Interval(id='graph-update',interval=2000,n_intervals=gs_value)
            else:
                return dcc.Interval(id='graph-update',interval=3600000)

# set auto update slider value
@app.callback(
    Output('season_slider', 'value'),
    [Input('graph-update', 'n_intervals')])
def Update_slider(n_intervals):
    return n_intervals


# if __name__ == '__main__':
#     app.run_server(debug=True)

