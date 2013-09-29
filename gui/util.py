import wx, os

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
        wx.Frame.__init__(self, parent, -1, title, \
                          style = wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)
        panel = wx.Panel(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.result = wx.TextCtrl(panel, -1, "",
                                  style = wx.TE_MULTILINE | wx.TE_READONLY)
        sizer.Add(self.result, flag = wx.EXPAND, proportion = 1)
        panel.SetSizer(sizer)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
    def OnClose(self, event):
        self.Hide()

    def write(self, msg):
        self.result.AppendText(msg)
        self.Show()

# the image display frame
class ImageFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, \
                          style = (wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)
                          ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
        self.SetMinSize((500,-1))
        self.panel = wx.Panel(self)
        self.img = wx.StaticBitmap(self.panel)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
    def load(self, path):
        if not os.path.exists(path):
            return
        img = wx.Image(path, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.img.SetBitmap(img)
        self.Refresh()
        self.panel.Fit()
        self.Fit()
        self.Show()

    def OnClose(self, event):
        self.Hide()
