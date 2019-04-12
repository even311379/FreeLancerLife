import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, Event
from django_plotly_dash import DjangoDash
import plotly.graph_objs as go
import pandas as pd
import pandas_datareader.data as web
import datetime

import plotly
import random
import plotly.graph_objs as go
from collections import deque


# app = DjangoDash('SimpleExample')   # replaces dash.Dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Interval(id='my-interval'),
    dcc.RadioItems(id='set-time',
        value=1000,
        options=[
            {'label': 'Every second', 'value': 1000},
            {'label': 'Every 5 seconds', 'value': 5000},
            {'label': 'Off', 'value': 60*60*1000} # or just every hour
        ]),
    html.Div(id='display-time')
])


@app.callback(
    dash.dependencies.Output('display-time', 'children'),
    events=[dash.dependencies.Event('my-interval', 'interval')])
def display_time():
    return str(datetime.datetime.now())


@app.callback(
    dash.dependencies.Output('my-interval', 'interval'),
    [dash.dependencies.Input('set-time', 'value')])
def update_interval(value):
    return value

'''
X = deque(maxlen=20)
Y =deque(maxlen=20)
X.append(1)
Y.append(1)

# app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1000 # interval unit is milli sec., so 1000 means 1 sec
        )
    ]
)

@app.callback(Output('live-graph','figure'),events = [Event('graph-update','interval')])
def update_graph():
    global X
    global Y
    X.append(X[-1]+1)
    Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))

    data = go.Scatter(
        x = list(X),
        y = list(Y),
        name = 'Scatter',
        mode = 'lines+markers'
    )

    return {'data':[data],
        'layout': go.Layout(xaxis=dict(range=[min(X),max(X)]),
        yaxis=dict(range=[min(Y),max(Y)])
        )
        }
'''


'''
# tutorial 03
'''
# app.layout = html.Div(
#     children=[html.H1('Dash tutorial'),
#     html.Div(children='''
#         symbol to graph:
#     '''),
#     dcc.Input(id='input', value='', type='text'),
#     html.Div(id='output-graph')
#     ])


# @app.callback(
#     Output(component_id='output-graph', component_property='children'),
#     [Input(component_id='input', component_property='value')]
# )
# def update(input_data='TSLA'):
#     stock = input_data
#     try:
#         df = web.DataReader(stock,'iex',start,end)
#     except:
#         return 'You typed a wrong stock symble, try: AAPL'

#     return dcc.Graph(
#         id='example',
#         figure={
#             'data':[
#                 {'x':df.index,'y':df.close,'type':'line','name':stock},
#             ],
#             'layout':{'title':'stock of {}'.format(stock)},},)

'''
# tutorual 02
app.layout = html.Div(children=[
    dcc.Input(id='input',value='Enter something', type='text'),
    html.Div(id='output')
])

@app.callback(
    Output(component_id='output', component_property='children'),
    [Input(component_id='input', component_property='value')])
def update_value(input_data):
    try:
        return str(float(input_data)**2)
    except:
        return "Error"
'''


'''
# tutorial 01

app.layout = html.Div(
    children=[html.H1('Dash tutorial'),
    dcc.Graph(id='example',figure = {'data':[
        {'x':[1,2,3,4,5],'y':[5,4,3,2,1],'type':'line','name':'Boats'},
        {'x':[1,2,3,4,5],'y':[3,3,2,2,1],'type':'bar','name':'cars'},],
        'layout':{'title':'basic dash sample'},},
        style={'hieght': '500%','display':'inline-block'}
        )
    ])
'''