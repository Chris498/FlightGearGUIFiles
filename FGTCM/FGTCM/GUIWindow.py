import wx
import time
import sys
import os
import stomp
import wx.html2

from FGObject import FGObject
import FGParser

#global coordinates for the plane marker
coordinate1 = 0.0
coordinate2 = 0.0

class Panel(wx.Panel):
	def __init__(self,parent,id,pos,size):
		wx.Panel.__init__(self,parent,id,pos,size)
		
	def Update(self):
		return
		
class EnvironmentPanelBackground(wx.Panel):
	def __init__(self,parent,id):
		wx.Panel.__init__(self,parent,id)
		self.SetBackgroundColour("blue")
		
		self.EnviInfoPanel = EnvironmentPanel(self,-1)
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		sizer.Add(self.EnviInfoPanel,1,wx.EXPAND|wx.ALL,5)
		
		self.SetSizer(sizer)
		
	def Update(self):
		#print("update EnvironmentPanelBackground")
		self.EnviInfoPanel.Update()
		
class GPSPanel(wx.Panel):
	def __init__(self,parent,id):
		wx.Panel.__init__(self,parent,id)
		self.parent = parent
		self.SetBackgroundColour("grey")
		GPSSizer = wx.BoxSizer()
		self.parent.html_view = wx.html2.WebView.New(self)
		dir_name = os.getcwd()+"/test.htm"
		self.parent.html_view.LoadURL(dir_name)
		GPSSizer.Add(self.parent.html_view,1,wx.EXPAND|wx.ALL,5)
		self.SetSizer(GPSSizer)
		#scriptString = """addMarker(new google.maps.LatLng(%s,%s))""" % (str(10.1),str(20.1))
		#parent.html_view.RunScript(scriptString)
		#self.HTML_VIEW = parent.html_view
		
	def UpdateMarker(self,name,FGObjects):
		fgobject = FGObjects[name]
		print("updating the marker")
	
	def CreateMarker(self,name,FGObjects):
		fgobject = FGObjects[name]
		coordinateLat = fgobject.prop_list['latitude-deg']
		coordinateLong = fgobject.prop_list['longitude-deg']
		print("coordinateLat %s"%coordinateLat)
		print("coordinateLong %s"%coordinateLong)
		scriptString = """addMarker(new google.maps.LatLng(%s,%s))""" % (str(20.0),str(30.0))
		print(scriptString)
		#self.parent.html_view.RunScript(scriptString)
		#self.parent.CallJavaScriptFunction(scriptString)
		#return scriptString

		print("creating the marker")

class FlightStatusPanelBackground(wx.Panel):
	def __init__(self,parent,id):
		wx.Panel.__init__(self,parent,id)
		self.SetBackgroundColour("green")
		
		self.FlightInfoPanel = FlightPanel(self,-1)
		
		sizer = wx.BoxSizer()
		
		sizer.Add(self.FlightInfoPanel,1,wx.EXPAND|wx.ALL,5)
		
		self.SetSizer(sizer)
		
	def Update(self):
		self.FlightInfoPanel.Update()
		
class EnvironmentPanel(wx.Panel):
	def __init__(self,parent,id):
		wx.Panel.__init__(self,parent,id)
		self.SetBackgroundColour("white")
		
		boldFont = wx.Font(14,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_ITALIC,wx.FONTWEIGHT_BOLD)

		EnviInfoText = wx.StaticText(self,label="\n\n  Environment Info\n\n  - Time of Day:\n      Noon\n  - Sky Conditions:\n      Clear Skies\n  - Temperature:\n      54 Degrees F\n  - Wind Speed:\n      8 Knots\n  - Wind Direction:\n      North East\n")
		EnviInfoText.SetFont(boldFont)		
		
	def Update(self):
		return
		
