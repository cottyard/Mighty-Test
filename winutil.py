from win32gui import *
import win32gui, win32api, win32con
import time

titles = set()

def getAllTitles(hwnd, lparam):
    if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
        titles.add(GetWindowText(hwnd))


def clickOnWindow(hld, pos, times = 1):
    cursor_pos = win32gui.GetCursorPos()
    win32api.SetCursorPos(pos)

    
    # win32gui.SetActiveWindow(hld)
    # Press Alt or SetForegroundWindow() fails on occassions. I don't know why.
    if win32gui.GetForegroundWindow() != hld:
        win32api.keybd_event(win32con.VK_MENU, 0, \
                             win32con.KEYEVENTF_EXTENDEDKEY, 0)
        win32gui.SetForegroundWindow(hld)
        win32api.keybd_event(win32con.VK_MENU, 0, \
                             win32con.KEYEVENTF_EXTENDEDKEY | \
                             win32con.KEYEVENTF_KEYUP, 0)
    
    time.sleep(0.2)
    for i in range(times):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, pos[0], pos[1],0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, pos[0], pos[1],0,0)

    win32api.SetCursorPos(cursor_pos)

cursor_pos = (0, 0)
def avertCursor():
    global cursor_pos
    cursor_pos = win32gui.GetCursorPos()
    # don't move to the bottom right corner of the screen
    # will cause windows 7 to show desktop
    win32api.SetCursorPos((0, win32api.GetSystemMetrics(1)))

def revertCursor():
    global cursor_pos
    win32api.SetCursorPos(cursor_pos)

def bringToForeground(hld):
    win32gui.SetForegroundWindow(hld)

def isMaximized(hld):
    return win32con.SW_SHOWMAXIMIZED == \
           GetWindowPlacement(hld)[1]

def clickOnMaximizeButton(hld):
    rect = win32gui.GetWindowRect(hld)
    btn_pos = (rect[2]-70, rect[1]+10)
    clickOnWindow(hld, btn_pos)

def clickOnMinimizeButton(hld):
    rect = win32gui.GetWindowRect(hld)
    btn_pos = (rect[2]-100, rect[1]+10)
    clickOnWindow(hld, btn_pos)

def maximizeWindow(hld):
    if not hld: return
    if isMaximized(hld):
        return False
    clickOnMaximizeButton(hld)
    return True

def normalizeWindow(hld):
    if not hld: return
    if not isMaximized(hld):
        return False
    clickOnMaximizeButton(hld)
    return True

def minimizeWindow(hld):
    if not hld: return
    clickOnMinimizeButton(hld)
    return True

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
    EnumWindows(getAllTitles, 0)
    for t in titles:
        if title in t:
            return FindWindow(None, t)
    return None

def clickInsideWindow(title, pos_relative, times = 1):
    wnd = getWindowHandle(title)
    if not wnd:
        return False
    pos = WindowToScreen(wnd, pos_relative)
    clickOnWindow(wnd, pos, times)
    return True

if __name__ == '__main__':
    normalizeWindow(getWindowHandle("winutil.py"))
