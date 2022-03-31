#!/usr/bin/python

import serial
import time
import pynmea2
import os
import datetime
import threading

def timestamp():
    return str(datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S"))

#venusGPS = serial.Serial("/dev/ttyUSB0",baudrate=9600,timeout=5)
venusGPS = serial.Serial("/dev/ttySOFT0",baudrate=9600,timeout=5)

logPath = os.path.join(os.getcwd(),'log')
if(not os.path.exists(logPath)):
    os.mkdir(logPath)
gpsFile = os.path.join(logPath,'gps' + timestamp() + '.txt')
with open(gpsFile,'a') as f:
    f.write("Begin File-------------------------------------\n")

# nmea:
# $GPGGA,timestamp,lat,n,lon,w,fix,numsats,hdop,altitude,m,geoid,m,time,dgps,checksum
def begin():
    venusGPS.reset_input_buffer()
    venusGPS.flush()
    while 1:
        nmeaString = venusGPS.readline()
        #print("{}".format(nmeaString))
        try:
            #pynmea2.parse("{}".format(nmeaString))
            with open(gpsFile,'a') as f:
                f.write("{}\n".format(nmeaString))

            venusGPS.reset_input_buffer()
            venusGPS.flush()
            time.sleep(3)
        except:
            print("Exception...")
            continue

        '''
        nmeaParsed = pynmea2.parse(nmeaString);
        '''

def GetLatestGPS():
    with open(gpsFile,'r') as f:
        for latest in f:
            pass
    print("Latest: {}\n".format(latest[19:58]))
    return "{}.".format(latest[19:58])

# this file is imported in IridiumTransmitter.py,
# which runs the entire file,
# and launches this thread:
threading.Thread(target=begin).start()