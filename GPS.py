#!/usr/bin/python

import serial
import pynmea2
from Logger import Logger


class GPS:
    def __init__(self, debug=False):
        # venusGPS = serial.Serial("/dev/ttyUSB0",baudrate=9600,timeout=5)
        self.logger = Logger("GPS", debug)
        self.logger.log("Initiating GPS with debugging {}".format("True" if debug else "False"))
        self.venusGPS = serial.Serial("/dev/ttySOFT0", baudrate=9600, timeout=5)
        self.venusGPS.reset_input_buffer()
        self.venusGPS.flush()
        self.lastsMessage = ""

    # nmea:
    # $GPGGA,timestamp,lat,n,lon,w,fix,numsats,hdop,altitude,m,geoid,m,time,dgps,checksum
    def GetLatestGPS(self):
        nmeaString = self.venusGPS.readline()
        nmeaString = nmeaString.decode(errors='ignore')
        # print(">{}<".format(nmeaString))
        try:
            msg = pynmea2.parse(nmeaString)
            self.lastsMessage = "{:.5f},{:.5f},{:.2f}\n".format(msg.latitude, msg.longitude, msg.altitude)  # f.write("{:.5f},{:.5f},{:.2f}\n".format(msg.latitude, msg.longitude, msg.altitude))

            self.venusGPS.reset_input_buffer()
            self.venusGPS.flush()
            return self.lastsMessage
        except:
            self.logger.log("Exception. Sending last message... ", self.lastsMessage)
            return self.lastsMessage


'''
nmeaParsed = pynmea2.parse(nmeaString);
'''
