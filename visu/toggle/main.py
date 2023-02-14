
# The code creates a Dash app that displays two tabs with different graphs and data. 
# The first function, app.layout, creates the two tabs for the app and assigns each to a different value ('tab-1' and 'tab-2'). It also creates a Div for each of the tabs which will later be populated with HTML code.
# The second function, render_content, is a callback which is used to render the content of the tabs when they are clicked. It takes the value of the tab as an input and returns the HTML code which will be displayed in the tab. 
# The third function, update_ssid_menu, is also a callback and it is used to update the dropdown menu in the first tab with the SSIDs available in the database.
# The fourth function, update_figure, is used to update the heatmap in the first tab with the data corresponding to the selected SSID. It takes the selected SSID as an input and returns a figure containing the heatmap.
# The fifth function, update_channel_bar, is used to update the channel bar chart in the first tab with the data corresponding to the selected SSID. It takes the selected SSID as an input and returns a figure containing the bar chart.
# The sixth function, update_signal_bar, is used to update the signal bar chart in the first tab with the data corresponding to the selected SSID. It takes the selected SSID as an input and returns a figure containing the bar chart.
# The seventh function, update_beacon_bar, is used to update the beacon bar chart in the first tab with the data corresponding to the selected SSID. It takes the selected SSID as an input and returns a figure containing the bar chart.
# The eighth function, update_error_histogram, is used to update the error histogram in the first tab with the data corresponding to the selected SSID. It takes the selected SSID as an input and returns a figure containing the histogram.
# The ninth function, update_ip_menu, is similar to the update_ssid_menu function but is used to update the dropdown menu in the second tab with the IPs available in the database.
# The tenth function, update_ip_figure, is used to update the heatmap in the second tab with the data corresponding to the selected IP. It takes the selected IP as an input and returns a figure containing the heatmap.
# The eleventh function, update_ip_channel_bar, is used to update the channel bar chart in the second tab with the data corresponding to the selected IP. It takes the selected IP as an input and returns a figure containing the bar chart.
# The twelfth function, update_ip_signal_bar, is used to update the signal bar chart in the second tab with the data corresponding to the selected IP. It takes the selected IP as an input and returns a figure containing the bar chart.
# The thirteenth function, update_ip_beacon_bar, is used to update the beacon bar chart in the second tab with the data corresponding to the selected IP. It takes the selected IP as an input and returns a figure containing the bar chart.
# The fourteenth function, update_ip_error_histogram, is used to update the error histogram in the second tab with the data corresponding to the selected IP. It takes the selected IP as an input and returns a figure containing the histogram.
# Finally, the last function, app.run_server, is used to run the Dash app on a local server.


from dash import Dash, dcc, html, Input, Output
import dash_daq as daq
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sqlite3


app = Dash(__name__)
app.config.suppress_callback_exceptions=True

conn = sqlite3.connect('./data/data.db')
points = pd.read_sql('SELECT * FROM data', conn) 
conn.close()

print('start')



#Create Tab 1 and Tab2
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

#Fill Tab 1 and Tab 2 with HTML
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
                    ]),
                    dcc.Graph(
                        id='ip-heatmap'
                    ),
                    html.Div([
                            html.Div([
                                dcc.Graph(
                                    id='ip-channel-bar'
                                )
                            ], style={'width': '33%', 'display': 'inline-block'}),
                            html.Div([
                                dcc.Graph(
                                    id='ip-signal-bar'
                                )                                
                            ], style={'width': '33%', 'display': 'inline-block'}),
                            html.Div([
                                dcc.Graph(
                                    id='ip-beacon-bar'
                                )                                
                            ], style={'width': '33%', 'float': 'right', 'display': 'inline-block'})
                        ]),
                    html.Div([
                        dcc.Graph(
                            id='ip-error-histogram'
                        )
                    ])
                ])










#Updates SSID-Menu. The return must be a list and no dataframe
@app.callback(
    Output('ssid-menu', 'options'),
    Input('update-button-state', 'n_clicks'))
def update_ssid_menu(n_clicks):
    conn = sqlite3.connect('./data/data.db')
    data = pd.read_sql('SELECT * FROM data', conn) 
    conn.close()
    return data['ssid'].unique().tolist()


#Update heatmap
@app.callback(
    Output('ssid-heatmap', 'figure'),
    Input('ssid-menu', 'value'))
