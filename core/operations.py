import os, time
import winutil
import snapshot
import screenresolution

from coreexceptions import WindowNotFound

class Annotation:
    def __init__(self, content = ""):
        self.content = content
        
    def play(self):
        # do nothing.. I'm just a tiny
        # piece of annotation
        pass
    
    def script_out(self):
        return self.content
    
    def script_in(self, script):
        self.content = script
        return self

class Click:
    
    def __init__(self, title = "", pos = (0, 0)):
        self.title = title
        self.pos = pos
        
    def play(self):
        winutil.clickInsideWindow(self.title, self.pos)

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
        winutil.clickInsideWindow(self.title, self.pos, times = 2)

class RightClick(Click):
    def play(self):
        winutil.clickInsideWindow(self.title, self.pos, button = 2)

class Drag:
    def __init__(self, title_1 = "", pos_1 = (0, 0),
                       title_2 = "", pos_2 = (0, 0)):
        self.title_1 = title_1
        self.title_2 = title_2
        self.pos_1 = pos_1
        self.pos_2 = pos_2

    def play(self):
        winutil.mouseDownInsideWindow(self.title_1, self.pos_1)
        winutil.mouseUpInsideWindow(self.title_2, self.pos_2)

    def script_out(self):
        return str((self.title_1, self.pos_1,
                    self.title_2, self.pos_2))

    def script_in(self, script):
        t = eval(script)
        self.title_1 = t[0]
        self.pos_1 = t[1]
        self.title_2 = t[2]
        self.pos_2 = t[3]
        return self

class Hold:
    def __init__(self, title = "", pos = (0, 0), duration = 0):
        self.title = title
        self.pos = pos
        self.duration = duration

    def play(self):
        winutil.mouseDownInsideWindow(self.title, self.pos)
        time.sleep(self.duration)
        winutil.mouseUpInsideWindow(self.title, self.pos)

    def script_out(self):
        return str((self.title, self.pos, self.duration))

    def script_in(self, script):
        t = eval(script)
        self.title = t[0]
        self.pos = t[1]
        self.duration = t[2]
        return self

import datetime
import vision

class SmartClick:
    def __init__(self, pos = (0, 0)):
        filename = datetime.datetime.fromtimestamp(time.time())\
                   .strftime('%Y-%m-%d %H.%M.%S')
        from recorder import Recorder
        self.path = Recorder.traceFileToPath(filename)
        widget_pos = snapshot.snapWidgetFromPoint(pos, self.path)
        # SmartClick does not support Orient
        self.pos = (pos[0] - widget_pos[0], pos[1] - widget_pos[1])
        
    def play(self):
        if not os.path.exists(os.path.realpath(self.path)):
            return 'error: template image ' + self.path + ' does not exist.'
        widget_pos = vision.findInScreen(self.path)
        if widget_pos is None:
            return 'message: did not find ' + self.path + ' on screen.'
        sPos = (widget_pos[0] + self.pos[0], widget_pos[1] + self.pos[1])
        winutil.clickOnScreen(sPos)

    def script_out(self):
        return str((self.path, self.pos))

    def script_in(self, script):
        t = eval(script)
        self.path = t[0]
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

class Wait:
    def __init__(self, window_title = "", waiting_time = 0):
        self.window_title = window_title
        self.waiting_time = waiting_time

    def play(self):
        found = False
        start_time = time.time()
        while time.time() - start_time < self.waiting_time:
            time.sleep(1)
            try:
                winutil.getWindowHandle(self.window_title)
            except WindowNotFound:
                pass
            else:
                found = True
                break

        if not found:
            return "error: window " + self.window_title + \
                   " didn't show up in " + str(self.waiting_time) + \
                   " seconds"

    def script_out(self):
        return str((self.window_title, self.waiting_time))

    def script_in(self, script):
        t = eval(script)
        self.window_title = t[0]
        self.waiting_time = t[1]
        return self

class CheckPoint:
    def __init__(self, title = "", filename = ""):
        self.title = title
        self.filenames = (filename, )

    def play(self):
        from recorder import Recorder
        if len(self.filenames) == 1:
            img = Recorder.imageFileToPath(self.filenames[0])
            if not os.path.exists(img):
                snapshot.snapWindow(self.title, img)
                return "message: " + "check point image file " + img + \
                       " doesn't exist and has been created"

            tempfile = 'snapshots/checkpoint.png'
            snapshot.snapWindow(self.title, tempfile)

            if not snapshot.compareSnapshots(img, tempfile):
                return "error: " + "checkpoint fails: " + tempfile + \
                       " is inconsistent with " + img

            # delete temp file
            os.remove(os.path.realpath(tempfile))
            
        else: # this is a temporary behavior modification
            match = False
            tempfile = 'snapshots/checkpoint.png'
            snapshot.snapWindow(self.title, tempfile)
            
            for i in self.filenames:
                img = Recorder.imageFileToPath(i)
                if not os.path.exists(img):
                    return "message: check point image file " + img + \
                           " doesn't exist"

                if snapshot.compareSnapshots(img, tempfile):
                   match = True
                   break
                
            if not match:
                return "error: checkpoint fails: " + tempfile + \
                       " matches none of the image files"

    def script_out(self):
        return str((self.title,) + self.filenames)

    def script_in(self, script):
        t = eval(script)
        self.title = t[0]
        self.filenames = t[1:]
        return self

class Snap:
    def __init__(self, title = "", filename = ""):
        self.title = title
        self.filename = filename

    def play(self):
        from recorder import Recorder
        img = Recorder.imageFileToPath(self.filename)
        snapshot.snapWindow(self.title, img)

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


import keyutil

class Key: # We'll expand a keyboard module if this grows larger
    """
    Press or release a key. 1 for down, 0 for up.
    """
    def __init__(self, key = "", action = 1):
        self.key = key
        self.action = action

    def play(self):
        keyutil.toggle_key(self.key, self.action)
        
    def script_out(self):
        return str((self.key, self.action))

    def script_in(self, script):
        t = eval(script)
        self.key = t[0]
        self.action = t[1]
        return self

class TypeString:
    def __init__(self, string = ""):
        self.string = string

    def play(self):      
        for c in self.string:
            keyutil.tap_key(c)

    def script_out(self):
        return self.string
    
    def script_in(self, script):
        self.string = script
        return self
