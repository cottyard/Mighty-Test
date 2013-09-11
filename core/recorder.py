from win32gui import *
import win32gui, win32api, win32con
import time, os
import winutil
import snapshot
import screenresolution

from operations import CheckPoint, Click, RightClick, DoubleClick, Interval, \
                       Wait, Snap, WinState, Resolution, Orient, Key

operation_classes = dict()
operation_classes['Click'] = Click
operation_classes['RightClick'] = RightClick
operation_classes['DoubleClick'] = DoubleClick
operation_classes['Interval'] = Interval
operation_classes['Wait'] = Wait
operation_classes['CheckPoint'] = CheckPoint
operation_classes['Snap'] = Snap
operation_classes['Resolution'] = Resolution
operation_classes['Orient'] = Orient
operation_classes['WinState'] = WinState
operation_classes['Key'] = Key


class Recorder:
    
    KEY_DOWN = 1
    KEY_UP = 0
    DOUBLE_CLICK_INTERVAL = 0.5

    opList = []
    editPos = 0
    resolution = (0, 0)

    lastClickTime = 0

    def __init__(self):
        if not os.path.exists(os.path.realpath('snapshots')):
            os.mkdir(os.path.realpath('snapshots'))
        if not os.path.exists(os.path.realpath('lists')):
            os.mkdir(os.path.realpath('lists'))

    # interfaces
    
    def OnLeftDown(self, pos):
        return self.recordClick(pos, 1)

    def OnRightDown(self, pos):
        return self.recordClick(pos, 2)

    def recordInterval(self, itv):
        self.record(Interval(itv))

    def recordWait(self, title, waittime):
        self.record(Wait(title, waittime))

    def createCheckpoint(self, windowTitle, filename):
        path = self.imageFileToPath(filename)
        snapshot.snapWindow(windowTitle, path)
        self.record(CheckPoint(windowTitle, path))
    
    def recordCheckpoint(self, windowTitle, filename):
        path = self.imageFileToPath(filename)
        self.record(CheckPoint(windowTitle, path))

    def recordSnap(self, windowTitle, filename):
        path = self.imageFileToPath(filename)
        self.record(Snap(windowTitle, path))

    def recordWinState(self, title, state):
        self.record(WinState(title, state))

    def recordKey(self, key, action):
        self.record(Key(key, action))

    def recordResolution(self, resolution):
        self.record(Resolution(resolution))

    def recordOrient(self, flag):
        winutil.setOrientation(flag)
        self.record(Orient(flag))

    def play(self, interval = 0.5):
        self.beforePlay()
        for i in range(len(self.opList)):
            op = self.opList[i]
            e = op.play()
            if e:
                print e
                if e.startswith("error:"):
                    break
            time.sleep(interval)
        self.afterPlay()
        
    def erase(self, n = 1):
        for i in range(n):
            if self.editPos > 0:
                self.editPos -= 1
                del self.opList[self.editPos]
            else:
                break

    def printOpList(self):
        if not self.opList:
            print "empty"
            print
            return
        for i, op in enumerate(self.opList):
            print i + 1, ": " + op.__class__.__name__
            print '\t' + op.script_out()
        
        print

    def literateOpList(self):
         return ([op.__class__.__name__ for op in self.opList],
                 [op.script_out() for op in self.opList])

    def clear(self):
        self.opList = []
        self.editPos = 0

    def save(self, fname):
        with open(self.listFileToPath(fname), 'wb') as f:
            self.saveFile(f)

    def load(self, fname):
        with open(self.listFileToPath(fname), 'rb') as f:
            self.loadFile(f)

    def loadFromAbsPath(self, fpath):
        with open(fpath, 'rb') as f:
            self.loadFile(f)
            
    def saveToAbsPath(self, fpath):
        with open(fpath, 'wb') as f:
            self.saveFile(f)

    # private methods
    def recordClick(self, pos, button):
        # get clicked window title
        wnd = WindowFromPoint(pos)
        while GetParent(wnd):
            wnd = GetParent(wnd)
        title = GetWindowText(wnd)

        # do not record click on Python Shell, cmd line or taskbar windows
        if not title: return False
        if "Python Shell" in title: return False
        if "Operation Genius" in title: return False
        wPos = winutil.ScreenToWindow(wnd, pos)

        if button == 1:
            click = Click(title, wPos)
            # See if the operation can be converted to DoubleClick
            if len(self.opList) > 0:
                if self.editPos > 0:
                    lastOp = self.opList[self.editPos - 1]
                if lastOp.__class__.__name__ == 'Click':
                    if lastOp.equals(click) and \
                       time.time() - self.lastClickTime < \
                       self.DOUBLE_CLICK_INTERVAL:
                        del self.opList[self.editPos - 1]
                        self.editPos -= 1
                        self.record(DoubleClick(title, wPos))
                        return True
        
            self.lastClickTime = time.time()
            self.record(click)
            return True
            
        elif button == 2:
            self.record(RightClick(title, wPos))
            return True

    
    def loadFile(self, f):
        self.clear()
        while True:
            n = f.readline().strip()
            s = f.readline().strip()
            if not n or not s: break
            op = operation_classes[n]()
            self.opList.append(op.script_in(s))
            
        self.editPos = len(self.opList)

    def saveFile(self, f):
        for op in self.opList:
            f.write(op.__class__.__name__ + '\n')
            f.write(op.script_out() + '\n')
    
    def record(self, op):
        self.opList.insert(self.editPos, op)
        self.editPos += 1

    def setEdit(self, pos):
        if pos == -1:
            self.editPos = len(self.opList)
        elif pos >= 0 and pos <= len(self.opList):
            self.editPos = pos
        else:
            print "position out of index"

    def imageFileToPath(self, name):
        return 'snapshots/' + name + '.png'

    def listFileToPath(self, name):
        return 'lists/' + name + '.op'

    def beforePlay(self):
        winutil.setOrientation('tl')
        self.resolution = screenresolution.getRes()
        
    def afterPlay(self):
        if screenresolution.getRes() != self.resolution:
            screenresolution.convert(self.resolution)
