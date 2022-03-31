# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# pylint: disable=wrong-import-position
import time
from GPS import GetLatestGPS
from Logger import Logger
# CircuitPython / Blinka
# import board

import serial
debug = False
port = "/dev/serial0"
baud = 19200
logger = Logger("RockBlock", debug)
#uart = serial.Serial("/dev/serial0", 19200)
uart = serial.Serial(port)
#uart = board.UART()
#uart.baudrate = 19200

# via USB cable
# import serial
# uart = serial.Serial("/dev/ttyUSB0", 19200)

from adafruit_rockblock import RockBlock

logger.log("Initiating Rock Block on port " + str(port) + ", with baud rate " + str(baud) + ", and debugging " + "True" if debug else "False")
rb = RockBlock(uart)
logger.log("Model: ", str(rb.model))
logger.log("System Time: ", str(rb.system_time))
logger.log("Signal Quality: ", str(rb.signal_quality))

time.sleep(8)
while 1:
    # set the text
    gpsData = GetLatestGPS()
    logger.log("Setting Text... ", gpsData)
    rb.text_out = gpsData

    # try a satellite Short Burst Data transfer
    status = rb.satellite_transfer()
    logger.log("Talking to satellite... ", str(status))
    # loop as needed
    retry = 0
    while status[0] > 8:
        time.sleep(10)
        status = rb.satellite_transfer()
        logger.log(str(retry), str(status))
        gpsData = GetLatestGPS()
        logger.log("Setting Text... ", gpsData)
        rb.text_out = gpsData
        retry += 1

    logger.log("Sent!")
    time.sleep(180) #Sleep for 3 minutes