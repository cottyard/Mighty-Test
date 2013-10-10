import wx
from util import pack
import delegate
from delegate import gui_updator

class KeyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        self.button_down = wx.Button(self, label = "Down")
        self.button_up = wx.Button(self, label = "Up")
        self.button_type = wx.Button(self, label = "Type")
        
        self.keyList = ['Shift', 'Ctrl', 'Enter', 'Alt', 'BackSpace']
        self.choice_key = wx.Choice(self, choices = self.keyList)
        self.choice_key.SetSelection(0)

        self.textctrl_string = wx.TextCtrl(self)

        self.Bind(wx.EVT_BUTTON, self.OnDown, self.button_down)
        self.Bind(wx.EVT_BUTTON, self.OnUp, self.button_up)
        self.Bind(wx.EVT_BUTTON, self.OnType, self.button_type)

        self.SetSizer(pack(wx.VERTICAL,
                           pack(wx.HORIZONTAL,
                                self.button_down,
                                self.button_up,
                                self.choice_key),
                           pack(wx.HORIZONTAL,
                                self.button_type,
                                self.textctrl_string)
                           )
                      )

    @gui_updator
    def OnDown(self, event):
        key = self.choice_key.GetStringSelection().lower()
        delegate.recorder.recordKey(key, delegate.recorder.KEY_DOWN)

    @gui_updator
    def OnUp(self, event):
        key = self.choice_key.GetStringSelection().lower()
        delegate.recorder.recordKey(key, delegate.recorder.KEY_UP)

    @gui_updator
    def OnType(self, event):
        delegate.recorder.recordTypeString(
            self.textctrl_string.GetValue())
