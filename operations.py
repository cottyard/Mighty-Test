import os, time
import winutil
import snapshot
import screenresolution

"""

These classes are the operations.
I don't want them to inherit from an Operation class
because I just read about the idea "Duck Typing"

"""

        
class Click:
    def __init__(self, title = "", pos = (0, 0)):
        self.title = title
        self.pos = pos
        
    def play(self):
        wnd = winutil.getWindowHandle(self.title)
        if not wnd:
            print self.title + ' does not exist.'
            return
        pos = winutil.WindowToScreen(wnd, self.pos)
        winutil.clickOnWindow(wnd, pos)

    def script_out(self):
        return str((self.title, self.pos))
    
    def script_in(self, script):
        t = eval(script)
        self.title = t[0]
        self.pos = t[1]
        return self

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
            return "check point image file " + self.filename + \
                   " does not exist"
            
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
