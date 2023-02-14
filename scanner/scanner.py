# The code function shown above is used to scan for nearby wireless access points (APs) and store the data into a SQLite database.
# The first function establishes a connection to the database and creates a table if it does not already exist. It then stores the data from the table in an output array.
# The next function uses the GPSDClient library to get the current GPS coordinates. It also stores the current time in seconds.
# The third function uses the subprocess library to run the “iwlist” command on the specified wireless interface. This command lists all of the nearby APs. The output is then split into separate lines and stored in a data array.
# The fourth function iterates through the data array to find the IP address, channel, signal strength, and SSID of each AP. It then stores this information in an ap array. It also stores the current timestamp and the current GPS coordinates.
# The fifth function combines the ap array and the output array into one array and stores it in the database.
# The sixth and final function prints the output from the database to the console.



import subprocess
import numpy
import time
import os
import random
import sqlite3
import pandas as pd 

from gpsdclient import GPSDClient


random.seed(1)

wifiInterfaceName = os.environ["WIFI_INTERFACE_NAME"]

#Connect to database
conn = sqlite3.connect('/app/data/data.db')
conn.execute('CREATE TABLE IF NOT EXISTS data (ip TEXT, channel INTEGER, strength INTEGER, ssid TEXT, time TEXT, lat REAL, lon REAL, elat REAL, elon REAL, beacon INTEGER)')
outputArray = numpy.array(pd.read_sql('SELECT * FROM data', conn)) 

last_run_time = time.time()


with GPSDClient() as client:

    #Gets GPS-Data
    for result in client.dict_stream(convert_datetime=True, filter=["TPV"]):

        current_time = time.time() # Get the current time in seconds
        # Calculate the time since the code last ran
        delta_time = current_time - last_run_time
        # Print the time since the code last ran
        print("Time since code last ran: {:.2f} seconds".format(delta_time))
        last_run_time = current_time

    #Get all AP-Data

        process = subprocess.run(["iwlist", wifiInterfaceName, "scan"],
                            check=True,
                            stdout=subprocess.PIPE,
                            universal_newlines=True)

        print('process done')
    


        data = process.stdout.split("\n")

        #Gets IP, channel, signalStrangth, SSID out of the text of the list
        #Finds out how many different APs there are
        apcells = 0
        for x in range(len(data)):
            if "Cell" in data[x]:
                apcells = apcells + 1

        ap = numpy.ones((apcells, 10), dtype=object)

        timeStamp = int(time.time())

        apCellCounter = -1

        #Goes through the list and copies the requiered text if "" is in the same list.
        for x in range(len(data)):

            if "Address:" in data[x]:
                apCellCounter = apCellCounter + 1
                ap[apCellCounter, 0] = ((data[x])[29:46])
            if "Channel:" in data[x]:
                ap[apCellCounter, 1] = (int((data[x])[28:]))
            if "Signal level" in data[x]:
                ap[apCellCounter, 2] = (int((((data[x])[47:].replace("dBm","")).replace("=","")).strip()))
            if "SSID:" in data[x]:
                ap[apCellCounter, 3] = ((data[x])[27:].replace("\"",""))

            ap[apCellCounter, 4] = timeStamp



            ap[apCellCounter, 5] = result.get("lat", "n/a")
            ap[apCellCounter, 6] = result.get("lon", "n/a")
            ap[apCellCounter, 7] = result.get("epx", "n/a")
            ap[apCellCounter, 8] = result.get("epy", "n/a")            
        

            if "Last beacon:" in data[x]:
                ap[apCellCounter, 9] = int((data[x])[40:].replace("ms ago",""))

            #Deletes every row, where the last beacon was sent more then the last iwlist scan ago
            nap=ap[ap[:,9]< delta_time*1000]



        # Puts the row into the array
        outputArray=numpy.vstack([outputArray, nap]) 

        #Makes Array into a dataframe and adds it to the database
        df = pd.DataFrame(outputArray, columns=['ip','channel','strength','ssid','time','lat','lon','elat','elon','beacon'])
        conn = sqlite3.connect('/app/data/data.db')
        df.to_sql('data', conn, if_exists='replace', index=False)


        #Prints output to console
        cursor = conn.cursor() 
        cursor.execute("SELECT * FROM data") 
        rows = cursor.fetchall() 
        for row in rows: 
            print(row) 




        
conn.close()

