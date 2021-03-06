from win32gui import *
import win32gui, win32api, win32con
import time

from coreexceptions import WindowNotFound
"""
My ignorance of design caused a problem here.
This module is small at first and is getting ugly as it grows.
Refactor it sometime
"""

def clickOnScreen(pos):
    win32api.SetCursorPos(pos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, pos[0], pos[1],0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, pos[0], pos[1],0,0)

titles = None

def getAllTitles(hwnd, lparam):
    if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
        titles.add(GetWindowText(hwnd))

def bringToForeground(hld):
    while GetForegroundWindow() != hld:
        win32api.keybd_event(win32con.VK_MENU, 0, \
                                 win32con.KEYEVENTF_EXTENDEDKEY, 0)
        win32gui.SetForegroundWindow(hld)
        win32api.keybd_event(win32con.VK_MENU, 0, \
                             win32con.KEYEVENTF_EXTENDEDKEY | \
                             win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.2)


def mouseEventOnWindow(hld, pos, times = 1, button = 1,
                       down = True, up = True):

    bringToForeground(hld)

    win32api.SetCursorPos(pos)
    time.sleep(0.3)

    if button == 1:
        EVENT_1 = win32con.MOUSEEVENTF_LEFTDOWN
        EVENT_2 = win32con.MOUSEEVENTF_LEFTUP
    elif button == 2:
        EVENT_1 = win32con.MOUSEEVENTF_RIGHTDOWN
        EVENT_2 = win32con.MOUSEEVENTF_RIGHTUP
    
    for i in range(times):
        if down:
            win32api.mouse_event(EVENT_1, pos[0], pos[1],0,0)
        if up:
            win32api.mouse_event(EVENT_2, pos[0], pos[1],0,0)


cursor_pos = (0, 0)
def avertCursor():
    global cursor_pos
    cursor_pos = win32gui.GetCursorPos()
    win32api.SetCursorPos((0, win32api.GetSystemMetrics(1)))

def revertCursor():
    global cursor_pos
    win32api.SetCursorPos(cursor_pos)



def isMaximized(hld):
    return win32con.SW_SHOWMAXIMIZED == \
           GetWindowPlacement(hld)[1]

def clickOnMaximizeButton(hld):
    rect = win32gui.GetWindowRect(hld)
    btn_pos = (rect[2]-70, rect[1]+10)
    mouseEventOnWindow(hld, btn_pos)

def clickOnMinimizeButton(hld):
    rect = win32gui.GetWindowRect(hld)
    btn_pos = (rect[2]-100, rect[1]+10)
    mouseEventOnWindow(hld, btn_pos)

def maximizeWindow(hld):
    if not hld: return
    win32gui.ShowWindow(hld, win32con.SW_MAXIMIZE)

def normalizeWindow(hld):
    if not hld: return
    win32gui.ShowWindow(hld, win32con.SW_NORMAL)

def minimizeWindow(hld):
    if not hld: return
    win32gui.ShowWindow(hld, win32con.SW_MINIMIZE)

orientation = 'tl'

ref = dict()
ref['tl'] = lambda r: (r[0], r[1])
ref['tr'] = lambda r: (r[2], r[1])
ref['bl'] = lambda r: (r[0], r[3])
ref['br'] = lambda r: (r[2], r[3])

def setOrientation(flag = 'tl'):
    global orientation
    orientation = flag

def getReference(wnd):
    rect = GetWindowRect(wnd)
    return ref[orientation](rect)

def ScreenToWindow(wnd, pos):
    point = getReference(wnd)
    return (pos[0] - point[0], pos[1] - point[1])

def WindowToScreen(wnd, pos):
    point = getReference(wnd)
    return (point[0] + pos[0], point[1] + pos[1])

def getWindowHandle(title):
    """raises WindowNotFound"""

    global titles
    titles = set()
    EnumWindows(getAllTitles, 0)

    try:
        title = title.decode('utf-8', errors = "ignore")
    except UnicodeDecodeError:
        title = title.decode('utf-16', errors = "ignore")

    for t in titles:
        ut = t.decode('gb2312', errors = 'ignore')
        if title in ut:
            h = FindWindow(None, t)
            if h: return h

    raise WindowNotFound(title)

def clickInsideWindow(title, pos_relative, times = 1, button = 1):
    wnd = getWindowHandle(title)
    pos = WindowToScreen(wnd, pos_relative)
    mouseEventOnWindow(wnd, pos, times, button)

def mouseDownInsideWindow(title, pos_relative, button = 1):
    wnd = getWindowHandle(title)
    pos = WindowToScreen(wnd, pos_relative)
    mouseEventOnWindow(wnd, pos, button = button, up = False)

def mouseUpInsideWindow(title, pos_relative, button = 1):
    wnd = getWindowHandle(title)
    pos = WindowToScreen(wnd, pos_relative)
    mouseEventOnWindow(wnd, pos, button = button, down = False)

if __name__ == '__main__':
    normalizeWindow(getWindowHandle("winutil.py"))
