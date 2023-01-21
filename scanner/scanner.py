import subprocess
import numpy
import time
import os
import random

from gpsdclient import GPSDClient


random.seed(1)

wifiInterfaceName = os.environ["WIFI_INTERFACE_NAME"]

outputArray = numpy.genfromtxt('/app/data/data.csv', delimiter=",", dtype="str")


last_run_time = time.time()


with GPSDClient() as client:


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
                ap[apCellCounter, 9] = ((data[x])[40:].replace("ms ago",""))


        print('array done')


        outputArray=numpy.vstack([outputArray, ap]) #super inefficient

        numpy.savetxt("/app/data/data.csv", outputArray, fmt='%1s', delimiter=",")
