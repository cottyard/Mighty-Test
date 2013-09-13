import wx, sys
from mouse_panel import MousePanel
from window_panel import WindowPanel
from check_panel import CheckPanel
from key_panel import KeyPanel
from sync_panel import SyncPanel
from list_panel import ListPanel
from environ_panel import EnvironPanel
import delegate
       
class MainFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, "Operation Genius",
                          #style = wx.DEFAULT_FRAME_STYLE)
                          style = wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)

        self.panel = wx.Panel(self)

        self.mouse_panel = MousePanel(self.panel)
        self.window_panel = WindowPanel(self.panel)
        self.check_panel = CheckPanel(self.panel)
        self.key_panel = KeyPanel(self.panel)
        self.sync_panel = SyncPanel(self.panel)
        self.list_panel = ListPanel(self.panel)
        self.environ_panel = EnvironPanel(self.panel)
        
        pm = self.makeFunctionPane(self.mouse_panel, "Mouse")
        pw = self.makeFunctionPane(self.window_panel, "Window")
        pc = self.makeFunctionPane(self.check_panel, "Check")
        pk = self.makeFunctionPane(self.key_panel, "Key")
        ps = self.makeFunctionPane(self.sync_panel, "Sync")
        pl = self.makeFunctionPane(self.list_panel, "List")
        pe = self.makeFunctionPane(self.environ_panel, "Environment")

        sizer = wx.GridBagSizer(hgap = 10, vgap = 10)

        sizer.Add(pm, pos = (0, 1), flag = wx.EXPAND)
        sizer.Add(pk, pos = (1, 1), flag = wx.EXPAND)
        sizer.Add(ps, pos = (2, 1), flag = wx.EXPAND)
        sizer.Add(pw, pos = (3, 1), flag = wx.EXPAND)
        sizer.Add(pc, pos = (4, 1), flag = wx.EXPAND)
        sizer.Add(pe, pos = (5, 1), flag = wx.EXPAND)

        sizer.Add(pl, pos = (0, 0), span = (6, 1), flag = wx.EXPAND)

        for i in range(5):
            sizer.AddGrowableRow(i)

        sizer.AddGrowableCol(0)

        self.panel.SetSizer(sizer)
        
        self.panel.Fit()
        self.Fit()
        self.SetMinSize(self.GetSize())
        
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        self.Show()

    def makeFunctionPane(self, panel, label):
        box = wx.StaticBox(self.panel, label = label)
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        bsizer.Add(panel, flag = wx.EXPAND, proportion = 1)
        return bsizer

    def updateGUI(self):
        lists = delegate.recorder.literateOpList()
        l = [name + ' '*(20-len(name)) + data
             for name, data in zip(lists[0], lists[1])]
        edit = delegate.recorder.editPos
        self.list_panel.updateList(l, edit)
    
    def OnExit(self, event):
        #delegate.listener.stop()
        event.Skip()

class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()

        self.mainframe = MainFrame(parent = None, id = -1)
        
        delegate.listener.register_click(
            self.mainframe.mouse_panel.OnMouseEvent)

        self.out = sys.stdout
        self.err = sys.stderr

        sys.stdout = self.mainframe.list_panel.resultFrame
        sys.stderr = self.mainframe.list_panel.resultFrame

        self.mainframe.Show()
        return True

    def OnExit(self):
        delegate.listener.stop()
        sys.stdout = self.out
        sys.stderr = self.err
        wx.Exit()
    
    def getMainWindow(self):
        return self.mainframe


app = None

class GuiMeta:
    
    def update(self):
        app.getMainWindow().updateGUI()
        
    def toggleOnTop(self):
        
        app.getMainWindow().list_panel \
           .resultFrame.ToggleWindowStyle(wx.STAY_ON_TOP)
        app.getMainWindow().list_panel \
           .resultFrame.Refresh()

        app.getMainWindow().ToggleWindowStyle(wx.STAY_ON_TOP)
        app.getMainWindow().Refresh()
        
def InitGUI():
    global app
    app = MyApp(0)

def StartGUI():
    try:
        app.MainLoop()
    finally:
        print "Exit"

if __name__ == '__main__':
    app = wx.PySimpleApp()
    MainFrame(None, -1).Show()
    app.MainLoop()
    print "Stop"
##    try:
##    
##    except:
##        import traceback
##        xc = traceback.format_exception(*sys.exc_info())
##        wx.MessageBox(''.join(xc))

