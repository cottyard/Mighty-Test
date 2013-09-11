import wx
from util import pack
import delegate
from delegate import gui_updator

class WindowPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.button_max = wx.Button(self, label = "Maximize")
        self.button_nor = wx.Button(self, label = "Normalize")
        self.button_min = wx.Button(self, label = "Minimize")

        self.input_windowname = wx.TextCtrl(self)

        self.Bind(wx.EVT_BUTTON, self.Callback('max'), self.button_max)
        self.Bind(wx.EVT_BUTTON, self.Callback('norm'), self.button_nor)
        self.Bind(wx.EVT_BUTTON, self.Callback('min'), self.button_min)

        self.SetSizer(pack(wx.VERTICAL,
                           pack(wx.HORIZONTAL,
                                self.button_max,
                                self.button_nor,
                                self.button_min),
                           pack(wx.HORIZONTAL,
                                wx.StaticText(self, label = "window name: "),
                                self.input_windowname)
                           )
                      )

    def Callback(self, arg):
        @gui_updator
        def c(e):
            title = self.input_windowname.GetValue().encode('UTF-8')
            if title:
                delegate.recorder.recordWinState(title, arg)
        return c
