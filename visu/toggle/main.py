
from dash import Dash, dcc, html, Input, Output
import dash_daq as daq
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import math
import sqlite3


app = Dash(__name__)
app.config.suppress_callback_exceptions=True

conn = sqlite3.connect('data.db')
points = pd.read_sql('SELECT * FROM data', conn) 
conn.close()

print('start')




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
                            ], style={'width': '33%', 'display': 'inline-block'}),
                            html.Div([
                                dcc.Graph(
                                    id='signal-bar'
                                )                                
                            ], style={'width': '33%', 'display': 'inline-block'}),
                            html.Div([
                                dcc.Graph(
                                    id='beacon-bar'
                                )                                
                            ], style={'width': '33%', 'float': 'right', 'display': 'inline-block'})
                        ]),
                    html.Div([
                        dcc.Graph(
                            id='error-histogram'
                        ),
                        dcc.Graph(
                            id='error-map'
                        )
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
    conn = sqlite3.connect('data.db')
    data = pd.read_sql('SELECT * FROM data', conn) 
    conn.close()
    return data['ssid'].unique().tolist()


#Update heatmap
@app.callback(
    Output('ssid-heatmap', 'figure'),
    Input('ssid-menu', 'value'))
def update_figure(selected_ssid):
    conn = sqlite3.connect('data.db')
    points = pd.read_sql('SELECT * FROM data', conn)
    conn.close() 
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
    conn = sqlite3.connect('data.db')
    points = pd.read_sql('SELECT * FROM data', conn)
    conn.close() 
    filtered_points = points.drop(points[points.ssid != selected_ssid].index)
    fig = go.Figure(data=go.Bar(y=filtered_points.groupby('channel')['channel'].count(), x=sorted(filtered_points['channel'].unique()), width=0.8))
    fig.update_layout(title_text='Channel')
    return fig

#Update Signal barchart
@app.callback(
    Output('signal-bar', 'figure'),
    Input('ssid-menu', 'value'))
def update_figure(selected_ssid):
    conn = sqlite3.connect('data.db')
    points = pd.read_sql('SELECT * FROM data', conn) 
    conn.close()
    filtered_points = points.drop(points[points.ssid != selected_ssid].index)
    fig = go.Figure(data=go.Bar(y=filtered_points.groupby('strength')['strength'].count(), x=sorted(filtered_points['strength'].unique()), width=0.8))
    fig.update_layout(title_text='Signal Strength')
    return fig

#Update beacon barchart
@app.callback(
    Output('beacon-bar', 'figure'),
    Input('ssid-menu', 'value'))
def update_figure(selected_ssid):
    conn = sqlite3.connect('data.db')
    points = pd.read_sql('SELECT * FROM data', conn) 
    conn.close()
    filtered_points = points.drop(points[points.ssid != selected_ssid].index)
    fig = go.Figure(data=go.Bar(y=filtered_points.groupby('beacon')['beacon'].count(), x=sorted(filtered_points['beacon'].unique()), width=1.0))
    fig.update_layout(title_text='Time Since Last Beacon')
    return fig


#Update Error Histogram
@app.callback(
    Output('error-histogram', 'figure'),
    Input('ssid-menu', 'value'))
def update_figure(selected_ssid):
    conn = sqlite3.connect('data.db')
    points = pd.read_sql('SELECT * FROM data', conn)
    conn.close() 
    filtered_points = points.drop(points[points.ssid != selected_ssid].index)
    fig = px.density_heatmap(filtered_points, x="elat", y="elon", marginal_x="histogram", marginal_y="histogram", text_auto=True)
    fig.update_layout(height=1000 ,margin={"r":0,"t":0,"l":0,"b":0})
    return fig

#Update Error Map
@app.callback(
    Output('error-map', 'figure'),
    Input('ssid-menu', 'value'))
def update_figure(selected_ssid):
    conn = sqlite3.connect('data.db')
    points = pd.read_sql('SELECT * FROM data', conn) 
    conn.close()
    filtered_points = points.drop(points[points.ssid != selected_ssid].index)
    fig = go.Figure()

    print('test')

    value_max = filtered_points['strength'].max()
    value_min = filtered_points['strength'].min()
    value_twothirds = value_min + 2*((value_max-value_min)/3)
    value_onethird = value_min + (value_max-value_min)/3
    value_min = filtered_points['strength'].min()

    lat1 = []
    lat2 = []
    lat3 = []
    lon1 = []
    lon2 = []
    lon3 = []

    print(value_max)
    print(value_min)

    for row in filtered_points.iterrows():
        if row[1]['elat'] != 'n/a':
            #row[0] is the row number and row[1] is the tuple(?) with the data
            if row[1]['strength'] >= value_twothirds:
                lat1 = lat1+binlat(float(row[1]['lat']),float(row[1]['elat'])) 
                lon1 = lon1+binlon(float(row[1]['lon']),float(row[1]['elon']))
            if row[1]['strength'] >= value_onethird:
                lat2 = lat2+binlat(float(row[1]['lat']),float(row[1]['elat']))
                lon2 = lon2+binlon(float(row[1]['lon']),float(row[1]['elon']))
            if row[1]['strength'] >= value_min:
                lat3 = lat3+binlat(float(row[1]['lat']),float(row[1]['elat']))
                lon3 = lon3+binlon(float(row[1]['lon']),float(row[1]['elon']))
                    

    # Create top rectangle
    fig.add_trace(go.Scattermapbox(
        lon = lon1,
        lat = lat1,
        mode = 'lines',
        line = dict(color = 'green', width = 2),
        fill = "toself",
        opacity=0.5
    ))
    #Create mid rectangle
    fig.add_trace(go.Scattermapbox(
        lon = lon2,
        lat = lat2,
        mode = 'lines',
        line = dict(color = 'yellow', width = 2),
        fill = "toself",
        opacity=0.5
    ))
    #Create bot rectangle
    fig.add_trace(go.Scattermapbox(
        lon = lon3,
        lat = lat3,
        mode = 'lines',
        line = dict(color = 'red', width = 2),
        fill = "toself",
        opacity=0.5
    ))
    fig.update_layout(
    mapbox = {
        'style': "open-street-map",
        'center': { 'lon': 13.3256412, 'lat': 52.5156451},
        'zoom': 16},


    height=1000,
    margin = {'l':0, 'r':100, 'b':0, 't':0})

    return fig


#Update MAC-Menu
@app.callback(
    Output('ip-menu', 'options'),
    Input('update-button-state', 'n_clicks'))
def update_ip_menu(n_clicks):
    conn = sqlite3.connect('data.db')
    data = pd.read_sql('SELECT * FROM data', conn) 
    conn.close()
    return data['ip'].unique().tolist()


def binlat (lat, error):
    error_degree = error * 0.00001466666
    list = [lat+error_degree, lat+error_degree, lat-error_degree, lat-error_degree, lat+error_degree, None]
    return list

def binlon (lon, error):
    error_degree = error * 0.00001466666
    list = [lon+error_degree, lon-error_degree, lon-error_degree, lon+error_degree, lon+error_degree, None]
    return list








if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True, port=8050)


