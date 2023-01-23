import plotly.graph_objects as go # or plotly.express as px
import sqlite3
import pandas as pd

fig = go.Figure()


def binlat (lat, error):
    error_degree = error * 0.00001466666
    list = [lat+error_degree, lat+error_degree, lat-error_degree, lat-error_degree, lat+error_degree, None]
    return list

def binlon (lon, error):
    error_degree = error * 0.00001466666
    list = [lon+error_degree, lon-error_degree, lon-error_degree, lon+error_degree, lon+error_degree, None]
    return list

conn = sqlite3.connect('data.db')
points = pd.read_sql('SELECT * FROM data', conn) 
conn.close()
filtered_points = points.drop(points[points.ssid != '2Girls1Router'].index)
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
        opacity=0.5
    ))
    #Create mid rectangle
fig.add_trace(go.Scattermapbox(
        lon = lon2,
        lat = lat2,
        mode = 'lines',
        line = dict(color = 'yellow', width = 2),
        opacity=0.5
    ))
    #Create bot rectangle
fig.add_trace(go.Scattermapbox(
        lon = lon3,
        lat = lat3,
        mode = 'lines',
        line = dict(color = 'red', width = 2),
        opacity=0.5
    ))
fig.update_layout(
    mapbox = {
        'style': "open-street-map",
        'center': { 'lon': 13.3256412, 'lat': 52.5156451},
        'zoom': 16},


    height=1000,
    margin = {'l':0, 'r':100, 'b':0, 't':0})


import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])




if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True, port=8050)
