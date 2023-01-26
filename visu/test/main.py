import plotly.graph_objects as go # or plotly.express as px
import sqlite3
import pandas as pd
import math
import os

latfac = 0.000009
lonfac = 0.00001466

ssid = os.environ["SSID_NAME"]

def binlat (lat, error):
    error_degree = error * latfac
    list = [lat+error_degree, lat+error_degree, lat-error_degree, lat-error_degree, lat+error_degree, None]
    return list

def binlon (lon, error):
    error_degree = error * lonfac
    list = [lon+error_degree, lon-error_degree, lon-error_degree, lon+error_degree, lon+error_degree, None]
    return list


def binlat1 (lat, strength):
    strenght_degree = math.pow(10, ((27.55 - (20 * math.log10(2440)) + math.fabs(strength))/ 20.0))*latfac
    y_coord = []
    for i in range(0, 361): 
        y_coord.append(lat + strenght_degree * math.sin(math.radians(i)))
    y_coord.append(None)
    return y_coord

def binlon1 (lon, strength):
    strenght_degree = math.pow(10, ((27.55 - (20 * math.log10(2440)) + math.fabs(strength))/ 20.0))*lonfac
    x_coord = []
    for i in range(0, 361): 
        x_coord.append(lon + strenght_degree * math.cos(math.radians(i)))
    x_coord.append(None)
    return x_coord



conn = sqlite3.connect('./data/data.db')
points = pd.read_sql('SELECT * FROM data', conn) 
conn.close()
filtered_points = points.drop(points[points.ssid != ssid].index)

####################################

fig1 = go.Figure()

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
fig1.add_trace(go.Scattermapbox(
        lon = lon1,
        lat = lat1,
        mode = 'lines',
        line = dict(color = 'green', width = 2),
        opacity=0.5
    ))
    #Create mid rectangle
fig1.add_trace(go.Scattermapbox(
        lon = lon2,
        lat = lat2,
        mode = 'lines',
        line = dict(color = 'yellow', width = 2),
        opacity=0.5
    ))
    #Create bot rectangle
fig1.add_trace(go.Scattermapbox(
        lon = lon3,
        lat = lat3,
        mode = 'lines',
        line = dict(color = 'red', width = 2),
        opacity=0.5
    ))
fig1.update_layout(
    mapbox = {
        'style': "open-street-map",
        'center': { 'lon': 13.3256412, 'lat': 52.5156451},
        'zoom': 16},


    height=1000,
    margin = {'l':0, 'r':150, 'b':0, 't':50})
fig1.update_layout(title_text='GNSS Error Range of ' + ssid)
##################################

fig2 = go.Figure()

lat11 = []
lon11 = []

for row in filtered_points.iterrows():
    if row[1]['lat'] != 'n/a':
        lat11 = lat11+binlat1(float(row[1]['lat']),float(row[1]['strength'])) 
        lon11 = lon11+binlon1(float(row[1]['lon']),float(row[1]['strength']))


fig2.add_trace(go.Scattermapbox(
        lon = lon11,
        lat = lat11,
        mode = 'lines',
        line = dict(color = 'blue', width = 2),
        opacity=0.5
    ))

fig2.update_layout(
    mapbox = {
        'style': "open-street-map",
        'center': { 'lon': 13.3256412, 'lat': 52.5156451},
        'zoom': 16},


    height=1000,
    margin = {'l':0, 'r':150, 'b':0, 't':50})

fig2.update_layout(title_text='Range Approximation of ' + ssid)








import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2)
])




if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True, port=8050)
