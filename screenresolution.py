import win32api, win32con

def getRes():
    winDev = win32api.EnumDisplayDevices(DevNum = 0)
    winSettings = win32api.EnumDisplaySettings(winDev.DeviceName, \
                                               win32con.ENUM_CURRENT_SETTINGS)
    return (winSettings.PelsWidth, winSettings.PelsHeight)

def convert(res):
    winDev = win32api.EnumDisplayDevices(DevNum = 0)
    winSettings = win32api.EnumDisplaySettings(winDev.DeviceName, \
                                               win32con.ENUM_CURRENT_SETTINGS)

    winSettings.PelsWidth = res[0]
    winSettings.PelsHeight = res[1]

    win32api.ChangeDisplaySettingsEx(winDev.DeviceName, winSettings)