class FlightPanel(wx.Panel):
	def __init__(self,parent,id):
		wx.Panel.__init__(self,parent,id)
		self.SetBackgroundColour("white")
		
		boldFont = wx.Font(14,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_ITALIC,wx.FONTWEIGHT_BOLD)
		
		FlightInfoText = wx.StaticText(self, label = "\n\n  Flight Info\n\n  - Latitude:  122.3478922   - Longitude:  37.456789   \n - Speed:  477.23 Knots \n  - Orientation:  North at 12 degrees\n  - Flight Time:  3hr 47min 12sec\n   - Current Time:  15:07:14")
		FlightInfoText.SetFont(boldFont)
		
	def Update(self):
		return
		

class GPSWindow(wx.Frame):
	def __init__(self, parent, id,):  
		
		
		super(GPSWindow, self).__init__(parent, size=(1024,700), style = wx.DEFAULT_FRAME_STYLE)
		
		#The top most sizer that splits the screen horizontally
		TopHorizSizer = wx.BoxSizer(wx.HORIZONTAL)
		
		#The rest of the sizers
		RightVertSizer = wx.BoxSizer(wx.VERTICAL)
		GPSSizer = wx.BoxSizer()
		#self.html_view = wx.html2.WebView.New(self)
		
		#The main panel all others will be parented to
		self.MainPanel = wx.Panel(self)
		self.MainPanel.SetBackgroundColour("orange")
		#The other sub panels
		self.EnvironmentInfoBackground = EnvironmentPanelBackground(self.MainPanel,-1)
		self.FlightInfoBackground = FlightStatusPanelBackground(self.MainPanel,-1)
		self.GPS = GPSPanel(self.MainPanel,-1)

		#add sub panels to the right sizer
		RightVertSizer.Add(self.GPS,2,wx.EXPAND)
		RightVertSizer.Add(self.FlightInfoBackground,1,wx.EXPAND)
		
		#add the left sub panel and right sizer to the main horizontal sizer
		TopHorizSizer.Add(self.EnvironmentInfoBackground,1,wx.EXPAND)
		TopHorizSizer.Add(RightVertSizer,3,wx.EXPAND)
		
		#set the main panel's sizer
		self.MainPanel.SetSizer(TopHorizSizer)

		#initiate timer and timer event
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
		
		self.timer.Start(400)
		self.fgObjects = {}
	
	#called on every timer event, updates the main panel
	def OnTimer(self, event):
		self.updateTheView()

	#updates main panel which will update all sub panels
	def updateTheView(self):
		global coordinate1
		global coordinate2
		#self.GPS.Update(self.fgObjects)
		self.EnvironmentInfoBackground.Update()
		self.FlightInfoBackground.Update()
		#scriptString = """moveMarker(new google.maps.LatLng(%s,%s),map,marker)""" % (str(coordinate1),str(coordinate2))
		#self.MainPanel.html_view.RunScript(scriptString)
		scriptString = """deleteMarkers()"""
		self.MainPanel.html_view.RunScript(scriptString)
		for name,playerDict in self.fgObjects.iteritems():
			#print(name)
			lat = ""
			lon = ""
			for property,value in playerDict.prop_list.iteritems():
				#print("%s: %s"%(property,value))
				if(property == "latitude-deg"):
					lat = value
					#print(lat)
				if(property == "longitude-deg"):
					lon = value
					#print(lon)
			scriptString = """updateMarker(%s,%s)""" % (str(lat),str(lon))
			self.MainPanel.html_view.RunScript(scriptString)
			
			
		coordinate1 +=1
		coordinate2 +=2
		
		#scriptString = """updateMarkers(new google.maps.LatLng(%s,%s))"""%(str(coordinate1),str(coordinate2))
		#self.MainPanel.html_view.RunScript(scriptString)
		
	def callJavaScriptFunction(stringCommand):
		#self.MainPanel.html_view.RunScript(stringCommand)
		print("call this function")

		
	def updateFGObjs(self, string):
		if string is not None:
			fgPlayerDictsList = FGParser.parse(string)
			#print("here")
			if len(fgPlayerDictsList) == 0:
				return
			for playerDict in fgPlayerDictsList:
				if "playername:" not in playerDict:
					#print("not in")
					continue
				else:
					playerid = playerDict["playername:"]
					if playerid in self.fgObjects:
						self.fgObjects[playerid].updateFromMessage(playerDict)
						#self.GPS.UpdateMarker(playerid,self.fgObjects)
						#print("update -------------- %s"% playerDict)
					else:
						newPlayer = FGObject(playerid, playerDict)
						self.fgObjects[playerid] = newPlayer
						#self.GPS.CreateMarker(playerid,self.fgObjects)
						#commandString = """addMarker(new google.maps.LatLng(%s,%s))"""%(str(2.0),str(10.0))
						#self.MainPanel.html_view.RunScript(commandString)
						#print("create-------------------- %s"% playerDict)
		

