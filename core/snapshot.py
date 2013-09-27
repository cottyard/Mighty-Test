import win32api, win32con, win32gui, win32clipboard
import time, os
import math, operator
from PIL import ImageGrab, Image
import winutil

def snapWidgetFromPoint(point, path):
    wnd = win32gui.WindowFromPoint(point)
    rect = win32gui.GetWindowRect(wnd)
    i = ImageGrab.grab(rect)
    i.save(path, "PNG")
    return (rect[0], rect[1])

def snapWindow(title, filepath):
    hld = winutil.getWindowHandle(title)
    normalWindow = not winutil.isMaximized(hld)
    winutil.maximizeWindow(hld)
    winutil.bringToForeground(hld)
    winutil.avertCursor()
    time.sleep(2)
    
    # use PrintScreen to capture app window
    # the combination Alt + PrintScreen is problematic on some win 7 versions
    

    win32api.keybd_event(win32con.VK_SNAPSHOT, 0, 0, 0)
    win32api.keybd_event(win32con.VK_SNAPSHOT, 0, win32con.KEYEVENTF_KEYUP, 0)
    
    """
    # Alt + PrintScreen to capture app window
    win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)
    time.sleep(1) # Hold Alt for one sec so that window appearance stablizes

    win32api.keybd_event(win32con.VK_SNAPSHOT, 0, 0, 0)
    win32api.keybd_event(win32con.VK_SNAPSHOT, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.5)
    
    win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)

    time.sleep(0.1)
    """
    
    time.sleep(2) # Wait long enough for the clipboard to accept the new image
    
    winutil.revertCursor()

    r = win32gui.GetWindowRect(hld)
    
    if normalWindow:
        winutil.normalizeWindow(hld)
        
    # Carve out the window and save sto file
    im = ImageGrab.grabclipboard()
    w, h = im.size

    CROP_BORDER = 10

    im.crop((r[0] + CROP_BORDER, r[1] + 30,
             r[2] - CROP_BORDER, r[3] - CROP_BORDER)) \
      .save(filepath, 'PNG')

tolerance = 10.0

def compareSnapshots(filename, tempfile):
    o = Image.open(filename).histogram()
    t = Image.open(tempfile).histogram()
    
    result = math.sqrt(reduce(operator.add,
                              map(lambda a,b: (a-b)**2, o, t))/len(o))
    return result < float(tolerance)

if __name__ == '__main__':
    print compareSnapshots("checkpoint.gif", "filter_newfilter.gif")
