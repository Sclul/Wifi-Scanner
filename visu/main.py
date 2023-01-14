
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


app = Dash(__name__)

points = pd.read_csv('/app/track_points.csv')
fig = go.Figure(go.Densitymapbox(lat=points.lat, lon=points.lon, z=points.strength,radius=10))
fig.update_geos(fitbounds="locations")
fig.update_layout(mapbox_style="open-street-map", mapbox_center_lat=52.5156451, mapbox_center_lon=13.3256412, mapbox_zoom=16)
fig.update_layout(height=1000 ,margin={"r":0,"t":0,"l":0,"b":0})

app.layout = html.Div([

        html.Div([
            dcc.Dropdown(
                points['ssid'].unique(),
                'eduroam',
                id='ssid-menu'
            ),
            dcc.RadioItems(
                ['Linear', 'Log'],
                'Linear',
                id='xaxis-type',
                inline=True
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
    dcc.Graph(
        id='heatmap'
  
    ),
    dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
])


#Update heatmap
@app.callback(
    Output('heatmap', 'figure'),
    Input('ssid-menu', 'value'))
def update_figure(selected_ssid):
    points = pd.read_csv('/app/track_points.csv')
    filtered_points = points.drop(points[points.ssid != selected_ssid].index)
    fig = go.Figure(go.Densitymapbox(lat=filtered_points.lat, lon=filtered_points.lon, z=filtered_points.strength,radius=10))
    fig.update_geos(fitbounds="locations")
    fig.update_layout(mapbox_style="open-street-map", mapbox_center_lat=52.5156451, mapbox_center_lon=13.3256412, mapbox_zoom=16)
    fig.update_layout(height=1000 ,margin={"r":0,"t":0,"l":0,"b":0})
    return fig

@app.callback(
    Output('ssid-menu', 'options'),
    Input('interval-component', 'n_intervals'))
def update_ssid_menu(n):
    data = pd.read_csv('/app/track_points.csv')
    return data['ssid'].unique().tolist()



if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True, port=8050)