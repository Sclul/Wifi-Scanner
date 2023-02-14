# Wifi-Scanner
Install both docker and docker-compose beforehand.
##  Starting GNSS
1. sudo apt install gpsd
2. sudo su
3. gpsd -D 5 -N -n /dev/ttyUSB0

## Start Scanner and visualization
1. Edit the three rows in docker-compose.yml according to their comments.
2. docker-compose up

## Use Websites
1. Static map of SSID specified in docker-compose.yml on 0.0.0.0:8051
2. Live map on 0.0.0.0:8050
3. Left tab to visulize SSIDs, right tab to visulize specific APs/MAC-Addresses.
4. Select SSID/AP from the dropdown menu.


