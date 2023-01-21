
from dash import Dash, dcc, html, Input, Output
import dash_daq as daq
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import math



app = Dash(__name__)
app.config.suppress_callback_exceptions=True

points = pd.read_csv('/app/track_points.csv')


app.layout = html.Div([
    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-1',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='SSID-Stats',
                value='tab-1',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='AP-Stats',
                value='tab-2',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
        ]),
    html.Div(id='tabs-content-classes')
])


@app.callback(Output('tabs-content-classes', 'children'),
              Input('tabs-with-classes', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
                    html.Div([
                        html.Div([
                            dcc.Dropdown(
                                points['ssid'].unique(),
                                'eduroam',
                                id='ssid-menu'
                            )
                        ], style={'width': '90%', 'display': 'inline-block'}),
                        html.Div([
                            html.Button(id='update-button-state', n_clicks=0, children='Update', style={'font-size': '24px'}),
                        ], style={'width': '100px', 'float': 'right', 'display': 'inline-block'})
                    ]),
                    dcc.Graph(
                        id='ssid-heatmap'
                    ),
                    html.Div([
                            html.Div([
                                dcc.Graph(
                                    id='channel-bar'
                                )
                            ], style={'width': '50%', 'display': 'inline-block'}),
                            html.Div([
                                dcc.Graph(
                                    id='signal-bar'
                                )                                
                            ], style={'width': '50%', 'float': 'right', 'display': 'inline-block'})
                        ]),
                    html.Div([
                            html.Div([
                                dcc.Graph(
                                    id='elat-bar'
                                )
                            ], style={'width': '50%', 'display': 'inline-block'}),
                            html.Div([
                                dcc.Graph(
                                    id='elon-bar'
                                )                                
                            ], style={'width': '50%', 'float': 'right', 'display': 'inline-block'})
                        ])
                ])
    elif tab == 'tab-2':
        return html.Div([
                    html.Div([
                        html.Div([
                            dcc.Dropdown(
                                points['ip'].unique(),
                                id='ip-menu'
                            )
                        ], style={'width': '90%', 'display': 'inline-block'}),
                        html.Div([
                            html.Button(id='update-button-state', n_clicks=0, children='Update', style={'font-size': '24px'}),
                        ], style={'width': '100px', 'float': 'right', 'display': 'inline-block'})
                    ])
                ])










#Updates SSID-Menu. The return must be a list and no dataframe
@app.callback(
    Output('ssid-menu', 'options'),
    Input('update-button-state', 'n_clicks'))
def update_ssid_menu(n_clicks):
    data = pd.read_csv('/app/track_points.csv')
    return data['ssid'].unique().tolist()


#Update heatmap
@app.callback(
    Output('ssid-heatmap', 'figure'),
    Input('ssid-menu', 'value'))
def update_figure(selected_ssid):
    points = pd.read_csv('/app/track_points.csv')
    filtered_points = points.drop(points[points.ssid != selected_ssid].index)
    fig = go.Figure(go.Densitymapbox(lat=filtered_points.lat, lon=filtered_points.lon, z=filtered_points.strength,radius=10))
    fig.update_geos(fitbounds="locations")
    fig.update_layout(mapbox_style="open-street-map", mapbox_center_lat=52.5156451, mapbox_center_lon=13.3256412, mapbox_zoom=16)
    fig.update_layout(height=1000 ,margin={"r":0,"t":0,"l":0,"b":0})

    return fig

#Update Channel barchart
@app.callback(
    Output('channel-bar', 'figure'),
    Input('ssid-menu', 'value'))
def update_figure(selected_ssid):
    points = pd.read_csv('/app/track_points.csv')
    filtered_points = points.drop(points[points.ssid != selected_ssid].index)
    fig = go.Figure(data=go.Bar(y=filtered_points.groupby('channel')['channel'].count(), x=sorted(filtered_points['channel'].unique()), width=0.8))
    fig.update_layout(title_text='Channel')
    return fig

#Update Signal barchart
@app.callback(
    Output('signal-bar', 'figure'),
    Input('ssid-menu', 'value'))
def update_figure(selected_ssid):
    points = pd.read_csv('/app/track_points.csv')
    filtered_points = points.drop(points[points.ssid != selected_ssid].index)
    fig = go.Figure(data=go.Bar(y=filtered_points.groupby('strength')['strength'].count(), x=sorted(filtered_points['strength'].unique()), width=0.8))
    fig.update_layout(title_text='Signal Strength')
    return fig

#Update ELAT barchart
@app.callback(
    Output('elat-bar', 'figure'),
    Input('ssid-menu', 'value'))
def update_figure(selected_ssid):
    points = pd.read_csv('/app/track_points.csv')
    filtered_points = points.drop(points[points.ssid != selected_ssid].index)
    fig = go.Figure(data=go.Bar(y=filtered_points.groupby('elat')['elat'].count(), x=sorted(filtered_points['elat'].unique()), width=0.8))
    fig.update_layout(title_text='Error Latitude')
    return fig

#Update ELON barchart
@app.callback(
    Output('elon-bar', 'figure'),
    Input('ssid-menu', 'value'))
def update_figure(selected_ssid):
    points = pd.read_csv('/app/track_points.csv')
    filtered_points = points.drop(points[points.ssid != selected_ssid].index)
    fig = go.Figure(data=go.Bar(y=filtered_points.groupby('elon')['elon'].count(), x=sorted(filtered_points['elon'].unique()), width=0.8))
    fig.update_layout(title_text='Error Longitude')
    return fig

#Update MAC-Menu
@app.callback(
    Output('ip-menu', 'options'),
    Input('update-button-state', 'n_clicks'))
def update_ip_menu(n_clicks):
    data = pd.read_csv('/app/track_points.csv')
    return data['ip'].unique().tolist()






if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True, port=8050)


