import wx
import time
import sys
import os
import stomp
import wx.html2
#import ee
from FGObject import FGObject
import FGParser

class Panel(wx.Panel):
	def __init__(self,parent,id,pos,size):
		wx.Panel.__init__(self,parent,id,pos,size)


class TCMFrame(wx.Frame):
	
	def __init__(self, parent, id):
		self.count = 1
		
		super(TCMFrame, self).__init__(parent, size=(1024,700), style = wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)
		self.mainPanel = wx.Panel(self)

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		mainSizer.Add(self.mainPanel,wx.EXPAND)

		self.mainPanel.SetBackgroundColour('grey')
		self.panel = Panel(self.mainPanel, -1, (300,0), (724,400))
		'''
		wx.Frame.__init__(self,parent,id,'Listener',size = (400,400))
		panel=wx.Panel(self)
        '''
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
		'''
		self.custom=wx.StaticText(self.panel,-1,"This is custom", (0,0), (260,-1),wx.ALIGN_CENTER)
		self.custom.SetLabel("test text")
		'''
		#set up gps view
		bSizer1 = wx.BoxSizer(wx.VERTICAL)
		bSizer5 = wx.BoxSizer(wx.HORIZONTAL)
		self.html_view = wx.html2.WebView.New(self.panel)
		bSizer5.Add(self.html_view,1,wx.EXPAND|wx.ALL,5)
		dir_name = os.getcwd()+"/test.htm"
		self.html_view.LoadURL(dir_name)

		self.timer.Start(400)
		self.panel.SetSizer( bSizer5 )

		bSizer5.Fit(self.panel )

		self.panel.Layout()

		bSizer1.Add( self.panel, wx.EXPAND )
		bSizer1.Fit(self.panel)
		mainSizer.Fit(self.mainPanel)


		self.Centre( wx.BOTH )


		self.SetSizer( mainSizer )
		#self.doLayout()
		self.Layout()

		#self.Centre( wx.BOTH )
		self.Show()
		self.fgObjects = {}

	def doLayout(self):
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.panel,5,wx.EXPAND)
		#sizer.Add(self.virtpanel,1,wx.EXPAND)
		self.SetSizer(sizer)


	def closewindow(self,event):
		self.Destroy()
	
	def OnTimer(self, event):
		self.updateTheView()

	def updateTheView(self):
		global coordinate1
		global coordinate2
		scriptString = """moveMarker(new google.maps.LatLng(%s,%s),map,marker)""" % (str(37.6136),str(-122.357))
		self.html_view.RunScript(scriptString)

	def update(self):
		#call function to update positions using extrapolation 
		return
	def updateFGObjs(self, string):
		if string is not None:
			fgPlayerDictsList = FGParser.parse(string)
			if len(fgPlayerDictsList) == 0:
				return
			for playerDict in fgPlayerDictsList:
				if "playername" not in playerDict:
					continue
				else:
					playerid = playerDict["playername"]
					if playerid in self.fgObjects:
						self.fgObjects[playerid].updateFromMessage(playerDict)
					else:
						newPlayer = FGObject(playerid, playerDict)
						self.fgObjects[playerid] = newPlayer
					

	def OnTimer(self, event):
		self.update()

	

		
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
            print("Received %s in %f seconds" % (self.count, diff))
            conn.disconnect()
            sys.exit(0)
        else:
            if self.count==0:
                self.start = time.time()
        
            self.count += 1
            print("Received %s message: %s" % (self.count,message))	  

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
	frame = TCMFrame(parent = None, id=-1)

	user = os.getenv("ACTIVEMQ_USER") or "admin"
	password = os.getenv("ACTIVEMQ_PASSWORD") or "password"
	host = os.getenv("ACTIVEMQ_HOST") or "localhost"
	port = os.getenv("ACTIVEMQ_PORT") or 61613
	#conn = stomp.Connection(host_and_ports = [(host, port)])
	conn = stomp.Connection(host_and_ports = [("35.9.22.201", port)])
	#conn = stomp.Connection(host_and_ports = [("10.0.1.17", port)])
	conn.set_listener('', MyListener(conn,frame))
	conn.start()
	conn.connect(login=user,passcode=password)
	conn.subscribe(destination="TEST.FOO", id=1, ack='auto')
	print("Waiting for messages...")
	
	frame.Show()
	app.MainLoop()

