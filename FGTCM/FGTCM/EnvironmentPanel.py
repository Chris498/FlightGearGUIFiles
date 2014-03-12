import wx
import wx.lib.scrolledpanel as scrolled

class EnvironmentPanel(wx.Panel):
	def __init__(self,parent,id):
		wx.Panel.__init__(self,parent,id)
		self.SetBackgroundColour("black")
		self.SetDoubleBuffered(True)
		self.FlightInfoPanel = scrolled.ScrolledPanel(self, -1)
		self.FlightInfoPanel.SetupScrolling()

		self.FlightInfoPanel.SetBackgroundColour("white")
		
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer2 = wx.BoxSizer(wx.VERTICAL)
		sizer3 = wx.BoxSizer(wx.VERTICAL)
		
		self.boldFont = wx.Font(14,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_ITALIC,wx.FONTWEIGHT_BOLD)
		
		sizer2.Add(sizer3,1,wx.EXPAND)
		self.FlightInfoPanel.SetSizer(sizer2)
		self.FlightInfoPanel.Layout()
		sizer2.Fit(self.FlightInfoPanel)
		sizer.Add(self.FlightInfoPanel,1,wx.EXPAND)
		self.SetSizer(sizer)
		self.FlightInfoPanel.Layout()
		
		self.Centre()
		self.EnvironmentInfoText = wx.StaticText(self.FlightInfoPanel, label = "\n\n  Environment Info\n\n  - Weather Scenario:\n      \n  - Sky Conditions:\n      \n  - Temperature:\n      \n  - Wind Speed:\n      \n  - Wind Direction:\n      \n")
		self.EnvironmentInfoText.SetFont(self.boldFont)
		
		sizer3.Add(self.EnvironmentInfoText)
		
		self.FlightInfoPanel.SetAutoLayout(1)
		
	def UpdateText(self,weatherScenario,skyConditions,temperature,windSpeed,windDirection):
		self.EnvironmentInfoText.SetLabel("\n\n  Environment Info\n\n  - Weather Scenario:\n   %s   \n  - Sky Conditions:\n   %s   \n  - Temperature:\n   %s Deg F  \n  - Wind Speed:\n   %s Knots  \n  - Wind Direction:\n   %s Deg  \n"%(weatherScenario,skyConditions,temperature,windSpeed,windDirection))