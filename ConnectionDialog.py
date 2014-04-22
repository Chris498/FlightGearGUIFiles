import wx
#This Class handles the Connection Dialog that appears in FlightTracker when modifying the connection speed.

class ConnectionDialog(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE,
            ):


        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)

        self.PostCreate(pre)


        sizer = wx.BoxSizer(wx.VERTICAL)
		
		
        self.boldFont = wx.Font(14,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_ITALIC,wx.FONTWEIGHT_BOLD)

        label = wx.StaticText(self, -1, "Edit the interval messages are sent from FlightGear")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
		


        label = wx.StaticText(self, -1, "Enter Connection Speed in Seconds:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.text = wx.TextCtrl(self, -1, "3.0", size=(80,-1))
        box.Add(self.text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)


        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        

        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)
