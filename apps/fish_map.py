import os
import json
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash
import plotly.graph_objs as go
from dash.dependencies import Input, Output, Event

from apps.utils import EOO_calculator, create_geojson

fish_data = pd.read_excel('media/documents/fish_demo_data.xlsx')
fish_names_dict = []
for i in fish_data.Scientific_name.unique():
    fish_names_dict.append({'label':i,'value':i})

app = DjangoDash('FishMap')
mapbox_access_token = 'pk.eyJ1IjoiZXZlbjMxMTM3OSIsImEiOiJjamFydGVtOHk0bHo1MnFyejhneGowaG1sIn0.gyK3haF84TD-oxioghabsQ'

# style: light, dark, outdoors,

# fig = dict(data=data, layout=layout)

app.layout  = html.Div([
    dcc.Dropdown(
    id='species_selector',
    options=fish_names_dict,
    value=''
    ),
    html.Div(id='fish_info'),
    html.Div(id='fish_map'),
])

@app.callback(
    Output('fish_info','children'),
    [Input('species_selector', 'value')]
)
def show_info(value):
    return 'You have selected "{}"'.format(value)


@app.callback(
    Output('fish_map','children'),
    [Input('species_selector', 'value')]
)
def show_map(value):
    if not value:
        return 'please select a species'
    else:
        
        df = fish_data[fish_data.Scientific_name == value]
        fish_name = value.replace(' ','_')
        print(len(df))
        print(EOO_calculator(df)[0])
        print(len(EOO_calculator(df)[0]))
        if len(df[['Latitude','Longitude']]) >= 3:
            EOO = EOO_calculator(df)[1]
            create_geojson(EOO_calculator(df)[0], fish_name)
        else:
            create_geojson([], fish_name)

        data = [
            go.Scattermapbox(
                lat=df.Latitude.tolist(),
                lon=df.Longitude.tolist(),
                mode='markers',
                marker=dict(
                    size=14
                ),
                text=[str(i)+'_'+str(j) for i,j in zip(df.Year,df.Source)],
            )
        ]

        layout = go.Layout(
            autosize=True,
            hovermode='closest',
            mapbox=dict(
                layers=[
                    dict(
                        sourcetype = 'geojson',
                        source = '/media/documents/{}.json'.format(fish_name),
                        type = 'fill',
                        color = "rgba(255,240,100,0.5)",
                        fill = {'outlinecolor':"rgba(0,0,0,0)"}
                    )
                ],
                accesstoken=mapbox_access_token,
                bearing=0,
                center=dict(
                    lat=24,
                    lon=121
                ),
                pitch=0,
                zoom=7,
                style='outdoors'
            ),
        )
        fish_map = dict(data=data, layout=layout)
        if len(df[['Latitude','Longitude']]) >= 3:
            EOO_text = 'EOO = {0} km^2'.format(round(EOO,2))
        else:
            EOO_text = 'Too few points to draw EOO.'

        return [html.H3('The sites for ' + value),
             dcc.Graph(id='graph', figure=fish_map, style={'height': '800px',}),
             EOO_text]

# app.layout = html.Div(
#     children=[html.H1('Dash tutorial'),
#     dcc.Graph(id='example',figure = {'data':[
#         {'x':[1,2,3,4,5],'y':[5,4,3,2,1],'type':'line','name':'Boats'},
#         {'x':[1,2,3,4,5],'y':[3,3,2,2,1],'type':'bar','name':'cars'},],
#         'layout':{'title':'basic dash sample'},},
#         style={'height': '500%','display':'inline-block'}
#         )
#     ])