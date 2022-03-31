import smbus
import time
from Logger import Logger


class MPL3115A2:
    def __init__(self, ForC='F', debug=False):
        self.logger = Logger("MPL3115A2", debug)
        self.logger.log("Initiating MPL3115A2 with temperature logging mode in {0} and debugging {1}".format("Fahrenheit" if ForC == 'F' else "Celsius", "True" if debug else "False"))
        self.ForC = 'F' if ForC.upper() == 'F' else 'C'
        self.bus = smbus.SMBus(1)
        # MPL3115A2 address, 0x60(96)p
        # Select control register, 0x26(38)
        # 0xB9(185) Active mode, OSR = 128, Altimeter mode
        self.bus.write_byte_data(0x60, 0x26, 0xB9)

        # MPL3115A2 address, 0x60(96)
        # Select data configuration register, 0x13(19)
        # 0x07(07) Data ready event enabled for altitude, pressure, temperature
        self.bus.write_byte_data(0x60, 0x13, 0x07)

    def getAltimeterData(self):
        # MPL3115A2 address, 0x60(96)
        # Select control register, 0x26(38)
        # 0xB9(185) Active mode, OSR = 128, Altimeter mode
        self.bus.write_byte_data(0x60, 0x26, 0xB9)

        # MPL3115A2 address, 0x60(96)
        # Read data back from 0x00(00), 6 bytes
        # status, tHeight MSB1, tHeight MSB, tHeight LSB, temp MSB, temp LSB
        data = self.bus.read_i2c_block_data(0x60, 0x00, 6)

        # Convert the data to 20-bits
        tHeight = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
        temp = ((data[4] * 256) + (data[5] & 0xF0)) / 16
        altitude = tHeight / 16.0
        if self.ForC != 'F':
            temp = temp / 16.0

        # MPL3115A2 address, 0x60(96)
        # Select control register, 0x26(38)
        # 0x39(57) Active mode, OSR = 128, Barometer mode
        self.bus.write_byte_data(0x60, 0x26, 0x39)
        time.sleep(1)

        # MPL3115A2 address, 0x60(96)
        # Read data back from 0x00(00), 4 bytes
        # status, pres MSB1, pres MSB, pres LSB
        data = self.bus.read_i2c_block_data(0x60, 0x00, 4)

        # Convert the data to 20-bits
        pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
        pressure = (pres / 4.0) / 1000.0

        self.logger.log("Altitude: ", "{:.2f} m".format(altitude))
        self.logger.log("Pressure: ", "{:.2f} kPa".format(pressure))
        self.logger.log("Temperature: ", "{:.2f} {}".format(temp, self.ForC))

        return altitude, temp, pressure

# # Output to SD Card
# filename = "test.txt"
# file = open(filename, "w")
# file.write("Pressure : %.2f kPa" %pressure)
# file.write("Altitude : %.2f m" %altitude)
# file.write("Temperature in Celsius : %.2f C" %cTemp)
# file.close()
