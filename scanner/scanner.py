import subprocess
import numpy
import time
import os
import random

from gpsdclient import GPSDClient


random.seed(1)

wifiInterfaceName = os.environ["WIFI_INTERFACE_NAME"]

outputArray = numpy.genfromtxt('/app/data/data.csv', delimiter=",", dtype="str")


with GPSDClient() as client:

    for result in client.dict_stream(convert_datetime=True, filter=["TPV"]):

    #Get all AP-Data

        time.sleep(1)

        process = subprocess.run(["iwlist", wifiInterfaceName, "scan"],
                            check=True,
                            stdout=subprocess.PIPE,
                            universal_newlines=True)


    


        data = process.stdout.split("\n")

        #Gets IP, channel, signalStrangth, SSID out of the text of the list
        #Finds out how many different APs there are
        apcells = 0
        for x in range(len(data)):
            if "Cell" in data[x]:
                apcells = apcells + 1

        ap = numpy.ones((apcells, 7), dtype=object)

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






        # with GPSDClient() as client:

           
            # # for result in client.dict_stream(convert_datetime=True, filter=["TPV"]):
            # print("Latitude: %s" % result.get("lat", "n/a"))
            # print("Longitude: %s" % result.get("lon", "n/a"))





            # #Temp GPS
            # ################################
            
            # lat = 52.513 + random.random()*0.005
            # lon = 13.323 + random.random()*0.008

            ap[apCellCounter, 5] = result.get("lat", "n/a")
            ap[apCellCounter, 6] = result.get("lon", "n/a")
        
            #################################



        outputArray=numpy.vstack([outputArray, ap]) #super inefficient

        numpy.savetxt("/app/data/data.csv", outputArray, fmt='%1s', delimiter=",")
