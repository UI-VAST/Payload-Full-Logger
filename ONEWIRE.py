import os
import glob
import time
from Logger import Logger


class OneWire:
    def __init__(self, ForC='F', debug=False):
        self.logger = Logger("OneWire", debug)
        self.logger.log("Initiating OneWire Temperature Probe with temperature logging mode in {0} and debugging {1}".format("Fahrenheit" if ForC == 'F' else "Celsius", "True" if debug else "False"))
        self.ForC = 'F' if ForC.upper() == 'F' else 'C'

        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        self.device_file = device_folder + '/w1_slave'

    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()

        return lines

    def read_temp(self):
        lines = self.read_temp_raw()
        if len(lines) < 2:
            self.logger.log("OneWire Probe disconnected.")
            return None
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')

        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp = float(temp_string) / 1000.0
            if self.ForC == 'F':
                temp = temp * 9.0 / 5.0 + 32.0

            self.logger.log("Temperature: ", "{:.2f} {}".format(temp, self.ForC))

            return temp

