import plotly.graph_objects as go # or plotly.express as px


fig = go.Figure()

# Create a green rectangle
fig.add_trace(go.Scattermapbox(
    lon = [-118.50, -118.50, -117.50, -117.50, -118.50, None, -117.50, -117.50, -116.50, -116.50, -117.50],
    lat = [34.50, 35.50, 35.50, 34.50, 34.50, None, 34.50, 35.50, 35.50, 34.50, 34.50],
    mode = 'lines',
    line = dict(color = 'green', width = 2),
    fill = 'toself'
))

# Create a red rectangle
fig.add_trace(go.Scattermapbox(
    lon = [-118.50, -118.50, -117.50, -117.50, -118.50, None, -117.50, -117.50, -116.50, -116.50, -117.50],
    lat = [34.50, 35.50, 35.50, 34.50, 34.50, None, 34.50, 35.50, 35.50, 34.50, 34.50],
    mode = 'lines',
    line = dict(color = 'red', width = 2),
    fill = 'toself'
))




fig.update_layout(
    mapbox = {
        'style': "stamen-terrain",
        'center': { 'lon': -73.6, 'lat': 45.5},
        'zoom': 12, 'layers': [{
            'source': {
                'type': "FeatureCollection",
                'features': [{
                    'type': "Feature",
                    'geometry': {
                        'type': "MultiPolygon"

                    }
                }]
            },
            'type': "fill", 'below': "traces", 'color': "royalblue"}]},
    margin = {'l':0, 'r':0, 'b':0, 't':0})


import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])




if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True, port=8050)
