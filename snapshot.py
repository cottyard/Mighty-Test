import win32api, win32con, win32gui, win32clipboard
import time, os
import math, operator
from PIL import ImageGrab, Image
import winutil

def snapWindow(title, filepath):
    hld = winutil.getWindowHandle(title)
    normalWindow = winutil.maximizeWindow(hld)
    winutil.bringToForeground(hld)

    time.sleep(0.5)
    
    # Alt + PrintScreen to capture app window
    win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)
    time.sleep(1) # Hold Alt for one sec so that window appearance stablizes

    win32api.keybd_event(win32con.VK_SNAPSHOT, 0, 0, 0)
    win32api.keybd_event(win32con.VK_SNAPSHOT, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.5)
    
    win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)

    time.sleep(0.1)

    if normalWindow:
        winutil.normalizeWindow(hld)

    # Crop title bar and save picture to file
    im = ImageGrab.grabclipboard()
    w, h = im.size
    im.crop((0, 25, w, h)) \
      .save(filepath, 'PNG')

def compareSnapshots(filename, tempfile):
    o = Image.open(filename).histogram()
    t = Image.open(tempfile).histogram()
    
    result = math.sqrt(reduce(operator.add,
                              map(lambda a,b: (a-b)**2, o, t))/len(o))
    return result == float(0)

if __name__ == '__main__':
    print compareSnapshots("f1.png", "f2.png")
