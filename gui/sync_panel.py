import wx
from util import pack
import delegate
from delegate import gui_updator

class SyncPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.button_wait = wx.Button(self, label = "Wait")
        self.button_int = wx.Button(self, label = "Interval")

        self.input_windowname = wx.TextCtrl(self)
        self.input_time = wx.TextCtrl(self, size = (10, -1))

        self.Bind(wx.EVT_BUTTON, self.OnInt, self.button_int)
        self.Bind(wx.EVT_BUTTON, self.OnWait, self.button_wait)

        self.SetSizer(pack(wx.VERTICAL,
                           pack(wx.HORIZONTAL,
                                self.button_wait,
                                self.button_int,
                                wx.StaticText(self, label = "time: "),
                                self.input_time),
                           pack(wx.HORIZONTAL,
                                wx.StaticText(self, label = "window name: "),
                                self.input_windowname)
                           )
                      )
        
    @gui_updator
    def OnInt(self, event):
        try:
            itv = float(self.input_time.GetValue())
            delegate.recorder.recordInterval(itv)
        except:
            pass

    @gui_updator
    def OnWait(self, event):
        try:
            waitingtime = float(self.input_time.GetValue())
        except:
            pass
        else:
            windowname = self.input_windowname.GetValue()
            if windowname:
                delegate.recorder.recordWait(windowname, waitingtime)