class Icon:
    #'''Get/make marker icons at http://mapki.com/index.php?title=Icon_Image_Sets'''
    def __init__(self,id='icon'):
        self.id = id
        #self.image = ""     #uses default Google Maps icon
        self.shadow = ""
		
		
        self.image = ""
        self.iconSize = (12, 20)    # these settings match above icons
        self.shadowSize = (22, 20)
        self.iconAnchor = (6, 20)
        self.infoWindowAnchor = (5, 1)

   

class MyListener(object):
  
  def __init__(self, conn, frame):
    self.conn = conn
    self.count = 0
    self.start = time.time()
    self.frame = frame
  
  def on_error(self, headers, message):
    print('received an error %s' % message)

  def on_message(self, headers, message):
    self.frame.updateFGObjs(message)
    if message == "SHUTDOWN":
      diff = time.time() - self.start
      print('disconnecting')
      self.conn.disconnect()
      sys.exit(0)
      
    else:
		if self.count==0:
			self.start = time.time()
		self.count += 1
		coordinates = message.split()
		
		#global coordinate1
		#global coordinate2
		#coordinate1 = float(coordinates[0])
		#coordinate2 = float(coordinates[1])
		
		
		#print(coordinate1)
		#print(coordinate2)
		
		#print("Received message: %s" % message)
	  

   
class Map:
    def __init__(self,id="map",pointlist=None):
        global coordiante1
        global coordinate2
        self.id       = id    # div id        
        #self.width    = "500px"  # map div width
        #self.height   = "300px"  # map div height
        self.center   = (coordinate1,coordinate2)     # center map latitude coordinate
        self.zoom        = "1"   # zoom level
        self.navcontrols  =   True   # show google map navigation controls
        self.mapcontrols  =   True   # show toogle map type (sat/map/hybrid) controls
        if pointlist == None:
            self.points = []   # empty point list
        else:
            self.points = pointlist   # supplied point list
    
    def __str__(self):
        return self.id
        
    
    def setpoint(self, point):
        """ Add a point (lat,long,html,icon) """
        self.points.append(point)
	

