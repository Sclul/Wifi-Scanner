from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
import os

app = Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=10*1000, # in milliseconds
        n_intervals=0
    )
])



ssid = os.environ["SSID"]


@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    points = pd.read_csv('/app/track_points.csv')

    points = points.drop(points[points.ssid != ssid].index)

    fig = go.Figure(go.Densitymapbox(lat=points.lat, lon=points.lon, z=points.strength,
                                 radius=10))

    fig.update_geos(fitbounds="locations")
    fig.update_layout(mapbox_style="open-street-map", mapbox_center_lat=52.5156451, mapbox_center_lon=13.3256412, mapbox_zoom=16)
    fig.update_layout(height=1000 ,margin={"r":0,"t":0,"l":0,"b":0})
    return fig








app.run_server(host='0.0.0.0',debug=True, port=8050)

