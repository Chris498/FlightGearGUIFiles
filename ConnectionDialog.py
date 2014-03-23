import wx

class ConnectionDialog(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE,
            ):

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)

        # Now continue with the normal construction of the dialog
        # contents
        sizer = wx.BoxSizer(wx.VERTICAL)
		
		
        self.boldFont = wx.Font(14,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_ITALIC,wx.FONTWEIGHT_BOLD)

        label = wx.StaticText(self, -1, "Edit the interval messages are sent from FlightGear")
        #label.SetFont(self.boldFont)
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
		
        #radioButton = wx.RadioButton(self,-1,"button1")
        #box.Add(radioButton)
        #self.Bind(wx.EVT_RADIOBUTTON,self.RadioSelect,radioButton)

        label = wx.StaticText(self, -1, "Enter Connection Speed in Seconds:")
        #label.SetHelpText("This is the help text for the label")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.text = wx.TextCtrl(self, -1, "3.0", size=(80,-1))
       # text.SetHelpText("Here's some help text for field #1")
        box.Add(self.text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        #sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

       # box = wx.BoxSizer(wx.HORIZONTAL)

       # label = wx.StaticText(self, -1, "Field #2:")
        #label.SetHelpText("This is the help text for the label")
        #box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        #text = wx.TextCtrl(self, -1, "", size=(80,-1))
        #text.SetHelpText("Here's some help text for field #2")
       # box.Add(text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

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
		
    #def RadioSelect(self,e):
    #    print("selected a radioButton")