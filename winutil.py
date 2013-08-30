from win32gui import *
import win32gui, win32api, win32con
import time

titles = set()

def getAllTitles(hwnd, lparam):
    if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
        titles.add(GetWindowText(hwnd))

def clickOnWindow(hld, pos):
    cursor_pos = win32gui.GetCursorPos()
    win32api.SetCursorPos(pos)

    win32gui.SetForegroundWindow(hld)
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, pos[0], pos[1],0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, pos[0], pos[1],0,0)

    win32api.SetCursorPos(cursor_pos)

def maximizeWindow(hld):
    rect = win32gui.GetWindowRect(hld)
    btn_pos = (rect[2]-70, rect[1]+10)
    clickOnWindow(hld, btn_pos)


def ScreenToWindow(wnd, pos):
    rect = GetWindowRect(wnd)
    return (pos[0] - rect[0], pos[1] - rect[1])

def WindowToScreen(wnd, pos):
    rect = GetWindowRect(wnd)
    return (rect[0] + pos[0], rect[1] + pos[1])

def getWindowHandle(title):
    EnumWindows(getAllTitles, 0)
    for t in titles:
        if title in t:
            return FindWindow(None, t)
    return None

if __name__ == '__main__':
    maximizeWindow(getWindowHandle("winutil.py"))
