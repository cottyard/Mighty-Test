from win32gui import *
import win32gui, win32api, win32con
import time, os, platform
import winutil
import snapshot
import screenresolution

from coreexceptions import WindowNotFound

from operations import Annotation, \
                       CheckPoint, Snap, \
                       Click, RightClick, DoubleClick, \
                       Hold, Drag, \
                       Interval, Wait, \
                       WinState, Resolution, \
                       Orient, \
                       Key, TypeString

operation_classes = dict()
operation_classes['Annotation'] = Annotation
operation_classes['Click'] = Click
operation_classes['RightClick'] = RightClick
operation_classes['DoubleClick'] = DoubleClick
operation_classes['Hold'] = Hold
operation_classes['Drag'] = Drag
operation_classes['Interval'] = Interval
operation_classes['Wait'] = Wait
operation_classes['CheckPoint'] = CheckPoint
operation_classes['Snap'] = Snap
operation_classes['Resolution'] = Resolution
operation_classes['Orient'] = Orient
operation_classes['WinState'] = WinState
operation_classes['Key'] = Key
operation_classes['TypeString'] = TypeString

class Recorder:
            
    if platform.release() == 'XP':
        SNAPSHOT_DIR = 'snapshots/xp/'
    elif platform.release() == '7':
        SNAPSHOT_DIR = 'snapshots/'
    else:
        raise Exception('Not supported OS')
    
    LIST_DIR = 'lists/'
    
    KEY_DOWN = 1
    KEY_UP = 0
    DOUBLE_CLICK_INTERVAL = 0.5
    HOLD_INTERVAL = 1

    opList = []
    editPos = 0
    resolution = (0, 0)

    lastClickTime = 0
    
    leftDownTime = 0
    leftDownTitle = ""
    leftDownPos = (0, 0)

    def __init__(self):
        if not os.path.exists(os.path.realpath(self.SNAPSHOT_DIR)):
            os.mkdir(os.path.realpath(self.SNAPSHOT_DIR))
        if not os.path.exists(os.path.realpath(self.LIST_DIR)):
            os.mkdir(os.path.realpath(self.LIST_DIR))



    # interfaces
    """
        Need to refactor these mouse motion processing code sometime
    """
    def OnMouseLeft(self, pos, press, windowname = ''):
        title, wPos = self.getTitleAndPos(pos, windowname)

        if press:
            self.leftDownTime = time.time()
            self.leftDownTitle = title
            self.leftDownPos = wPos
        else:
            if wPos == self.leftDownPos:
                interval = time.time() - self.leftDownTime
                if interval < self.HOLD_INTERVAL:
                    self.recordClick(title, wPos, 1)
                else: # not released immediately: Hold
                    self.recordHold(title, wPos, round(interval, 2))
            else: # released at a different place: Drag
                self.recordDrag(self.leftDownTitle, self.leftDownPos,
                                title, wPos)

    def OnMouseRight(self, pos, press, windowname = ''):
        title, wPos = self.getTitleAndPos(pos, windowname)
        if windowname:
            title = windowname
        if press:
            self.recordClick(title, wPos, 2)

    def recordInterval(self, itv):
        self.record(Interval(itv))

    def recordWait(self, title, waittime):
        self.record(Wait(title, waittime))
    
    def recordCheckpoint(self, windowTitle, filename):
        self.record(CheckPoint(windowTitle, filename))

    def recordSnap(self, windowTitle, filename):
        self.record(Snap(windowTitle, filename))

    def recordWinState(self, title, state):
        self.record(WinState(title, state))

    def recordKey(self, key, action):
        self.record(Key(key, action))

    def recordTypeString(self, string):
        self.record(TypeString(string))

    def recordResolution(self, resolution):
        self.record(Resolution(resolution))

    def recordOrient(self, flag):
        winutil.setOrientation(flag)
        self.record(Orient(flag))

    def play(self, interval = 0.5):
        self.beforePlay()
        try:
            for i in range(len(self.opList)):
                op = self.opList[i]
                e = op.play()
                if e:
                    print e
                    if e.startswith("error:"):
                        break
                time.sleep(interval)
                
        except WindowNotFound as e:
            print "error: cannot find window", e
            
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

    def setEdit(self, pos):
        if pos == -1:
            self.editPos = len(self.opList)
        elif pos >= 0 and pos <= len(self.opList):
            self.editPos = pos
        else:
            print "position out of index"

    def annotate(self, content):
        self.record(Annotation(content))


    # private methods
    def getTitleAndPos(self, pos, windowname = ""):
        """return the title of the top-level window;
        if windowname is given, return the given window title
        when the name is found in the window inheritance chain"""
        
        wnd = WindowFromPoint(pos)
        while True:
            if not GetParent(wnd): break
            if windowname:
                if windowname in GetWindowText(wnd):
                    break
            wnd = GetParent(wnd)
            
        title = GetWindowText(wnd)
        wPos = winutil.ScreenToWindow(wnd, pos)
        return (title, wPos)
    
    def validTitle(self, title):
        # do not record click on Python Shell, cmd line or taskbar windows
        if not title: return False
        if "Python Shell" in title: return False
        if "Operation Genius" in title: return False
        return True
        
    def recordClick(self, title, pos, button):
        if not self.validTitle(title): return
        if button == 1:
            click = Click(title, pos)
            # See if the operation can be converted to DoubleClick
            if len(self.opList) > 0:
                lastOp = None
                if self.editPos > 0:
                    lastOp = self.opList[self.editPos - 1]
                if lastOp.__class__.__name__ == 'Click':
                    if lastOp.equals(click) and \
                       time.time() - self.lastClickTime < \
                       self.DOUBLE_CLICK_INTERVAL:
                        del self.opList[self.editPos - 1]
                        self.editPos -= 1
                        self.record(DoubleClick(title, pos))
                        return

            self.lastClickTime = time.time()
            self.record(click)
            
        elif button == 2:
            self.record(RightClick(title, pos))

    def recordHold(self, title, pos, duration):
        if not self.validTitle(title): return
        self.record(Hold(title, pos, duration))

    def recordDrag(self, title_1, pos_1, title_2, pos_2):
        if not self.validTitle(title_1): return
        if not self.validTitle(title_2): return
        self.record(Drag(title_1, pos_1, title_2, pos_2))
    
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

    def beforePlay(self):
        winutil.setOrientation('tl')
        self.resolution = screenresolution.getRes()
        
    def afterPlay(self):
        if screenresolution.getRes() != self.resolution:
            screenresolution.convert(self.resolution)

    @classmethod
    def imageFileToPath(self, name):
        return self.SNAPSHOT_DIR + name + '.png'

    @classmethod
    def listFileToPath(self, name):
        return self.LIST_DIR + name + '.op'
