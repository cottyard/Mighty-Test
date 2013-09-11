import wx
from util import pack
import delegate
from delegate import gui_updator

class CheckPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.button_checkpoint = wx.Button(self, label = "Checkpoint")
        self.button_snap = wx.Button(self, label = "Snap")
        
        self.input_windowname = wx.TextCtrl(self)
        self.input_filename = wx.TextCtrl(self)

        self.Bind(wx.EVT_BUTTON, self.OnCheckpoint, self.button_checkpoint)
        self.Bind(wx.EVT_BUTTON, self.OnSnap, self.button_snap)

        self.SetSizer(pack(wx.VERTICAL,
                           pack(wx.HORIZONTAL,
                                self.button_checkpoint,
                                self.button_snap),
                           pack(wx.HORIZONTAL,
                                wx.StaticText(self, label = "window name: "),
                                self.input_windowname),
                           pack(wx.HORIZONTAL,
                                wx.StaticText(self, label = "image name: "),
                                self.input_filename),
                           )
                      )
    @gui_updator
    def OnCheckpoint(self, event):
        s1 = self.input_windowname.GetValue()
        s2 = self.input_filename.GetValue()
        if s1 and s2:
            delegate.recorder.recordCheckpoint(s1, s2)
    @gui_updator
    def OnSnap(self, event):
        s1 = self.input_windowname.GetValue()
        s2 = self.input_filename.GetValue()
        if s1 and s2:
            delegate.recorder.recordSnap(s1, s2)
