import wx
import time
import sys
import os
import stomp
import wx.html2
import math
import wx.lib.scrolledpanel as scrolled

from datetime import datetime
from FGObject import FGObject
import FGParser

#global coordinates for the plane marker
coordinate1 = 0.0
coordinate2 = 0.0
currentDisplayFlight= "Player"

class Panel(wx.Panel):
	def __init__(self,parent,id,pos,size):
		wx.Panel.__init__(self,parent,id,pos,size)
		
	def Update(self):
		return
		
class EnvironmentPanelBackground(wx.Panel):
	def __init__(self,parent,id):
		wx.Panel.__init__(self,parent,id)
		self.SetBackgroundColour("black")
		
		self.EnviInfoPanel = EnvironmentPanel(self,-1)
		
		sizer = wx.BoxSizer()
		
		sizer.Add(self.EnviInfoPanel,1,wx.EXPAND|wx.ALL,5)
		
		self.SetSizer(sizer)
		
	def Update(self):
		#print("update EnvironmentPanelBackground")
		self.EnviInfoPanel.Update()

class PlaneSelectPanelBackground(wx.Panel):
	def __init__(self,parent,id):
		wx.Panel.__init__(self,parent,id)
		self.SetBackgroundColour("Black")
		self.parent = parent
		self.FlightInfoClass = ""
		self.panel = wx.Panel(self, -1)
		self.panel.SetBackgroundColour("white")
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.boldFont = wx.Font(14,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_ITALIC,wx.FONTWEIGHT_BOLD)

		#button = wx.Button(self.panel,-1,"Button")

		self.vbox = wx.BoxSizer(wx.VERTICAL)
		#self.vbox.Add(button)

		#add_btn = wx.Button(self.panel,-1,"Add")
		#add_btn.Bind(wx.EVT_BUTTON, self.add)

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		#hbox.Add(add_btn)

		main_vbox = wx.BoxSizer(wx.VERTICAL)
		main_vbox.Add(self.vbox,1,wx.EXPAND|wx.ALL,5)
		main_vbox.Add(hbox)

		self.panel.SetSizer(main_vbox)
		mainSizer.Add(self.panel,1,wx.EXPAND|wx.ALL,5)
		self.SetSizer(mainSizer)
		self.panel.Layout()
		
		self.group1_ctrls = []

		self.Centre()
		self.Show(True)
		
		self.SelectionInfo = wx.StaticText(self.panel, label = "  Select A Flight")
		self.SelectionInfo.SetFont(self.boldFont)
		self.vbox.Add(self.SelectionInfo)

	def add(self,event):
		#self.vbox.Add((wx.RadioButton(self.panel,-1,"Button")))
		#self.panel.Layout()
		self.addRadio("wahoo")
		
	def addRadio(self,name):
		found = 0
		for theName in self.group1_ctrls:
			if theName == name:
				found = 1
		if(found ==0):
			radioButton = wx.RadioButton(self.panel,-1,name)
			radioButton.SetFont(self.boldFont)
			self.vbox.Add(radioButton)
			self.panel.Layout()
			self.group1_ctrls.append(name)
			self.panel.Bind(wx.EVT_RADIOBUTTON, self.OnGroup1Select, radioButton )
			if(name == "Player"):
				radioButton.SetValue(1)
			else:
				radioButton.SetValue(0)
	
	def OnGroup1Select( self, event ):
		global currentDisplayFlight
		radio_selected = event.GetEventObject()
		print('Group1 %s selected\n' % radio_selected.GetLabel() )
		currentDisplayFlight = radio_selected.GetLabel()
		#self.FlightInfoClass.updateText(radio_selected.GetLabel(),
		#self.parent.EnvironmentInfoBackground
		

	def updateFlightInfoObject(self,object):
		self.FlightInfoClass = object
		

