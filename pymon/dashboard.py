""" """
from datetime import datetime, timedelta
import dash
from dash.dependencies import Output, Input, State
import dash_core_components as core
import dash_html_components as html
import plotly.graph_objs as go
import pymon.database as db

import pandas as pd
import numpy as np

def df_to_table(df):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df.columns])] +
        # Body
        [
            html.Tr(
                [
                    html.Td(df.iloc[i][col])
                    for col in df.columns
                ]
            )
            for i in range(len(df))
        ]
)

sample_data = pd.DataFrame(
    np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
    columns=['name', 'value', 'help'])

app = dash.Dash(__name__,
    routes_pathname_prefix='/dashboard/',
    assets_url_path='./pymon/assets'
)


app.layout = html.Div(
    id='main',
    children=[
        core.Interval(id="i_graphs", interval=1 * 5000, n_intervals=0),
        core.Interval(id="i_servers", interval=1 * 30000, n_intervals=0),
        core.Interval(id="i_time", interval=1 * 1000, n_intervals=0),
        html.Div([
                html.Div([html.H1('PyMon')],
                    className='two columns',
                ),
                html.Div([html.P(datetime.utcnow())],
                    id='time',
                    className='four columns',
                    style={'float': 'right'}
                ),
            ],
            className='row'
        ),
        html.Div([
                html.Div([
                        html.P('Time Range:',
                            style={}
                        ),
                    ],
                    className='one columns'
                ),
                html.Div([
                        core.Slider(
                            min=1,
                            max=60,
                            step=1,
                            marks={x: str(x) for x in range(0, 60, 10)},
                            value=30,
                            updatemode='drag',
                            id='slider-time-range'
                        )
                    ],
                    className='four columns'
                    #style={'display': 'inline-block', 'width': '75%'}
                ),
                html.Div([
                        html.P('Server:',
                            style={}
                        ),
                    ],
                    className='one columns'
                ),
                html.Div([
                        core.Dropdown(id='server-dropdown', options=[])
                    ],
                    id='servers',
                    className='four columns'
                )
            ],
           className='row'
        ),
        html.Div(
            [
                html.Div(id='graphs', style={'marginTop':'5'}),
                html.Div(
                    id='data_table',
                    children=[df_to_table(sample_data)],
                    className='row',
                    style={
                        "maxHeight": "350px",
                        "overflowY": "scroll",
                        "padding": "8px",
                        "marginTop": "5px",
                        "backgroundColor":"white",
                        "border": "1px solid #C8D4E3",
                        "borderRadius": "3px"
                    },
                )
            ],
            id='server_content', 
            className='row',
            style={'margin': '2% 3%'}
        ),

        html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css",rel="stylesheet"),
        html.Link(href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
        html.Link(href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css", rel="stylesheet")
    ],
    className='row',
    style={'margin': '5px'}
)

def set_layout():
    pass

@app.callback(Output("time", "children"),
        [Input("i_time", "n_intervals")])
def update_time(number_intervals):
    return html.P('UTC: ' + datetime.utcnow().strftime('%d/%m/%Y, %H:%M:%S'))

last_value = None
last_dropdown = []

@app.callback(Output("servers", "children"),
        [Input("i_servers", "n_intervals")],
        [State('server-dropdown', 'value')])
def update_servers(number_intervals, selected_server):
    servers = []
    with db.db_session():
        for server in db.select(s.name for s in db.Server):
            servers.append({'label': server, 'value': server})

    determine_graphs(1, 1, 'test-client')

    dropdown = core.Dropdown(id='server-dropdown',
        options=servers,
        value=selected_server
    )
    return dropdown


@app.callback(Output("data_table", "children"),
         [Input('server-dropdown', 'value')])
def update_table_data(server):
    with db.db_session():
        server_data = list(db.select(
            (d.monitor.name, d.value, d.create_date) for d in db.Record
            if d.monitor.server.name == server
        ).order_by(lambda: db.desc(d.create_date))[:100])

    sample_data = pd.DataFrame(
        server_data, columns=['name', 'value', 'created']
    )
    return df_to_table(sample_data)


@app.callback(Output("graphs", "children"),
        [Input("i_graphs", "n_intervals"),
         Input('slider-time-range', 'value'),
         Input('server-dropdown', 'value')])
def determine_graphs(number_intervals, time_range, server):
    with db.db_session():
        server_mons = list(db.select(
            d.name for d in db.Monitor
            if d.server.name == server
        ))

        server_data = list(db.select(
            (d.monitor.name, d.value, d.create_date) for d in db.Record
            if d.monitor.server.name == server
        )[:100])

    sample_data = pd.DataFrame(server_data, columns=['name', 'value', 'created'])

    graphs = []

    for monitor in server_mons:
        graphs.append(update_graphs(monitor, time_range, server))

    print(len(graphs))
    graph = html.Div(
        children=graphs,
        className='row',
        style={'marginTop': '5px'}
    )
    return graph


def update_graphs(monitor_name, time_range, server):
    if server is None:
        return html.Div('Please select a server')

    with db.db_session():
        data = db.select(
            (d.value, d.create_date) for d in db.Record 
            if d.monitor.name == monitor_name
            and d.create_date >= datetime.utcnow() - timedelta(minutes=time_range)
        ).order_by(lambda: d.create_date)
        x = [x[1] for x in data]
        y = [y[0] for y in data]
        both = list(data)

    # Complex process to add "gaps" to graph
    '''
    first = True
    previous_time = None
    new = []
    for v, t in both:
        if first:
            new.append((v, t))
            previous_time = t
            first = False
            continue
        diff = (t - previous_time).total_seconds()
        if diff > 30:
            new.append((0, previous_time))
            new.append((0, t))
        previous_time = t
        new.append((v, t))

    x = [x[1] for x in new]
    y = [x[0] for x in new]
    '''
    trace = go.Scatter(
        x=x,
        y=y,
        mode='lines+markers',
        fill='tozeroy',
        name='Test',
        connectgaps=False
    )

    layout = go.Layout(
        #title=monitor_name,
        uirevision='same',
        yaxis={'range': [0,100]},
        margin=go.layout.Margin(
            l=33,
            r=25,
            t=5,
            b=37,
            pad=4
        )
    )
    graph = html.Div(
        children=[
            html.P(monitor_name),
            core.Graph(
                id=server+'_'+monitor_name,
                figure={
                    'data': [trace], 
                    'layout': layout,
                },
                style={"height": "90%", "width": "98%"},
                config={
                    'displayModeBar': False
                }
            )
        ],
        className='four columns chart_div'
    )
    return graph


def get_app(__name__):
    return app.server

def run_server():
    app.run_server(debug=True)

