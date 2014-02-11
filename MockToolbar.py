import wx
import time
import sys
import os
import stomp
import wx.html2


coordinate1 = 50.0
coordinate2 = 50.0

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
		#panel = wx.Panel(self)
		self.html_view = wx.html2.WebView.New(self)
		dir_name=os.getcwd()+"/test.htm"
		self.html_view.LoadURL(dir_name)
		#self.html_view.SetPage("<html><body> hello </body></html>", "")
		
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
		
		#gpsSubButton = wx.Button(none,label="gps!",pos=(10,10),size=(90,90))
		#self.Bind(wx.EVT_BUTTON,self.gpsSubButtonMethod,gpsSubButton)	
		
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
		
		self.timer.Start(2000)
		#print g.showhtml()
		self.Show()
		
	def OnTimer(self, event):
		global g
		g.maps[0].zoom = self.count
		#dir_name=os.getcwd()+"/test.htm"
		#self.html_view.SetPage(str(g.showhtml()), "")
		#print(str(g.showhtml()))
		#self.html_view.LoadURL(dir_name)
		print("timer")
		self.count = self.count +1
		
	def gpsSubButtonMethod(self):
		print("clicked the button")

		
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
		
		
		g = PyMap()                         # creates an icon & map by default
		icon2 = Icon('icon2')               # create an additional icon
		icon2.image = "PlaneImage.png"
		#icon2.shadow = "http://labs.google.com/ridefinder/images/mm_20_shadow.png" # do not hotlink from your web page!
		g.addicon(icon2)
		g.key = "ABQIAAAAQQRAsOk3uqvy3Hwwo4CclBTrVPfEE8Ms0qPwyRfPn-DOTlpaLBTvTHRCdf2V6KbzW7PZFYLT8wFD0A" # you will get your own key
		g.maps[0].zoom = 5
		#q = [1,1]                           # create a marker with the defaults
		r = [coordinate1,coordinate2,'','icon2']              # icon2.id, specify the icon but no text
		#s = [3,3,'hello, <u>world</u>']     # don't specify an icon & get the default
		#g.maps[0].setpoint(q)               # add the points to the map
		g.maps[0].setpoint(r)
		#g.maps[0].setpoint(s)
		#print g.showhtml()
		open('test.htm','wb').write(g.showhtml())   # generate test file
		
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
    """
    Python wrapper class for Google Maps API.
    """
    
    def __str__(self):
        return "Pymap"
    
    def __init__(self, key=None, maplist=None, iconlist=None):
        """ Default values """
        self.key      = "ABQIAAAAQQRAsOk3uqvy3Hwwo4CclBTrVPfEE8Ms0qPwyRfPn-DOTlpaLBTvTHRCdf2V6KbzW7PZFYLT8wFD0A"      # set your google key
	#self.key = "AIzaSyBHpCyQYJ0p5GtkszIEWPIGoppDbwNzzrU"
        if maplist == None:
            self.maps = [Map()]
        else:
            self.maps = maplist
        if iconlist == None:
            self.icons = [Icon()]
        else:
            self.icons = iconlist
    
    def addicon(self,icon):
        self.icons.append(icon)
        
    def _navcontroljs(self,map):
        """ Returns the javascript for google maps control"""    
        if map.navcontrols:
            return  "           %s.gmap.addControl(new GSmallMapControl());\n" % (map.id)
        else:
            return ""    
    
    
    def _mapcontroljs(self,map):
        """ Returns the javascript for google maps control"""    
        if map.mapcontrols:
            return  "           %s.gmap.addControl(new GMapTypeControl());\n" % (map.id)
        else:
            return ""     
    
    
    def _showdivhtml(self,map):
        """ Returns html for dislaying map """
        html = """\n<div id=\"%s\">\n</div>\n""" % (map.id)
        return html
    
    def _point_hack(self, points):
        count = 1
        
        for item in points:
            open = str(item).replace("(", "[")
            open = open.replace(")", "]")
        
        return open
    
    
    def _mapjs(self,map):
        js = "%s_points = %s;\n" % (map.id,map.points)
        
        js = js.replace("(", "[")
        js = js.replace(")", "]")
        js = js.replace("u'", "'")
        js = js.replace("''","")    #python forces you to enter something in a list, so we remove it here
