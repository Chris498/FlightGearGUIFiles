import wx
import os

#This class is in charge of the GPS map panel in FlightTracker. It is essentially a panel that houses an html page.

class GPSPanel(wx.Panel):
	def __init__(self,parent,id):
		#initialize panel
		wx.Panel.__init__(self,parent,id)
		self.parent = parent
		self.SetBackgroundColour("black")
		self.SetDoubleBuffered(True)
		GPSSizer = wx.BoxSizer()
		#set html page to be the one created from the javascript
		self.parent.html_view = wx.html2.WebView.New(self)
		dir_name = os.getcwd()+"/test.htm"
		self.parent.html_view.LoadURL(dir_name)
		GPSSizer.Add(self.parent.html_view,1,wx.EXPAND)
		self.SetSizer(GPSSizer)
		
	#update the flight markers
	def UpdateMarker(self,name,FGObjects):
		fgobject = FGObjects[name]
	
	#create a new flight marker
	def CreateMarker(self,name,FGObjects):
		fgobject = FGObjects[name]
		coordinateLat = fgobject.prop_list['latitude-deg']
		coordinateLong = fgobject.prop_list['longitude-deg']
		scriptString = """addMarker(new google.maps.LatLng(%s,%s))""" % (str(20.0),str(30.0))