import wx
import wx.lib.scrolledpanel as scrolled
from datetime import datetime

class FlightPanel(wx.Panel):
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
		self.FlightInfoText = wx.StaticText(self.FlightInfoPanel, label = "\n  Flight Info\n\n  - Flight Name:  \n  - Latitude:     - Longitude:     \n - Speed:   \n  - Heading:  \n  - Altitude:   \n  - Current Fuel:  \n  - Total Fuel Capacity:  \n  - Flight Time:  \n   - Current Time:")
		self.FlightInfoText.SetFont(self.boldFont)
		
		sizer3.Add(self.FlightInfoText)
		
		self.FlightInfoPanel.SetAutoLayout(1)
	
	def updateText(self,name,lat,lon,speed,heading,alt,currentFuel,fuelCapacity,elapsedTime):
		#print("update the text")

		currentTime = datetime.now()
		self.FlightInfoText.SetLabel("\n  Flight Info\n\n  - Flight Name:  %s  \n  - Latitude:  %s Deg - Longitude:  %s Deg \n  - Speed:  %s Knots \n  - Heading:  %s Deg \n  - Altitude:  %s Ft? \n  - Current Fuel:  %s Gals? \n  - Total Fuel Capacity:  %s Gals?\n  - Flight Time:  %s\n  - Current Time:  %s"%(name,lat,lon,speed,heading,alt,currentFuel,fuelCapacity,elapsedTime,currentTime))
