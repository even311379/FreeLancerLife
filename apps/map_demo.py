import os
import pandas as pd
import numpy as np

import dash
import dash_table
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
app = DjangoDash('demo_map')
# app = dash.Dash(__name__)

mapbox_access_token = 'pk.eyJ1IjoiZXZlbjMxMTM3OSIsImEiOiJjamFydGVtOHk0bHo1MnFyejhneGowaG1sIn0.gyK3haF84TD-oxioghabsQ'
name, clats, clons = parse_my_geoj('media/documents/map_final.geojson')

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
    title='Farm fields managed',
    titlefont=dict(color='#CCCCCC', size=20),
    autosize=True,
    hovermode='closest',
    height=500,
    margin=dict(l=20,r=20,b=20,t=40),
    mapbox=dict(
        layers=[
            dict(
                sourcetype = 'geojson',
                source = '/media/documents/map_final.geojson',
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
    paper_bgcolor='#7B7C7C',
    # plot_bgcolor='rgba(0,0,0,0)',
    # modebar=dict(bgcolor='#F8F9FA')
)


demo_map = go.Figure(data=data, layout=layout)

app.layout = html.Div([
    html.P('Please select the season, and all infomation will change'),
    dcc.RadioItems(
        id='my_radio',
        options=[
            {'label':'春','value':'0'},
            {'label':'夏','value':'1'},
            {'label':'秋','value':'2'},
            {'label':'冬','value':'3'},
        ],
        value='0',
        labelStyle={'display': 'inline-block'},
        className='mt-2'

    ),
    html.Div(dcc.Graph(id='test_map',figure=demo_map)),
    html.Div([
        html.Div([html.H3('本季資料表'),html.Div(id='left_panel')],className='col col-6'),
        html.Div([html.H3('本季柱狀圖'),html.Div(id='right_panel')],className='col col-6'),
    ], className='row mt-2 d-flex justify-content-between'),
    ],
    className='container bg-light',
    )

# Update graph by changing slider value
@app.callback(
    Output('test_map','figure'),
    [Input('my_radio', 'value')])
def update_graph(value):
    value = int(value)
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


@app.callback(
    Output('left_panel','children'),
    [Input('my_radio','value')])
def left_panel_contents(value):
    value = int(value)
    df = pd.DataFrame(dict(name=name,amount=amount[value]))
    return dash_table.DataTable(
            data=df.to_dict('rows'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            virtualization=True,
            style_as_list_view=True,
            style_header={
                'fontWeight': 'bold',
                'backgroundColor': '#00676A',
                'color': 'white'
            },
            style_cell_conditional=[
            {
                'if': {'column_id': 'name'},
                'textAlign': 'left'
            } ,{'backgroundColor': '#00676A','color': 'white'}]
            )
@app.callback(
    Output('right_panel','children'),
    [Input('my_radio','value')])
def right_panel_contents(value):
    value = int(value)
    print(value)
    df = pd.DataFrame(dict(name=name,amount=amount[value]))
    dff = df.sort_values(by=['amount']).reset_index(drop=True)
    X = dff['name'].tolist()
    Y = dff['amount'].tolist()
    simple_fig = dcc.Graph(
        figure=dict(
        data=[go.Bar(x = X,y =Y,marker=dict(color="#0074D9"))],
        layout=dict(xaxis=dict(automargin=True),
                    yaxis=dict(automargin=True),
                    margin=dict(t=30,l=10,r=10,b=10),
                    ),
                )
        )

    return simple_fig
# if __name__ == '__main__':
#     app.run_server(debug=True)