class PlaneSelectPanel(scrolled.ScrolledPanel):
	def __init__(self,parent,id):
		scrolled.ScrolledPanel.__init__(self,parent,id)
		#self.panel = scrolled.ScrolledPanel(self)
		self.SetBackgroundColour("white")
		#boldFont = wx.Font(14,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_ITALIC,wx.FONTWEIGHT_BOLD)
		self.vbox = wx.BoxSizer(wx.VERTICAL)
		self.grid1 = wx.FlexGridSizer( cols=1 )
		self.group1_ctrls = []
		
		#self.ScrolledPanel = PlaneSelectPanel
		
		#radio1 = wx.RadioButton( self, -1, " Radio1 ", style = wx.RB_GROUP )
		#radio2 = wx.RadioButton( self, -1, " Radio2 " )
		# radio3 = wx.RadioButton( self, -1, " Radio3 " )
		
		# self.group1_ctrls.append(radio1)
		# self.group1_ctrls.append(radio2)
		# self.group1_ctrls.append(radio3)
		
		# radio4 = wx.RadioButton( self, -1, " Radio1 ", style = wx.RB_GROUP )
		# radio5 = wx.RadioButton( self, -1, " Radio2 " )
		# radio6 = wx.RadioButton( self, -1, " Radio3 " )
		
		# self.group1_ctrls.append(radio4)
		# self.group1_ctrls.append(radio5)
		# self.group1_ctrls.append(radio6)
		
		# radio7 = wx.RadioButton( self, -1, " Radio1 ", style = wx.RB_GROUP )
		# radio8 = wx.RadioButton( self, -1, " Radio2 " )
		# radio9 = wx.RadioButton( self, -1, " Radio3 " )
		
		# self.group1_ctrls.append(radio7)
		# self.group1_ctrls.append(radio8)
		# self.group1_ctrls.append(radio9)
		
		# radio10 = wx.RadioButton( self, -1, " Radio1 ", style = wx.RB_GROUP )
		# radio11 = wx.RadioButton( self, -1, " Radio2 " )
		# radio12 = wx.RadioButton( self, -1, " Radio3 " )
		
		# self.group1_ctrls.append(radio10)
		# self.group1_ctrls.append(radio11)
		# self.group1_ctrls.append(radio12)
		
		#for radio in self.group1_ctrls:
			#self.grid1.Add( radio, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
			
		# self.desc = wx.StaticText(self, -1,"\n  Select a Flight:")
		# self.desc.SetForegroundColour("Black")
		# self.desc.SetFont(boldFont)
		
		# self.vbox.Add(self.desc, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		# self.box1 = wx.BoxSizer(wx.VERTICAL)
		# self.box1.Add( self.grid1, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		# self.vbox.Add( self.box1, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )		
		

		
		self.SetSizer(self.vbox)
		self.vbox.Fit(self)
		self.SetAutoLayout(1)
		self.SetupScrolling()
		
		# for radio in self.group1_ctrls:
			# self.Bind(wx.EVT_RADIOBUTTON, self.OnGroup1Select, radio )
			
		# for radio in self.group1_ctrls:
		# radio.SetValue(0)
	
			
	def OnGroup1Select(self,event):
		radio_selected = event.GetEventObject()
		
	def updateButtons():
		return



	def Update(self):
		return	

class GPSPanel(wx.Panel):
	def __init__(self,parent,id):
		wx.Panel.__init__(self,parent,id)
		self.parent = parent
		self.SetBackgroundColour("black")
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
		#print("updating the marker")
	
	def CreateMarker(self,name,FGObjects):
		fgobject = FGObjects[name]
		coordinateLat = fgobject.prop_list['latitude-deg']
		coordinateLong = fgobject.prop_list['longitude-deg']
		#print("coordinateLat %s"%coordinateLat)
		#print("coordinateLong %s"%coordinateLong)
		scriptString = """addMarker(new google.maps.LatLng(%s,%s))""" % (str(20.0),str(30.0))
		#print(scriptString)
		#self.parent.html_view.RunScript(scriptString)
		#self.parent.CallJavaScriptFunction(scriptString)
		#return scriptString

		#print("creating the marker")

