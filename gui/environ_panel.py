import wx
from util import pack
import delegate
from delegate import gui_updator

class EnvironPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.button_resolution = wx.Button(self, label = "Resolution")

        self.input_width = wx.TextCtrl(self, size = (20, -1))
        self.input_height = wx.TextCtrl(self, size = (20, -1))

        self.Bind(wx.EVT_BUTTON, self.OnResolution, self.button_resolution)

        self.SetSizer(pack(wx.HORIZONTAL,
                           self.button_resolution,
                           wx.StaticText(self, label = "width: "),
                           self.input_width,
                           wx.StaticText(self, label = "height: "),
                           self.input_height)
                      )
        
    @gui_updator
    def OnResolution(self, event):
        try:
            res = (int(self.input_width.GetValue()),
                   int(self.input_height.GetValue()))
            delegate.recorder.recordResolution(res)
        except:
            pass