class PyMap:
    def GoogleMapPy(self):
		""" Returns complete javacript for rendering map """
        
		self.js = """<script src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false"></script>
		<script>
		var map;
		//var marker;
		var center;
		var poly;
		var infowindow;
		var image;
		var markers = [];
		function initialize() {
			center = new google.maps.LatLng(0.0,0.0);
			var mapOptions = {zoom: 1,center: center};
			image = {
				url: 'PlaneImage.png',
				// This marker is 20 pixels wide by 32 pixels tall.
				size: new google.maps.Size(1000, 1000),
				// The origin for this image is 0,0.
				origin: new google.maps.Point(0,0),
				// The anchor for this image is the base of the flagpole at 0,32.
				anchor: new google.maps.Point(10, 10)
			};
			map = new google.maps.Map(document.getElementById('map-canvas'),mapOptions);
			//marker = new google.maps.Marker({position: center, map: map,icon: image, animation: google.maps.Animation.DROP});
			var polyOptions = {
			strokeColor: '#FF00FF',
			strokeOpacity: 1.0,
			strokeWeight: 3
			};
			poly = new google.maps.Polyline(polyOptions);
			poly.setMap(map);
			
			//var contentString = ['coordinates','Latitude: ' + marker.getPosition().lat(), 'Longitude: '+marker.getPosition().lng()].join('<br>');
			
			function createInfoWindowContent(){
				return[
					'Coordinates:',
					'Latitude: ' + marker.getPosition().lat(),
					'Longitude: ' + marker.getPosition().lng()
				].join('<br>');
			}
			infowindow = new google.maps.InfoWindow();
			
			//google.maps.event.addListener(marker, 'click', function() {
			//	infowindow.setContent(createInfoWindowContent());
			//	infowindow.open(map,marker);
			//});
			
			google.maps.event.addListener(map,'click',function(event) {
				addMarker(event.latLng,'click');
			});
			


		}
		
		// Sets the map on all markers in the array.
		function setAllMap(map) {
			for (var i = 0; i < markers.length; i++) {
				markers[i].setMap(map);
			}
		}		

		// Removes the markers from the map, but keeps them in the array.
		function clearMarkers() {
			setAllMap(null);
		}

		// Shows any markers currently in the array.
		function showMarkers() {
			setAllMap(map);
		}

		// Deletes all markers in the array by removing references to them.
		function deleteMarkers() {
			clearMarkers();
			markers = [];
		}

		function moveMarker(position, map, marker) {
			//infowindow.close();
			var path = poly.getPath();
			path.push(position);
			marker.setPosition(position);
			map.panTo(position);
			//infowindow.setContent(createInfoWindowContent());
			//infowindow.open(map,marker);
		}
		
		function addMarker(location) {
			alert("addmarker");
			var marker2 = new google.maps.Marker({
				position: location,
				map: map,
				icon: image
			});
			//map.panTo(location);
			markers.push(marker2);
		}
		function addMarker2(lat, lon) {
			var location = new google.maps.LatLng(lat,lon);
			var marker2 = new google.maps.Marker({
				position: location,
				map: map,
				icon: image
			});
			//map.panTo(location);
			markers.push(marker2);
		}
		
		function updateMarker(lat, lon) {
			addMarker2(lat, lon);
		}
		
		function createAlert() {
			alert("Alert created");
		}

		google.maps.event.addDomListener(window, 'load', initialize);

		</script>
		"""
		return self.js 
        
    def showhtml(self):
		"""returns a complete html page with a map"""
        
		self.html = """
		<!DOCTYPE html>
<html>
  <head>
    <title>Accessing arguments in UI events</title>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <style>
      html, body, #map-canvas {
        height: 100%%;
        margin: 0px;
        padding: 0px
      }
    </style>
    %s
  </head>
  <body>
    <div id="map-canvas"></div>
  </body>
</html>
		""" % self.GoogleMapPy()
		return self.html
		
if __name__ == '__main__':

	g = PyMap()                         
	open('test.htm','wb').write(g.showhtml())   # generate test file
	

	
	app=wx.PySimpleApp()
	frame = GPSWindow(parent = None, id=-1)
	
	#------------------------------------------------------------------------
	###
	### The Stomp/broker information
	###
	user = os.getenv("ACTIVEMQ_USER") or "admin"
	password = os.getenv("ACTIVEMQ_PASSWORD") or "password"
	host = os.getenv("ACTIVEMQ_HOST") or "localhost"
	port = os.getenv("ACTIVEMQ_PORT") or 61613
	conn2 = stomp.Connection(host_and_ports = [(host, port)])
	#conn2 = stomp.Connection(host_and_ports = [("35.9.22.201", port)])
	#conn = stomp.Connection(host_and_ports = [("10.0.1.17", port)])
	conn2.set_listener('', MyListener(conn2,frame))
	conn2.start()
	conn2.connect(login=user,passcode=password)
	conn2.subscribe(destination="TEST.FOO", id=1, ack='auto')
	print("Waiting for messages...")
	#-----------------------------------------------------------------------------
	
	frame.Show()
	app.MainLoop()