class FlightStatusPanelBackground(wx.Panel):
	def __init__(self,parent,id):
		wx.Panel.__init__(self,parent,id)
		self.SetBackgroundColour("black")
		
		self.FlightInfoPanel = FlightPanel(self,-1)
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		sizer.Add(self.FlightInfoPanel,1,wx.EXPAND|wx.ALL,5)
		
		self.SetSizer(sizer)
		sizer.Fit(self)
		
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
		self.SetDoubleBuffered(True)
		self.SetBackgroundColour("white")
		
		self.boldFont = wx.Font(14,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_ITALIC,wx.FONTWEIGHT_BOLD)
		#sizer = wx.BoxSizer()
		self.FlightInfoText = wx.StaticText(self, label = "\n  Flight Info\n\n  - Flight Name:  \n  - Latitude:     - Longitude:     \n - Speed:   \n  - Orientation:  \n  - Flight Time:  \n   - Current Time:")
		self.FlightInfoText.SetFont(self.boldFont)
		#sizer.Add(FlightInfoText,0,wx.EXPAND)
		#self.SetSizer(sizer)
		
	def updateText(self,name,lat,lon,elapsedTime):
		#print("update the text")
		currentTime = datetime.now()
		self.FlightInfoText.SetLabel("\n  Flight Info\n\n  - Flight Name:  %s  \n  - Latitude:  %s  - Longitude:  %s   \n  - Speed:   \n  - Orientation: \n  - Flight Time:  %s\n  - Current Time:  %s"%(name,lat,lon,elapsedTime,currentTime))
		
	def Update(self):
		return
		

