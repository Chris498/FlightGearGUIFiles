import wx

class MainWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.panel = wx.Panel(self)
        self.buttons = [wx.Button(self.panel, label=str(n)) for n in range(9)]

        self.sizer = wx.GridBagSizer()
        for i, button in enumerate(self.buttons):
            self.sizer.Add(button, (i / 3, i % 3), flag=wx.ALL | wx.EXPAND)
        self.sizer.AddGrowableCol(1)
        self.sizer.AddGrowableRow(1)

        self.border = wx.BoxSizer()
        self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 20)

        self.panel.SetSizerAndFit(self.border)  
        self.Show()

app = wx.App(False)
win = MainWindow(None)
app.MainLoop()