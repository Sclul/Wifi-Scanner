# Wifi-Scanner

Progress in work.



## Configuration
1. Edit the three rows in docker-compose according to their comments
2. docker-compose up
3. Live on Port 8050, Maps on Port 8051 


##  Starting GNSS
1. sudo apt install gpsd
2. sudo su
3. sudo systemctl stop gpsd.socket 
4. gpsd -D 5 -N -n /dev/ttyUSB0
