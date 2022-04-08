# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import os #Initializes soft_uart
os.system("insmod //home/pi/soft_uart/soft_uart.ko gpio_tx=17 gpio_rx=18")
# pylint: disable=wrong-import-position
import time
from GPS import GPS
from Logger import Logger
from adafruit_rockblock import RockBlock
from mpl3115a2 import MPL3115A2
from ONEWIRE import OneWire
from extraDef import getData

import serial

debug = False
tsym = 'F'
port = "/dev/serial0"
baud = 19200
logger = Logger("RockBlock", debug)
# uart = serial.Serial("/dev/serial0", 19200)
uart = serial.Serial(port)
# uart = board.UART()
# uart.baudrate = 19200

# via USB cable
# import serial
# uart = serial.Serial("/dev/ttyUSB0", 19200)

gps = GPS(debug)
mpl = MPL3115A2(tsym, debug)
temp = OneWire(tsym, debug)

logger.log("Initiating Rock Block on port " + str(port) + ", with baud rate " + str(baud) + ", and debugging " + "True" if debug else "False")
rb = RockBlock(uart)
logger.log("Model: ", str(rb.model))
logger.log("System Time: ", str(rb.system_time))
logger.log("Signal Quality: ", str(rb.signal_quality))

time.sleep(8)
status = (-1)
retry = 0
counter = 0
while 1:
    # set the text
    data = getData()
    logger.log("Setting Text... ", data)
    rb.text_out = data

    if counter % 180 == 0:  # Send every
        # try a satellite Short Burst Data transfer
        status = rb.satellite_transfer()
        logger.log("Talking to satellite... ", str(status))  # loop as needed

    if status[0] > 8 and counter % 10 == 0:
        status = rb.satellite_transfer()
        logger.log(str(retry), str(status))
        logger.log("Signal Quality: ", str(rb.signal_quality))
        data = getData()
        logger.log("Setting Text... ", data)
        rb.text_out = data
        retry += 1

    if 8 >= status[0] > -1:
        logger.log("Sent!")
        status[0] = -1
        retry = 0

    time.sleep(1)  # Sleep for 1 second

