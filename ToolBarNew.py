import wx
import time
import sys
import os
import stomp
import wx.html2


coordinate1 = 0.0
coordinate2 = 0.0

class TestFrame(wx.MiniFrame):


	#initialize the frame
	def __init__(self, parent, id):
		wx.MiniFrame.__init__(self,parent,id,'',size = (770,110))
		panel=wx.Panel(self)
		panel.SetBackgroundColour('green')
		
		#create all of the toolbar buttons
		multi = wx.Image("Multi.png",wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		self.multi=wx.BitmapButton(panel,-1,multi,(10,10))
		self.Bind(wx.EVT_BUTTON, self.multiplayerButton,self.multi)
		self.multi.SetDefault()
		
		flightPlan = wx.Image("FlightPlan.png",wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		self.flightPlan = wx.BitmapButton(panel,-1,flightPlan,(160,10))
		self.Bind(wx.EVT_BUTTON,self.flightplanButton,self.flightPlan)
		self.flightPlan.SetDefault()
		
		gps = wx.Image("GPS.png",wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		self.gps = wx.BitmapButton(panel,-1,gps,(310,10))
		self.Bind(wx.EVT_BUTTON,self.gpsButton,self.gps)
		self.gps.SetDefault()
		
		log = wx.Image("Log.png",wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		self.log = wx.BitmapButton(panel,-1,log,(460,10))
		self.Bind(wx.EVT_BUTTON,self.logButton,self.log)
		self.log.SetDefault()
		
		otherFlights = wx.Image("OtherFlights.png",wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		self.otherFlights = wx.BitmapButton(panel,-1,otherFlights,(610,10))
		self.Bind(wx.EVT_BUTTON,self.otherFlightsButton,self.otherFlights)
		self.otherFlights.SetDefault()
		
		#self.timer = wx.Timer(self)
		#self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

		#self.timer.Start(2000)

	#def OnTimer(self,event):
		
		
	#button methods	
	def multiplayerButton(self,event):
		multiWindow = MultiplayerWindow(parent = frame, id= -1)
		multiWindow.Show()
		
	def flightplanButton(self,event):
		flightplanWindow = FlightplanWindow(parent = frame, id= -1)
		flightplanWindow.Show()
		
	def gpsButton(self,event):
		gpsWindow = GPSWindow(parent = frame, id = -1)
		
	def logButton(self,event):
		logWindow = LogWindow(parent = frame, id =-1)
		logWindow.Show()
	
	def otherFlightsButton(self, event):
		otherFlightsWindow = OtherFlightsWindow(parent = frame, id =-1)
		otherFlightsWindow.Show()
	
		
class MultiplayerWindow(wx.MiniFrame):
	
	def __init__(self, parent, id):
		wx.MiniFrame.__init__(self,parent,id,'Publisher',size = (400,400),style = wx.DEFAULT_FRAME_STYLE)
		self.panel=wx.Panel(self)
		send = wx.Button(self.panel,label="Send Message",pos=(10,100),size=(200,50))
		self.Bind(wx.EVT_BUTTON,self.sendButton,send)	
		self.Bind(wx.EVT_CLOSE,self.closewindow)
		wx.StaticText(self.panel, -1, "Message to Send:", pos=(10, 12))
		self.textBox = wx.TextCtrl(self.panel, -1, "Test it out and see", size=(125, -1), pos = (115,10))
		
	def sendButton(self,event):
		user = os.getenv("ACTIVEMQ_USER") or "admin"
		password = os.getenv("ACTIVEMQ_PASSWORD") or "password"
		host = os.getenv("ACTIVEMQ_HOST") or "localhost"
		port = os.getenv("ACTIVEMQ_PORT") or 61613


		conn = stomp.Connection(host_and_ports = [(host, port)])
		#conn = stomp.Connection(host_and_ports = [("35.9.22.201", port)])
		#conn = stomp.Connection(host_and_ports = [("10.0.1.17", port)])
		conn.start()
		conn.connect(login=user,passcode=password)
		
		textString = self.textBox.GetValue()

		conn.send(body=textString, destination='TEST.FOO')
  

		conn.disconnect()
	
	def closewindow(self,event):
		self.Destroy()

class FlightplanWindow(wx.MiniFrame):
	def __init__(self, parent, id):
		wx.MiniFrame.__init__(self,parent,id,'',size = (600,400), style = wx.DEFAULT_FRAME_STYLE)
		panel=wx.Panel(self)
		panel.SetBackgroundColour('green')
		self.Bind(wx.EVT_CLOSE,self.closewindow)
		
	def closewindow(self,event):
		self.Destroy()		
	

class GPSWindow(wx.Frame):
	def __init__(self, parent, id,):  
		
		#self.html_view = wx.html2.WebView.New(self)
		#print g.showhtml()		
		self.count = 1
	
		super(GPSWindow, self).__init__(parent, size=(350,365), style = wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)
		self.html_view = wx.html2.WebView.New(self)
		dir_name=os.getcwd()+"/test.htm"
		self.html_view.LoadURL(dir_name)
		#self.html_view.SetPage("<html><body> hello </body></html>", "")
		
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
		
		
		user = os.getenv("ACTIVEMQ_USER") or "admin"
		password = os.getenv("ACTIVEMQ_PASSWORD") or "password"
		host = os.getenv("ACTIVEMQ_HOST") or "localhost"
		port = os.getenv("ACTIVEMQ_PORT") or 61613
		conn2 = stomp.Connection(host_and_ports = [(host, port)])
		#conn = stomp.Connection(host_and_ports = [("35.9.22.201", port)])
		#conn = stomp.Connection(host_and_ports = [("10.0.1.17", port)])
		conn2.set_listener('', MyListener(conn2,self))
		conn2.start()
		conn2.connect(login=user,passcode=password)
		conn2.subscribe(destination="TEST.FOO", id=1, ack='auto')
		print("Waiting for messages...")
		
		self.timer.Start(500)
		self.Show()
		
	def OnTimer(self, event):
		self.updateTheView()

	def updateTheView(self):
		global coordinate1
		global coordinate2
		scriptString = """moveMarker(new google.maps.LatLng(%s,%s),map,marker)""" % (str(coordinate1),str(coordinate2))
		self.html_view.RunScript(scriptString)

		
class LogWindow(wx.MiniFrame):
	def __init__(self, parent, id):
		wx.MiniFrame.__init__(self,parent,id,'',size = (200,400), style = wx.DEFAULT_FRAME_STYLE)
		panel=wx.Panel(self)
		panel.SetBackgroundColour('green')
		self.Bind(wx.EVT_CLOSE,self.closewindow)
		
	def closewindow(self,event):
		self.Destroy()
		
class OtherFlightsWindow(wx.MiniFrame):
	def __init__(self, parent, id):
		wx.MiniFrame.__init__(self,parent,id,'',size = (200,400), style = wx.DEFAULT_FRAME_STYLE)
		panel=wx.Panel(self)
		panel.SetBackgroundColour('green')
		self.Bind(wx.EVT_CLOSE,self.closewindow)
		
	def closewindow(self,event):
		self.Destroy()

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
    self.frame = frame
  
  def on_error(self, headers, message):
    print('received an error %s' % message)

  def on_message(self, headers, message):	
    if message == "SHUTDOWN":
      conn.disconnect()
      sys.exit(0)
      
    else:
		coordinates = message.split()
		
		global coordinate1
		global coordinate2
		coordinate1 = float(coordinates[0])
		coordinate2 = float(coordinates[1])
		
		
		#g = PyMap()                         # creates an icon & map by default
		#icon2 = Icon('icon2')               # create an additional icon
		#icon2.image = "PlaneImage.png"
		#g.addicon(icon2)
		#g.key = "ABQIAAAAQQRAsOk3uqvy3Hwwo4CclBTrVPfEE8Ms0qPwyRfPn-DOTlpaLBTvTHRCdf2V6KbzW7PZFYLT8wFD0A" # you will get your own key
		#g.maps[0].zoom = 5
		#r = [coordinate1,coordinate2,'','icon2']              # icon2.id, specify the icon but no text
		#g.maps[0].setpoint(r)
		#open('test.htm','wb').write(g.showhtml())   # generate test file
		
		print(coordinate1)
		print(coordinate2)
		
		print("Received message: %s" % message)
	  

   
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
		var marker;
		var center;
		var poly;
		var infowindow;
		function initialize() {
			center = new google.maps.LatLng(0.0,0.0);
			var mapOptions = {zoom: 4,center: center};
			var image = {
				url: 'PlaneImage.png',
				// This marker is 20 pixels wide by 32 pixels tall.
				size: new google.maps.Size(50, 50),
				// The origin for this image is 0,0.
				origin: new google.maps.Point(0,0),
				// The anchor for this image is the base of the flagpole at 0,32.
				anchor: new google.maps.Point(10, 10)
			};
			map = new google.maps.Map(document.getElementById('map-canvas'),mapOptions);
			marker = new google.maps.Marker({position: center, map: map,icon: image, animation: google.maps.Animation.DROP});
			var polyOptions = {
			strokeColor: '#FFA500',
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
			
			google.maps.event.addListener(marker, 'click', function() {
				infowindow.setContent(createInfoWindowContent());
				infowindow.open(map,marker);
			});


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
	frame = TestFrame(parent = None, id=-1)
	frame.Show()
	app.MainLoop()