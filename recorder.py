from win32gui import *
import win32gui, win32api, win32con
import time, os
import winutil
import snapshot

from operations import CheckPoint, Click, Interval

operation_classes = dict()
operation_classes['Click'] = Click
operation_classes['Interval'] = Interval
operation_classes['CheckPoint'] = CheckPoint

class Recorder:
    opList = []
    checkpoint_number = 0
    recording_state = False
    editPos = 0

    # callbacks
    
    def OnLeftDown(self, pos):
        """callback function"""
        if self.recording_state:
            self.recordClick(pos)

    # interfaces

    def recordInterval(self, itv):
        self.record(Interval(itv))

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

        self.record(Click(title, wPos))

    def recordCheckpoint(self, windowTitle):
        self.checkpoint_number += 1
        if not os.path.exists(os.path.realpath('snapshots')):
            os.mkdir(os.path.realpath('snapshots'))
        filename = 'snapshots/' + windowTitle + '_' + \
                   str(self.checkpoint_number) + '.png'
        snapshot.snapWindow(windowTitle, filename)
        
        self.record(CheckPoint(windowTitle, filename))

    def erase(self):
        if self.editPos > 0:
            self.editPos -= 1
            if self.opList[self.editPos].__class__.__name__ == 'CheckPoint':
                self.checkpoint_number -= 1
            del self.opList[self.editPos]

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
        for i, op in enumerate(self.opList):
            if i == self.editPos:
                print "--- editting here ---"
            print op.script_out()
        
        print

    def setEdit(self, pos):
        if pos == -1:
            self.editPos = len(self.opList)
        elif pos >= 0 and pos <= len(self.opList):
            self.editPos = pos
        else:
            print "position out of index"


    def clear(self):
        self.opList = []
        self.editPos = 0
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
            self.editPos = len(self.opList)

    # private methods
    def record(self, op):
        self.opList.insert(self.editPos, op)
        self.editPos += 1
