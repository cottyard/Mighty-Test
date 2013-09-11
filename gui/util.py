import wx
def pack(style, *windows):
    s = wx.BoxSizer(style)
    for w in windows:
        if isinstance(w, (wx.Button, wx.Choice)):
            s.Add(w)
        elif isinstance(w, (wx.TextCtrl, wx.ListBox)):
            s.Add(w, flag = wx.EXPAND, proportion = 1)
        else:
            s.Add(w, flag = wx.EXPAND)
        
    return s

# the play result frame
class ResultFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title)
        panel = wx.Panel(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.result = wx.TextCtrl(panel, -1, "",
                                  style = wx.TE_MULTILINE | wx.TE_READONLY)
        sizer.Add(self.result, flag = wx.EXPAND, proportion = 1)
        panel.SetSizer(sizer)
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        
    def OnExit(self, event):
        self.Hide()

    def write(self, msg):
        self.result.AppendText(msg)
