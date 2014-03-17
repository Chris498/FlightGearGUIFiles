import wx
import wx.lib.scrolledpanel as scrolled

class Log(wx.Frame):
	def __init__(self, parent, id):
		wx.Frame.__init__(self,parent,id,'',size = (300,400), style = wx.DEFAULT_FRAME_STYLE)
		self.SetTitle("Log")
		self.Bind(wx.EVT_CLOSE,self.closewindow)
		
		
		self.SetDoubleBuffered(True)
		
		self.LogPanel = scrolled.ScrolledPanel(self, -1)
		self.LogPanel.SetupScrolling()

		self.LogPanel.SetBackgroundColour("white")
		
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer2 = wx.BoxSizer(wx.VERTICAL)
		sizer3 = wx.BoxSizer(wx.VERTICAL)
		a = 1
		self.boldFont = wx.Font(14,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_ITALIC,wx.FONTWEIGHT_BOLD)
		
		sizer2.Add(sizer3,1,wx.EXPAND)
		self.LogPanel.SetSizer(sizer2)
		self.LogPanel.Layout()
		sizer2.Fit(self.LogPanel)
		sizer.Add(self.LogPanel,1,wx.EXPAND)
		self.SetSizer(sizer)
		self.LogPanel.Layout()
		
		self.Centre()
		self.FlightInfoText = wx.StaticText(self.LogPanel, label = "\n  LOG\n  - ENTRY 1: \n  - ENTRY 2: \n  - ENTRY 3: \n  - ENTRY 4: \n  - ENTRY 5: \n  - ENTRY 6: \n  - ENTRY 7: \n  - ENTRY 8: \n  - ENTRY 9: ")
		self.FlightInfoText.SetFont(self.boldFont)
		
		sizer3.Add(self.FlightInfoText)
		
		self.LogPanel.SetAutoLayout(1)
		
		
		#panel=wx.Panel(self)
		#panel.SetBackgroundColour('White')

		
	def closewindow(self,event):
		self.Destroy()		