def update_figure(selected_ssid):
    conn = sqlite3.connect('./data/data.db')
    points = pd.read_sql('SELECT * FROM data', conn)
    conn.close() 
    if selected_ssid != '':
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
    conn = sqlite3.connect('./data/data.db')
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
    conn = sqlite3.connect('./data/data.db')
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
    conn = sqlite3.connect('./data/data.db')
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
    conn = sqlite3.connect('./data/data.db')
    points = pd.read_sql('SELECT * FROM data', conn)
    conn.close() 
    filtered_points = points.drop(points[points.ssid != selected_ssid].index)
    sorted_points = filtered_points.sort_values(['elat','elon'], ascending=False)
    fig = px.density_heatmap(sorted_points, x="elat", y="elon", marginal_x="histogram", marginal_y="histogram", text_auto=True)
    fig.update_layout(height=1000 ,margin={"r":0,"t":30,"l":0,"b":0})
    fig.update_layout(title_text='GNSS Error Histogram')
    return fig

#############################################

#Update MAC-Menu
@app.callback(
    Output('ip-menu', 'options'),
    Input('update-button-state', 'n_clicks'))
def update_ip_menu(n_clicks):
    conn = sqlite3.connect('./data/data.db')
    data = pd.read_sql('SELECT * FROM data', conn) 
    conn.close()
    return data['ip'].unique().tolist()

#Update heatmap
@app.callback(
    Output('ip-heatmap', 'figure'),
    Input('ip-menu', 'value'))
def update_figure(selected_ssid):
    conn = sqlite3.connect('./data/data.db')
    points = pd.read_sql('SELECT * FROM data', conn)
    conn.close() 
    filtered_points = points.drop(points[points.ip != selected_ssid].index)
    fig = go.Figure(go.Densitymapbox(lat=filtered_points.lat, lon=filtered_points.lon, z=filtered_points.strength,radius=10))
    fig.update_geos(fitbounds="locations")
    fig.update_layout(mapbox_style="open-street-map", mapbox_center_lat=52.5156451, mapbox_center_lon=13.3256412, mapbox_zoom=16)
    fig.update_layout(height=1000 ,margin={"r":0,"t":35,"l":0,"b":0})
    text = str(filtered_points.iloc[0]['ssid']) + ' is the corresponding SSID'
    fig.update_layout(title_text=text)
    return fig

#Update Channel barchart 
@app.callback(
    Output('ip-channel-bar', 'figure'),
    Input('ip-menu', 'value'))
def update_figure(selected_ssid):
    conn = sqlite3.connect('./data/data.db')
    points = pd.read_sql('SELECT * FROM data', conn)
    conn.close() 
    filtered_points = points.drop(points[points.ip != selected_ssid].index)
    fig = go.Figure(data=go.Bar(y=filtered_points.groupby('channel')['channel'].count(), x=sorted(filtered_points['channel'].unique()), width=0.8))
    fig.update_layout(title_text='Channel')
    return fig

#Update Signal barchart
@app.callback(
    Output('ip-signal-bar', 'figure'),
    Input('ip-menu', 'value'))
def update_figure(selected_ssid):
    conn = sqlite3.connect('./data/data.db')
    points = pd.read_sql('SELECT * FROM data', conn) 
    conn.close()
    filtered_points = points.drop(points[points.ip != selected_ssid].index)
    fig = go.Figure(data=go.Bar(y=filtered_points.groupby('strength')['strength'].count(), x=sorted(filtered_points['strength'].unique()), width=0.8))
    fig.update_layout(title_text='Signal Strength')
    return fig

#Update beacon barchart
@app.callback(
    Output('ip-beacon-bar', 'figure'),
    Input('ip-menu', 'value'))
def update_figure(selected_ssid):
    conn = sqlite3.connect('./data/data.db')
    points = pd.read_sql('SELECT * FROM data', conn) 
    conn.close()
    filtered_points = points.drop(points[points.ip != selected_ssid].index)
    fig = go.Figure(data=go.Bar(y=filtered_points.groupby('beacon')['beacon'].count(), x=sorted(filtered_points['beacon'].unique()), width=1.0))
    fig.update_layout(title_text='Time Since Last Beacon')
    return fig


#Update Error Histogram
@app.callback(
    Output('ip-error-histogram', 'figure'),
    Input('ip-menu', 'value'))
def update_figure(selected_ssid):
    conn = sqlite3.connect('./data/data.db')
    points = pd.read_sql('SELECT * FROM data', conn)
    conn.close() 
    filtered_points = points.drop(points[points.ip != selected_ssid].index)
    sorted_points = filtered_points.sort_values(['elat','elon'], ascending=False)
    fig = px.density_heatmap(sorted_points, x="elat", y="elon", marginal_x="histogram", marginal_y="histogram", text_auto=True)
    fig.update_layout(height=1000 ,margin={"r":0,"t":30,"l":0,"b":0})
    fig.update_layout(title_text='GNSS Error Histogram')
    return fig






#Run webpage

if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True, port=8050)


