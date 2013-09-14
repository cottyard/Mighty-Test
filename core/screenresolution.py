import win32api, win32con

def getRes():
    i = 0
    while i < 10:
        try:
            winDev = win32api.EnumDisplayDevices(DevNum = i)
            winSettings = win32api.EnumDisplaySettings(winDev.DeviceName, \
                                                       win32con.ENUM_CURRENT_SETTINGS)
        except Exception:
            i += 1
            continue
        else:
            return (winSettings.PelsWidth, winSettings.PelsHeight)
            

    raise Exception("can't find a display device")

def convert(res):
    winDev = win32api.EnumDisplayDevices(DevNum = 0)
    winSettings = win32api.EnumDisplaySettings(winDev.DeviceName, \
                                               win32con.ENUM_CURRENT_SETTINGS)

    winSettings.PelsWidth = res[0]
    winSettings.PelsHeight = res[1]

    win32api.ChangeDisplaySettingsEx(winDev.DeviceName, winSettings)
