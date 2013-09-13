import wx, os, threading
from util import pack, ResultFrame
import delegate
from delegate import gui_updator, daemon

class ListPanel(wx.Panel):

    BUTTON_SIZE = (55, -1)
    wildcard = "Operation files (*.op)|*.op|All files (*.*)|*.*"
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        class ShrinkableListBox(wx.ListBox):
            def __init__(self, parent, style):
                wx.ListBox.__init__(self, parent, style = style)
                self.Bind(wx.EVT_SIZE, self.OnSize)
            def OnSize(self, event):
                self.SetMinSize(wx.Size(1, 1))
                event.Skip()
                
        self.list = ShrinkableListBox(self, style = wx.LB_EXTENDED |
                                                    wx.LB_HSCROLL)

        self.button_play = wx.Button(self, label = "Play", size = self.BUTTON_SIZE)
        self.button_delete = wx.Button(self, label = "Delete", size = self.BUTTON_SIZE)
        self.button_clear = wx.Button(self, label = "Clear", size = self.BUTTON_SIZE)
        self.button_save = wx.Button(self, label = "Save", size = self.BUTTON_SIZE)
        self.button_load = wx.Button(self, label = "Load", size = self.BUTTON_SIZE)
        self.textctrl_edit = wx.TextCtrl(self, size = (30, -1))
        self.textctrl_edit.SetMaxLength(3)

        self.Bind(wx.EVT_BUTTON, self.OnClear, self.button_clear)
        self.Bind(wx.EVT_BUTTON, self.OnLoad, self.button_load)
        self.Bind(wx.EVT_BUTTON, self.OnPlay, self.button_play)
        self.Bind(wx.EVT_BUTTON, self.OnDelete, self.button_delete)
        self.Bind(wx.EVT_BUTTON, self.OnSave, self.button_save)
        self.Bind(wx.EVT_TEXT, self.OnEdit, self.textctrl_edit)
        
        self.Bind(wx.EVT_LISTBOX, self.OnSelect, self.list)

        self.SetSizer(pack(wx.VERTICAL,
                           self.list,
                           pack(wx.HORIZONTAL,
                                wx.StaticText(self, label = "Edit"),
                                self.textctrl_edit,
                                self.button_play,
                                self.button_delete,
                                self.button_clear,
                                self.button_save,
                                self.button_load)
                           )
                      )

        self.resultFrame = ResultFrame(self, "playing output")

    def updateList(self, l, edit):
        self.list.Set(l)
        if edit < len(l):
            self.list.SetSelection(edit)
        else:
            try:
                self.list.SetFirstItem(self.list.GetCount() - 1)
            except:
                pass
            
    # callbacks
    def OnEdit(self, event):
        try:
            for i in self.list.GetSelections():
                self.list.Deselect(i)
            
            p = int(self.textctrl_edit.GetValue())
            if p < 0 or p >= self.list.GetCount():
                raise ValueError
            
            delegate.recorder.setEdit(p)
            self.list.SetSelection(p)
        except:
            delegate.recorder.setEdit(-1)
            for i in self.list.GetSelections():
                self.list.Deselect(i)

    @daemon
    def OnPlay(self, event):
        self.resultFrame.Show()
        delegate.gui.toggleOnTop()
        try:
            print "---------- START ----------\n"
            delegate.recorder.play()
            print "\n---------- DONE ----------\n\n"
        finally:
            delegate.gui.toggleOnTop()

    @gui_updator
    def OnClear(self, event):
        self.textctrl_edit.SetValue('')
        delegate.recorder.clear()

    @gui_updator
    def OnDelete(self, event):
        s = list(self.list.GetSelections())
        s.reverse()
        for i in s:
            delegate.recorder.setEdit(i + 1)
            delegate.recorder.erase()
        delegate.recorder.setEdit(-1)

    def OnSelect(self, event):
        try:
            s = self.list.GetSelections()
            if len(s) == 1:
                self.textctrl_edit.SetValue(str(s[0]))
        except IndexError:
            pass

    def OnSave(self, event):
        dlg = wx.FileDialog(self, "Save operation list...",
                            os.getcwd(),
                            style = wx.SAVE | wx.OVERWRITE_PROMPT,
                            wildcard = self.wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            p = dlg.GetPath()
            if not os.path.splitext(p)[1]:
                p = p + '.op'
            delegate.recorder.saveToAbsPath(p)
        dlg.Destroy()

    @gui_updator
    def OnLoad(self, event):
        dlg = wx.FileDialog(self, "Open operation list...",
                            os.getcwd(), style=wx.OPEN, 
                            wildcard = self.wildcard) 
        if dlg.ShowModal() == wx.ID_OK: 
            p = dlg.GetPath() 
            delegate.recorder.loadFromAbsPath(p)
        dlg.Destroy()

        
