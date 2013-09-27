import wx
from util import pack
import delegate
from delegate import gui_updator

class MousePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        self.toggle_startstop = wx.ToggleButton(self, label = "Not Recording")
        self.running = False
        
        self.orientationList = ['Top Left', 'Top Right', 'Bottom Left', 'Bottom Right']
        self.orientationFlag = ['tl','tr','bl','br']
        self.choice_orient = wx.Choice(self, choices = self.orientationList)
        self.choice_orient.SetSelection(0)
        self.toggle_smartclick = wx.CheckBox(self, label = "Smart Click")
        self.textctrl_windowname = wx.TextCtrl(self)

        sizer = wx.GridBagSizer(hgap = 1, vgap = 1)
        sizer.Add(self.toggle_smartclick, pos = (1, 1), flag = wx.EXPAND)
        sizer.Add(self.choice_orient,pos = (0, 1), flag = wx.EXPAND)
        sizer.Add(self.toggle_startstop, pos = (0, 0), span = (2, 1), flag = wx.EXPAND)

        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnStartStop, self.toggle_startstop)
        self.Bind(wx.EVT_CHOICE, self.OnChoice, self.choice_orient)

        self.SetSizer(pack(wx.VERTICAL,
                           sizer,
                           (10, 10),
                           pack(wx.HORIZONTAL,
                                wx.StaticText(self, label = "window name: "),
                                self.textctrl_windowname)
                          )
                      )

    def OnStartStop(self, event):
        if self.running:
            self.toggle_startstop.SetLabel("Not Recording")
            self.running = False
            delegate.listener.stop()
        else:
            self.toggle_startstop.SetLabel("Recording...")
            self.running = True
            delegate.listener.start()

    @gui_updator
    def OnChoice(self, event):
        s = self.choice_orient.GetSelection()
        delegate.recorder.recordOrient(self.orientationFlag[s])

    def OnMouseEvent(self, *args):
        if self.toggle_smartclick.IsChecked():
            wx.CallAfter(self.mouseClick_smart, *args)
        else:
            wx.CallAfter(self.mouseClick, *args)
        
    @gui_updator
    def mouseClick(self, x, y, button, press):
        windowname = self.textctrl_windowname.GetValue()
        if button == 1:
            delegate.recorder.OnMouseLeft((x,y), press, windowname)
        elif button == 2:
            delegate.recorder.OnMouseRight((x,y), press, windowname)

    @gui_updator
    def mouseClick_smart(self, x, y, button, press):
        if not press:
            delegate.recorder.recordSmartClick((x,y))