##        js = js.replace("'icon'", "icon")
        for icon  in self.icons:
            js = js.replace("'"+icon.id+"'",icon.id)
        js +=   """             %s = new Map('%s',%s_points,%s,%s,%s);
        \n\n%s\n%s""" % (map.id,map.id,map.id,map.center[0],map.center[1],map.zoom, self._mapcontroljs(map), self._navcontroljs(map))
        return js
    
    
    
    def _iconjs(self,icon):
        js = """ 
                %s = new GIcon(); 
                %s.image = "%s";
                %s.shadow = "%s";
                %s.iconSize = new GSize(%s, %s);
                %s.shadowSize = new GSize(%s, %s);
                %s.iconAnchor = new GPoint(%s, %s);
                %s.infoWindowAnchor = new GPoint(%s, %s);
        """ % (icon.id, icon.id, icon.image, icon.id, icon.shadow, icon.id, icon.iconSize[0],icon.iconSize[1],icon.id, icon.shadowSize[0], icon.shadowSize[1], icon.id, icon.iconAnchor[0],icon.iconAnchor[1], icon.id, icon.infoWindowAnchor[0], icon.infoWindowAnchor[1])
        return js
     
    def _buildicons(self):
        js = ""
        if (len(self.icons) > 0):
            for i in self.icons:
               js = js + self._iconjs(i)    
        return js
    
    def _buildmaps(self):
        js = ""
        for i in self.maps:
            js = js + self._mapjs(i)+'\n'
        return js

    def pymapjs(self):
        """ Returns complete javacript for rendering map """
        
        self.js = """\n<script src=\"http://maps.google.com/maps?file=api&amp;v=2&amp;key=%s\" type="text/javascript"></script>
        <script type="text/javascript">
        //<![CDATA[
		var map;
		var longPos = 1.0;
		var latPos = 1.0;
		var icon2;
		var icon;
        function load() {
            if (GBrowserIsCompatible()) {
                
            
            function Point(lat,long,html,icon) {
                  this.gpoint = new GMarker(new GLatLng(lat,long),icon);
                  this.html = html;
                  
               }               
               
               
               function Map(id,points,lat,long,zoom) {
                  this.id = id;
                  this.points = points;
                  this.gmap = new GMap2(document.getElementById(this.id));
                  this.gmap.setCenter(new GLatLng(lat, long), zoom);
                  this.markerlist = markerlist;
                  this.addmarker = addmarker;
                  this.array2points = array2points;
                   
                  function markerlist(array) {
                     for (var i in array) {
                        this.addmarker(array[i]);
                     }
                  }
                  
                  function array2points(map_points) {            
                      for (var i in map_points) {  
                        points[i] = new Point(map_points[i][0],map_points[i][1],map_points[i][2],map_points[i][3]);         }
                      return points;   
                    }                  
                  
                  function addmarker(point) {
                     if (point.html) {
                       GEvent.addListener(point.gpoint, "click", function() { // change click to mouseover or other mouse action
                           point.gpoint.openInfoWindowHtml(point.html);
                        
                       });
                       
                     }
                     this.gmap.addOverlay(point.gpoint);  
                  }
                  this.points = array2points(this.points);
                  this.markerlist(this.points);
            }  
                    %s
                    %s
            }
        }
		function updateMap()
		{
			map.gmap.setCenter(new GLatLng(longPos,latPos), 5);
			var mypoints = map.array2points([[longPos, latPos, , icon2]]);
			map.markerlist(mypoints);
			
			longPos += 1.0;
			latPos += 1.0;
		}
        //]]>
        </script>
        
        
        """ % (self.key, self._buildicons(),self._buildmaps())
        return self.js 
    
    
        
    def showhtml(self):
        """returns a complete html page with a map"""
        
        self.html = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <title></title>
    %s
  </head>

  <body onload="load()" onunload="GUnload()">
    <div id="map" style="width: 300px; height: 300px"></div>
  </body>
  <button type="button" onclick="updateMap()">Click to update the map!</button>
</html>
""" % (self.pymapjs())
        return self.html


		
if __name__ == '__main__':

	g = PyMap()                         # creates an icon & map by default
	icon2 = Icon('icon2')               # create an additional icon
	icon2.image = "PlaneImage.png"
	#icon2.shadow = "http://labs.google.com/ridefinder/images/mm_20_shadow.png" # do not hotlink from your web page!
	g.addicon(icon2)
	g.key = "ABQIAAAAQQRAsOk3uqvy3Hwwo4CclBTrVPfEE8Ms0qPwyRfPn-DOTlpaLBTvTHRCdf2V6KbzW7PZFYLT8wFD0A" # you will get your own key
	g.maps[0].zoom = 5
	#q = [1,1]                           # create a marker with the defaults
	r = [coordinate1,coordinate2,'','icon2']              # icon2.id, specify the icon but no text
	#s = [3,3,'hello, <u>world</u>']     # don't specify an icon & get the default
	#g.maps[0].setpoint(q)               # add the points to the map
	g.maps[0].setpoint(r)
	#g.maps[0].setpoint(s)
	#print g.showhtml()
	open('test.htm','wb').write(g.showhtml())   # generate test file
	
	app=wx.PySimpleApp()
	frame = TestFrame(parent = None, id=-1)
	frame.Show()
	app.MainLoop()