from main import gps, mpl, temp


def getData():
    gpsData = gps.GetLatestGPS()
    altData = mpl.getAltimeterData()
    tempData = temp.read_temp()
    return gpsData, altData[1]