class GPSWindow(wx.Frame):
	def __init__(self, parent, id,):  
		
		
		super(GPSWindow, self).__init__(parent, size=(1024,700), style = wx.DEFAULT_FRAME_STYLE)
		
		#The top most sizer that splits the screen horizontally
		TopHorizSizer = wx.BoxSizer(wx.HORIZONTAL)
		
		#The rest of the sizers
		RightVertSizer = wx.BoxSizer(wx.VERTICAL)
		LeftVertSizer = wx.BoxSizer(wx.VERTICAL)
		GPSSizer = wx.BoxSizer()
		#self.html_view = wx.html2.WebView.New(self)
		
		#The main panel all others will be parented to
		self.MainPanel = wx.Panel(self)
		self.MainPanel.SetBackgroundColour("orange")
		#The other sub panels
		self.EnvironmentInfoBackground = EnvironmentPanelBackground(self.MainPanel,-1)
		self.FlightInfoBackground = FlightStatusPanelBackground(self.MainPanel,-1)
		self.GPS = GPSPanel(self.MainPanel,-1)
		self.PlaneSelectPanelBackground = PlaneSelectPanelBackground(self.MainPanel,-1)
		self.PlaneSelectPanelBackground.updateFlightInfoObject(self.FlightInfoBackground.FlightInfoPanel)

		#add sub panels to the right sizer
		RightVertSizer.Add(self.GPS,2,wx.EXPAND)
		RightVertSizer.Add(self.FlightInfoBackground,1,wx.EXPAND)
		
		LeftVertSizer.Add(self.EnvironmentInfoBackground,2,wx.EXPAND)
		LeftVertSizer.Add(self.PlaneSelectPanelBackground,1,wx.EXPAND)
		
		RightVertSizer.Layout()
		
		#add the left sub panel and right sizer to the main horizontal sizer
		TopHorizSizer.Add(LeftVertSizer,1,wx.EXPAND)
		TopHorizSizer.Add(RightVertSizer,3,wx.EXPAND)
		
		#set the main panel's sizer
		self.MainPanel.SetSizer(TopHorizSizer)

		#initiate timer and timer event
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
		
		self.timer.Start(300)
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
		
		#scriptString = """deleteMarkers()"""
		#self.MainPanel.html_view.RunScript(scriptString)
		for name,playerDict in self.fgObjects.iteritems():
			#print(name)
			lat = ""
			lon = ""
			speed = ""
			for property,value in playerDict.prop_list.iteritems():
				#print("%s: %s"%(property,value))
				if(property == "latitude-deg"):
					lat = value
					#print(lat)
				if(property == "longitude-deg"):
					lon = value
					#print(lon)

				
			currentTime = datetime.now()
			elapsedTime = currentTime - self.fgObjects[name].prop_list['startTime']
			self.fgObjects[name].prop_list['timeElapsed'] = elapsedTime
			#if((self.fgObjects[name].prop_list['pastLat'] != 'none') and (self.fgObjects[name].prop_list['pastLon'] != 'none')):
				#arc = self.distance_on_unit_sphere(float(lat),float(lon),float(self.fgObjects[name].prop_list['pastLat']),float(self.fgObjects[name].prop_list['pastLon']))
				#miles = 3963.1676 * arc
				#print("arc is: %s, miles are: %s,past lat/long: %s,%s  , current lat/lon %s,%s"%(arc,miles,float(self.fgObjects[name].prop_list['pastLat']),float(self.fgObjects[name].prop_list['pastLon']),lat,lon))
			self.fgObjects[name].prop_list['pastLat'] = lat;
			self.fgObjects[name].prop_list['pastLon'] = lon;
			#print(self.fgObjects[name].prop_list['pastLat']+"   "+self.fgObjects[name].prop_list['pastLon'])
			selected = self.fgObjects[name].prop_list['selected']
			scriptString = """updateMarker(%s,%s,"%s","%s")""" % (str(lat),str(lon),str(name),selected)
			self.MainPanel.html_view.RunScript(scriptString)
			self.PlaneSelectPanelBackground.addRadio(name)

			global currentDisplayFlight
			if(name == currentDisplayFlight):
				#print("matched" + name)
				self.fgObjects[name].prop_list['selected'] = "yes"
				self.FlightInfoBackground.FlightInfoPanel.updateText(name,lat,lon,self.fgObjects[name].prop_list['timeElapsed'])
				#self.PlaneSelectPanelBackground.addRadio(name)
			else:
				self.fgObjects[name].prop_list['selected'] = "no"
			
			
		coordinate1 +=1
		coordinate2 +=2
		
		#scriptString = """updateMarkers(new google.maps.LatLng(%s,%s))"""%(str(coordinate1),str(coordinate2))
		#self.MainPanel.html_view.RunScript(scriptString)
		
	#def callJavaScriptFunction(stringCommand):
		#self.MainPanel.html_view.RunScript(stringCommand)
		#print("call this function")

		
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
						#if(playerid == 'Player'):
							#self.PlaneSelectPanelBackground.addRadio(str(playerid))
							#print("done")
						
	def distance_on_unit_sphere(self,lat1, long1, lat2, long2):
		# Convert latitude and longitude to 
		# spherical coordinates in radians.
		degrees_to_radians = math.pi/180.0
			
		# phi = 90 - latitude
		phi1 = (90.0 - lat1)*degrees_to_radians
		phi2 = (90.0 - lat2)*degrees_to_radians
			
		# theta = longitude
		theta1 = long1*degrees_to_radians
		theta2 = long2*degrees_to_radians
			
		# Compute spherical distance from spherical coordinates.
			
		# For two locations in spherical coordinates 
		# (1, theta, phi) and (1, theta, phi)
		# cosine( arc length ) = 
		#    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
		# distance = rho * arc length
		
		cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
			   math.cos(phi1)*math.cos(phi2))
		arc = math.acos( cos )

		# Remember to multiply arc by the radius of the earth 
		# in your favorite set of units to get length.
		return arc
		

