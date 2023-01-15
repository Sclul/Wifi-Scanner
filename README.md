# Wifi-Scanner

Progress in work.

Formula for Distance of the AP in an open field converted to GPS-coordinates (that are accurat enough in Berlin)
filtered_points['strength'] = filtered_points['strength'].apply(lambda x: (math.pow(10, ((27.55 - (20 * math.log10(2440)) + math.fabs(x))/ 20.0)))*0.00001466666)

## Todo

1. Add more Stuff to the data
2. Convert data from .csv to sql
3. Somehow visulize the inaccuracies (try boxing)
