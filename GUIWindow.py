import wx
import time
import sys
import os
import stomp
import wx.html2

#global coordinates for the plane marker
coordinate1 = 0.0
coordinate2 = 0.0

class Panel(wx.Panel):
	def __init__(self,parent,id,pos,size):
		wx.Panel.__init__(self,parent,id,pos,size)

class GPSWindow(wx.Frame):
	def __init__(self, parent, id,):  
		
		self.count = 1
		
		super(GPSWindow, self).__init__(parent, size=(1024,700), style = wx.DEFAULT_FRAME_STYLE)

		gridSizer = wx.GridBagSizer(2,2)
		
		TopHorizSizer = wx.BoxSizer(wx.HORIZONTAL)
		LeftVertSizer = wx.BoxSizer(wx.VERTICAL)
		RightVertSizer = wx.BoxSizer(wx.VERTICAL)
		GPSSizer = wx.BoxSizer()
		BottomSizer = wx.BoxSizer()
		
		self.MainPanel = wx.Panel(self)
		self.MainPanel.SetBackgroundColour("orange")
		LeftPanel = wx.Panel(self.MainPanel,-1)
		LeftPanel.SetBackgroundColour("black")
		


		
		BottomPanel = wx.Panel(self.MainPanel,-1)
		BottomPanel.SetBackgroundColour("black")
		GPSPanel = wx.Panel(self.MainPanel,-1)
		GPSPanel.SetBackgroundColour("black")
		
		
		self.html_view = wx.html2.WebView.New(GPSPanel)
		dir_name=os.getcwd()+"/test.htm"
		self.html_view.LoadURL(dir_name)
		
		GPSSizer.Add(self.html_view,1,wx.EXPAND|wx.ALL,5)
		GPSPanel.SetSizer(GPSSizer)
		
		EnviInfoPanel = wx.Panel(LeftPanel,-1)
		EnviInfoPanel.SetBackgroundColour("white")
		
		boldFont = wx.Font(14,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_ITALIC,wx.FONTWEIGHT_BOLD)
		EnviInfoText = wx.StaticText(EnviInfoPanel,label="\n\n  Environment Info\n\n  - Time of Day:\n      Noon\n  - Sky Conditions:\n      Clear Skies\n  - Temperature:\n      54 Degrees F\n  - Wind Speed:\n      8 Knots\n  - Wind Direction:\n      North East\n")
		EnviInfoText.SetFont(boldFont)
		
		LeftVertSizer.Add(EnviInfoPanel,1,wx.EXPAND|wx.ALL,5)
		
		FlightInfoPanel = wx.Panel(BottomPanel,-1)
		FlightInfoPanel.SetBackgroundColour("white")
		FlightInfoText = wx.StaticText(FlightInfoPanel, label = "\n\n  Flight Info\n\n  - Latitude:  122.3478922   - Longitude:  37.456789   \n - Speed:  477.23 Knots \n  - Orientation:  North at 12 degrees\n  - Flight Time:  3hr 47min 12sec\n   - Current Time:  15:07:14")
		FlightInfoText.SetFont(boldFont)
		
		BottomSizer.Add(FlightInfoPanel,1,wx.EXPAND|wx.ALL,5)
		BottomPanel.SetSizer(BottomSizer)

		#FlightInfoText = wx.TextCtrl(BottomPanel, -1, "Here is a looooooooooooooong line of text set in the control.\n\n" "The quick brown fox jumped over the lazy dog...",size=(700, 700), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)

		#FlightInfoText.SetInsertionPoint(0)
		RightVertSizer.Add(GPSPanel,2,wx.EXPAND)
		RightVertSizer.Add(BottomPanel,1,wx.EXPAND)
		
		LeftPanel.SetSizer(LeftVertSizer)
		
		
		TopHorizSizer.Add(LeftPanel,1,wx.EXPAND)
		TopHorizSizer.Add(RightVertSizer,3,wx.EXPAND)
		
		gridSizer.Add(TopHorizSizer, pos=(4,4), span = (20,20), flag = wx.EXPAND)
		self.MainPanel.SetSizer(TopHorizSizer)

		
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
		
		
		user = os.getenv("ACTIVEMQ_USER") or "admin"
		password = os.getenv("ACTIVEMQ_PASSWORD") or "password"
		host = os.getenv("ACTIVEMQ_HOST") or "localhost"
		port = os.getenv("ACTIVEMQ_PORT") or 61613
		conn2 = stomp.Connection(host_and_ports = [(host, port)])
		#conn2 = stomp.Connection(host_and_ports = [("35.9.22.201", port)])
		#conn = stomp.Connection(host_and_ports = [("10.0.1.17", port)])
		conn2.set_listener('', MyListener(conn2,self))
		conn2.start()
		conn2.connect(login=user,passcode=password)
		conn2.subscribe(destination="TEST.FOO", id=1, ack='auto')
		print("Waiting for messages...")
		
		self.timer.Start(400)

		self.Show()
		
	def OnTimer(self, event):
		self.updateTheView()

	def updateTheView(self):
		global coordinate1
		global coordinate2
		scriptString = """moveMarker(new google.maps.LatLng(%s,%s),map,marker)""" % (str(coordinate1),str(coordinate2))
		self.html_view.RunScript(scriptString)
		

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
			var mapOptions = {zoom: 1,center: center};
			var image = {
				url: 'PlaneImage.png',
				// This marker is 20 pixels wide by 32 pixels tall.
				size: new google.maps.Size(1000, 1000),
				// The origin for this image is 0,0.
				origin: new google.maps.Point(0,0),
				// The anchor for this image is the base of the flagpole at 0,32.
				anchor: new google.maps.Point(10, 10)
			};
			map = new google.maps.Map(document.getElementById('map-canvas'),mapOptions);
			marker = new google.maps.Marker({position: center, map: map,icon: image, animation: google.maps.Animation.DROP});
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
	frame = GPSWindow(parent = None, id=-1)
	frame.Show()
	app.MainLoop()