class Icon:
    #'''Get/make marker icons at http://mapki.com/index.php?title=Icon_Image_Sets'''
    def __init__(self,id='icon'):
        self.id = id
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
		var planeSymbol;
		var planeSymbolSelected;
		function initialize() {
			center = new google.maps.LatLng(37.6069,-122.381);
			var mapOptions = {zoom: 8,center: center};//,mapTypeId: google.maps.MapTypeId.TERRAIN};
			image = {
				url: 'PlaneImage.png',
				// This marker is 20 pixels wide by 32 pixels tall.
				size: new google.maps.Size(20, 20),
				// The origin for this image is 0,0.
				origin: new google.maps.Point(0,0),
				// The anchor for this image is the base of the flagpole at 0,32.
				anchor: new google.maps.Point(10, 10)
			};
			planeSymbol = {
				path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
				scale: 4,
				strokeWeight: 3,
				strokeColor: 'red'
			};
			
			planeSymbolSelected = {
				path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
				scale: 4,
				strokeWeight: 3,
				strokeColor: 'green'
			}
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
			
			//function createInfoWindowContent(){
			//	return[
			//		'Coordinates:',
			//		'Latitude: ' + marker.getPosition().lat(),
			//		'Longitude: ' + marker.getPosition().lng()
			//	].join('<br>');
			//}
			//infowindow = new google.maps.InfoWindow();
			
			//google.maps.event.addListener(marker, 'click', function() {
			//	infowindow.setContent(createInfoWindowContent());
			//	infowindow.open(map,marker);
			//});
			
			//google.maps.event.addListener(map,'click',function(event) {
			//	addMarker(event.latLng,'click');
			//});
			
			
			//--------------------------------------------------------------------------------
			


			  var lineCoordinates = [
				new google.maps.LatLng(22.291, 153.027),
				new google.maps.LatLng(18.291, 153.027)
			  ];

			  // Define the symbol, using one of the predefined paths ('CIRCLE')
			  // supplied by the Google Maps JavaScript API.
			  var lineSymbol = {
				path: google.maps.SymbolPath.CIRCLE,
				scale: 8,
				strokeColor: '#393',
				stokeOpacity: 1
			  };

			  // Create the polyline and add the symbol to it via the 'icons' property.
			//  line = new google.maps.Polyline({
				//path: lineCoordinates,
				//strokeWeight: 0,
			//	icons: [{
			//	  icon: lineSymbol,
			//	  offset: '100%'
			//	}],
			//	map: map
			//  });

			  //animateCircle();
			
			
			//--------------------------------------------------------------------------------
			


		}
		
		
		function animateCircle() {
		    var count = 0;
			window.setInterval(function() {
			  count = (count + 1) % 15;

			  var icons = line.get('icons');
			  icons[0].offset = (count / .15) + '%';
			  //icons[0].offset = '50%';
			  line.set('icons', icons);
		  }, 20);
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
		

		function addMarker(lat, lon,name) {
			var location = new google.maps.LatLng(lat,lon);
			var marker = new google.maps.Marker({
				position: location,
				map: map,
				icon: planeSymbol,
				title: name,
				optimized: false,
				pastLat: lat,
				pastLon: lon
				//rotation: 180
			});
			//alert(marker.pastLat);
			markers.push(marker);
			//alert("added marker");
		}
		
		function updateMarker(lat, lon,name,selected) {
			var theIndex;
			var found = 0
			if(markers.length == 0) {
				addMarker(lat,lon,name);
			}
			else {
				for(var i= 0;i<markers.length;i++)
				{
					//alert(String(name));
					if(markers[i].title == name)
					{
						//alert("exists");
						
						var newPosition = new google.maps.LatLng(lat,lon);
						if((parseFloat(markers[i].getPosition().lat()) == parseFloat(lat)) && (parseFloat(markers[i].getPosition().lng()) == parseFloat(lon))) {
							//alert("same pos");
						}
						else {

							markers[i].setPosition(newPosition);
							if(selected == 'yes') {
								markers[i].setIcon(planeSymbolSelected);
							}
							else {
								markers[i].setIcon(planeSymbol);
							}
							//alert("else");

							
							var lineCoords = [new google.maps.LatLng(parseFloat(markers[i].pastLat), parseFloat(markers[i].pastLon)),new google.maps.LatLng(parseFloat(lat), parseFloat(lon))];
							var planeLine = new google.maps.Polyline({
								path: lineCoords,
								strokeWeight: 0,
								icons: [{
									icon: marker[i].icon,
									offset: '100%'
								}],
								map: map
							});
							markers[i].pastLat = lat;
							markers[i].pastLon = lon;
							//animateLine(planeLine);
							
							
						}
						//markers[i].setPosition(newPosition);
						found = 1
					}
				  //alert(markers[i].title);
				}
				if(found == 0) {
					addMarker(lat,lon,name);
				}
			}
		}
		
		function animateLine(planeLine) {
			var count = 0;
			window.setInterval(function() {
				//count = (count + 1)%15;
				
				//var icons = planeLine.get('icons');
				//icons[0].offset = (count /.15)+'%';
				//planeLine.set('icons',icons);
				},20);
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