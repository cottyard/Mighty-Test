import wx
from util import pack
import delegate
from delegate import gui_updator

class MousePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        self.button_startstop = wx.Button(self, label = "Start")
        self.running = False
        
        self.orientationList = ['Top Left', 'Top Right', 'Bottom Left', 'Bottom Right']
        self.orientationFlag = ['tl','tr','bl','br']
        self.choice_orient = wx.Choice(self, choices = self.orientationList)
        self.choice_orient.SetSelection(0)
        self.textctrl_windowname = wx.TextCtrl(self)

        self.Bind(wx.EVT_BUTTON, self.OnStartStop, self.button_startstop)
        self.Bind(wx.EVT_CHOICE, self.OnChoice, self.choice_orient)

        self.SetSizer(pack(wx.VERTICAL,
                           pack(wx.HORIZONTAL,
                                self.button_startstop,
                                self.choice_orient),
                           pack(wx.HORIZONTAL,
                                wx.StaticText(self, label = "window name: "),
                                self.textctrl_windowname)
                          )
                      )

    def OnStartStop(self, event):
        if self.running:
            self.button_startstop.SetLabel("Start")
            self.running = False
            delegate.listener.stop()
        else:
            self.button_startstop.SetLabel("Stop")
            self.running = True
            delegate.listener.start()

    @gui_updator
    def OnChoice(self, event):
        s = self.choice_orient.GetSelection()
        delegate.recorder.recordOrient(self.orientationFlag[s])

    def OnMouseEvent(self, *args):
        wx.CallAfter(self.mouseClick, *args)

    @gui_updator
    def mouseClick(self, x, y, button, press):
        windowname = self.textctrl_windowname.GetValue()
        if button == 1:
            delegate.recorder.OnMouseLeft((x,y), press, windowname)
        elif button == 2:
            delegate.recorder.OnMouseRight((x,y), press, windowname)
