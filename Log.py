import wx
import wx.lib.scrolledpanel as scrolled

class Log(wx.Frame):
	def __init__(self, parent, player, logObject, id):
		wx.Frame.__init__(self,parent,id,'',size = (500,400), style = wx.DEFAULT_FRAME_STYLE)
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
		self.boldFont = wx.Font(10,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_ITALIC,wx.FONTWEIGHT_BOLD)
		
		sizer2.Add(sizer3,1,wx.EXPAND)
		self.LogPanel.SetSizer(sizer2)
		self.LogPanel.Layout()
		sizer2.Fit(self.LogPanel)
		sizer.Add(self.LogPanel,1,wx.EXPAND)
		self.SetSizer(sizer)
		self.LogPanel.Layout()
		
		self.Centre()
		
		numFlights = len(logObject.prop_list['pastFlights'])
		
		textToDisplay = ("\n  FLIGHT LOG \n\n ---------------------------------------------------------------------- \n CURRENT FLIGHT (Flight# %s) \n\n Flight Name:  %s \n Flight Started at:  %s \n"%((numFlights+1),logObject.prop_list['name'],logObject.prop_list['startTime']))
		
		numPositions = len(logObject.prop_list['lat'])
		for x in range(0,numPositions):
			textToDisplay += ("     ENTRY %s: Time: %s, Latitude: %s, Longitude: %s \n"% (x+1,logObject.prop_list['times'][x],logObject.prop_list['lat'][x],logObject.prop_list['lon'][x]))
			#print(logObject.prop_list['lat'][x])
			#print(logObject.prop_list['lon'][x])
		#print numPositions
		if 'endtime' in logObject.prop_list:
			textToDisplay += (" Flight ended at: %s \n\n ---------------------------------------------------------------------- \n" % logObject.prop_list['endtime'])
		else:
			textToDisplay += " ---------------------------------------------------------------------- \n"
			
		
		for x in range(0,numFlights):
			#oldFlight_prop_list = logObject.prop_list['pastFlights'][x]
			textToDisplay += (" Flight #%s: \n\n Flight started at: %s \n"%((x+1),logObject.prop_list['pastFlights'][x]['startTime']))
			numPastPositions = len(logObject.prop_list['pastFlights'][x]['lat'])
			for y in range(0, numPastPositions):
				textToDisplay += ("     ENTRY %s: Time: %s, Latitude: %s, Longitude: %s \n" %( y+1, logObject.prop_list['pastFlights'][x]['times'][y],logObject.prop_list['pastFlights'][x]['lat'][y],logObject.prop_list['pastFlights'][x]['lon'][y]))
			textToDisplay += ( "Flight ended at: %s \n\n ---------------------------------------------------------------------- \n" % logObject.prop_list['pastFlights'][x]['endtime'])
			
		
		
		self.FlightInfoText = wx.StaticText(self.LogPanel, label = textToDisplay )
		self.FlightInfoText.SetFont(self.boldFont)
		
		sizer3.Add(self.FlightInfoText)
		
		self.LogPanel.SetAutoLayout(1)
		
		
		#panel=wx.Panel(self)
		#panel.SetBackgroundColour('White')

		
	def closewindow(self,event):
		self.Destroy()		