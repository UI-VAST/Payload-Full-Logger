from GPS import GetLatestGPS
from main import mpl, temp


def getData():
    gpsData = GetLatestGPS()
    altData = mpl.getAltimeterData()
    tempData = temp.read_temp()
    return gpsData, altData[1]
