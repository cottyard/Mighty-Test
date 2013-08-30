from win32gui import *
import win32gui, win32api, win32con
import time, os
import winutil
import snapshot

"""

These classes are the operations.
I don't want them to inherit from an Operation class
because I just read about the idea "Duck Typing"

"""
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

operation_classes = dict()
operation_classes['Click'] = Click
operation_classes['Interval'] = Interval
operation_classes['CheckPoint'] = CheckPoint

class Recorder:
    opList = []
    checkpoint_number = 0
    recording_state = False
    

    # callbacks
    
    def OnLeftDown(self, pos):
        """callback function"""
        if self.recording_state:
            self.recordClick(pos)

    # interfaces

    def recordInterval(self, itv):
        self.opList.append(Interval(itv))

    def recordClick(self, pos):
        wnd = WindowFromPoint(pos)
        while GetParent(wnd):
            wnd = GetParent(wnd)
        title = GetWindowText(wnd)
        # do not record click on Python Shell, cmd line or taskbar windows
        if not title: return
        if "Python Shell" in title: return
        if "Operation Genius" in title: return
        wPos = winutil.ScreenToWindow(wnd, pos)
        self.opList.append(Click(title, wPos))

    def recordCheckpoint(self, windowTitle):
        self.checkpoint_number += 1
        if not os.path.exists(os.path.realpath('snapshots')):
            os.mkdir(os.path.realpath('snapshots'))
        filename = 'snapshots/' + windowTitle + '_' + \
                   str(self.checkpoint_number) + '.png'
        snapshot.snapWindow(windowTitle, filename)
        self.opList.append(CheckPoint(windowTitle, filename))

    def erase(self):
        if len(self.opList) > 0:
            if self.opList[-1].__class__.__name__ == 'CheckPoint':
                self.checkpoint_number -= 1
            del self.opList[-1]

    def play(self):
        for op in self.opList:
            e = op.play()
            if e:
                print "play error: " + e
                break
            time.sleep(0.1)

    def printOpList(self):
        if not self.opList:
            print "empty"
            return
        for op in self.opList:
            print op.script_out()

    def clear(self):
        self.opList = []
        self.checkpoint_number = 0

    def start(self):
        self.recording_state = True

    def stop(self):
        self.recording_state = False

    def save(self, fname):
        with open(fname + ".op", 'wb') as f:
            for op in self.opList:
                f.write(op.__class__.__name__ + '\n')
                f.write(op.script_out() + '\n')

    def load(self, fname):
        self.clear()
        with open(fname + ".op", 'rb') as f:
            while True:
                n = f.readline().strip()
                s = f.readline().strip()
                if not n or not s: break
                op = operation_classes[n]()
                self.opList.append(op.script_in(s))
                if n == 'CheckPoint':
                    self.checkpoint_number += 1



