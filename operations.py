import os, time
import winutil
import snapshot
import screenresolution
        
class Click:
    def __init__(self, title = "", pos = (0, 0)):
        self.title = title
        self.pos = pos
        
    def play(self):
        if not winutil.clickInsideWindow(self.title, self.pos):
            print self.title + ' does not exist.'
            return
    def equals(self, another_click):
        return self.title == another_click.title and \
               self.pos == another_click.pos
    
    def script_out(self):
        return str((self.title, self.pos))
    
    def script_in(self, script):
        t = eval(script)
        self.title = t[0]
        self.pos = t[1]
        return self

class DoubleClick(Click):
    def play(self):
        if not winutil.clickInsideWindow(self.title, self.pos, 2):
            print self.title + ' does not exist.'
            return

class Interval:
    def __init__(self, interval = 0):
        self.interval = interval
        
    def play(self):
        time.sleep(self.interval)

    def script_out(self):
        return str(self.interval)
    
    def script_in(self, script):
        t = eval(script)
        self.interval = t
        return self

class CheckPoint:
    def __init__(self, title = "", filename = ""):
        self.title = title
        self.filename = filename

    def play(self):
        if not os.path.exists(os.path.realpath(self.filename)):
            snapshot.snapWindow(self.title, self.filename)
            return "check point image file " + self.filename + \
                   " doesn't exist and has been created"
            
        tempfile = 'snapshots/checkpoint.png'
        snapshot.snapWindow(self.title, tempfile)

        if not snapshot.compareSnapshots(self.filename, tempfile):
            return "checkpoint fails: " + tempfile + \
                   " is inconsistent with " + self.filename

        # delete temp file
        os.remove(os.path.realpath(tempfile))

    def script_out(self):
        return str((self.title, self.filename))
    
    def script_in(self, script):
        t = eval(script)
        self.title = t[0]
        self.filename = t[1]
        return self

class Snap:
    def __init__(self, title = "", filename = ""):
        self.title = title
        self.filename = filename

    def play(self):
        try:
            snapshot.snapWindow(self.title, self.filename)
        except IOError:
            import traceback
            traceback.print_exc()

    def script_out(self):
        return str((self.title, self.filename))

    def script_in(self, script):
        t = eval(script)
        self.title = t[0]
        self.filename = t[1]
        return self

class WinState:
    """
    Change the window state
    
    state:
    
    max -> maximize the window
    min -> minimize the window
    norm -> recover the window
    """
    def __init__(self, title = "", state = ""):
        self.title = title
        self.state = state

    def play(self):
        h = winutil.getWindowHandle(self.title)
        if self.state == 'max':
            winutil.maximizeWindow(h)
        if self.state == 'norm':
            winutil.normalizeWindow(h)
        if self.state == 'min':
            winutil.minimizeWindow(h)

    def script_out(self):
        return str((self.title, self.state))

    def script_in(self, script):
        t = eval(script)
        self.title = t[0]
        self.state = t[1]
        return self

class Resolution:
    def __init__(self, resolution = None):
        self.resolution = resolution

    def play(self):
        res = screenresolution.getRes()
        if res != self.resolution:
            screenresolution.convert(self.resolution)
            time.sleep(5)

    def script_out(self):
        return str(self.resolution)
    
    def script_in(self, script):
        self.resolution = eval(script)
        return self

class Orient:
    def __init__(self, flag = "tl"):
        self.flag = flag

    def play(self):
        winutil.setOrientation(self.flag)
    
    def script_out(self):
        return self.flag

    def script_in(self, script):
        self.flag = script
        return self


import win32con, win32api
class Key: # We'll expand a keyboard module if this grows larger
    """
    Press or release a key. 1 for down, 0 for up.
    """
    keymask = dict()
    keymask["shift"] = win32con.VK_SHIFT
    
    def __init__(self, key = "", action = 1):
        Key.keymask[key] # raise KeyError if key is not supported
        self.key = key
        self.action = action

    def play(self):
        win32api.keybd_event(Key.keymask[self.key], 0, \
                             0 if self.action \
                             else win32con.KEYEVENTF_KEYUP, 0)

    def script_out(self):
        return str((self.key, self.action))

    def script_in(self, script):
        t = eval(script)
        self.key = t[0]
        self.action = t[1]
        return self
