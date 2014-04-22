import wx

#This class houses the javascript that will be embedded in the html code that is used in the GPS map panel in FlightTracker.

class PyMap:
    def GoogleMapPy(self):
		""" Returns complete javacript for rendering map """
        
		self.js = """<script src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false"></script>
		<script>
		var map;
		var center;
		var poly;
		var infowindow;
		var image;
		var markers = [];
		var symbols = [];
		var planeSymbol;
		var planeSymbolSelected;
		var CircleOptions;
		var FlightZone;
		var chicago = new google.maps.LatLng(41.850033, -87.6500523);
		
		
		// Handles the button for 'center on selected'
		function HomeControl(controlDiv, map) {
		
		controlDiv.style.padding = '6px';

		// Set CSS for the control border
		var controlUI = document.createElement('div');
		controlUI.style.backgroundColor = 'white';
		controlUI.style.borderStyle = 'solid';
		controlUI.style.borderWidth = '1px';
		controlUI.style.cursor = 'pointer';
		controlUI.style.textAlign = 'center';
		controlUI.title = 'Click to set the map to Home';
		controlDiv.appendChild(controlUI);

		// Set CSS for the control interior
		var controlText = document.createElement('div');
		controlText.style.fontFamily = 'Arial,sans-serif';
		controlText.style.fontSize = '12px';
		controlText.style.paddingLeft = '4px';
		controlText.style.paddingRight = '4px';
		controlText.innerHTML = '<b>Center On Selected</b>';
		controlUI.appendChild(controlText);


		google.maps.event.addDomListener(controlUI, 'click', function() {
			for (var i = 0; i < markers.length; i++) {
				if(markers[i].selected == true)
				{
					map.setCenter(markers[i].getPosition());
				}
			}
		});

		}
		
		//Button that displays the 100 Nautical Mile Flight Zone radius.
		function RadiusControl(controlDiv, map)  {
		
		controlDiv.style.padding = '6px';

		// Set CSS for the control border
		var controlUI = document.createElement('div');
		controlUI.style.backgroundColor = 'white';
		controlUI.style.borderStyle = 'solid';
		controlUI.style.borderWidth = '1px';
		controlUI.style.cursor = 'pointer';
		controlUI.style.textAlign = 'center';
		controlUI.title = 'Click to set the map to Home';
		controlDiv.appendChild(controlUI);

		// Set CSS for the control interior
		var controlText = document.createElement('div');
		controlText.style.fontFamily = 'Arial,sans-serif';
		controlText.style.fontSize = '12px';
		controlText.style.paddingLeft = '4px';
		controlText.style.paddingRight = '4px';
		controlText.innerHTML = '<b>Toggle Flight Zone</b>';
		controlUI.appendChild(controlText);


		google.maps.event.addDomListener(controlUI, 'click', function() {
			for (var i = 0; i < markers.length; i++) {
				if(markers[i].title == "Player")
				{
					if(FlightZone.getVisible() == false) {
						FlightZone.setVisible(true);
					}
					else {
						FlightZone.setVisible(false);
					}
				}
			}
		});
		}
		
		//initialize the map
		function initialize() {
			center = new google.maps.LatLng(37.6069,-122.381);
			var mapOptions = {zoom: 8,center: center};
			image = {
				url: 'PlaneImage.png',
				size: new google.maps.Size(20, 20),
				origin: new google.maps.Point(0,0),
				anchor: new google.maps.Point(10, 10)
			};
			
			//setup symbols
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
			
			//add 'center on selected' and 'show radius' buttons
			var homeControlDiv = document.createElement('div');
			var homeControl = new HomeControl(homeControlDiv, map);

			homeControlDiv.index = 1;
			map.controls[google.maps.ControlPosition.TOP_RIGHT].push(homeControlDiv);
			
			//Radius Control
			var radiusControlDiv = document.createElement('div');
			var radiusControl = new RadiusControl(radiusControlDiv, map);
			
			radiusControlDiv.index =1;
			map.controls[google.maps.ControlPosition.TOP_RIGHT].push(radiusControlDiv);
			
			//Flight Zone Radius information
			CircleOptions = {
			 strokeColor: '#FF0000',
			 strokeOpacity: 0.8,
			 strokeWeight: 2,
			 fillColor: '#FF0000',
			 fillOpacity: 0.25,
			 map: map,
			 center: center,
			 radius: 185200,
			 visible: false
			};
			
			FlightZone = new google.maps.Circle(CircleOptions);
			


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

		//Move flight marker
		function moveMarker(position, map, marker) {
			var path = poly.getPath();
			path.push(position);
			marker.setPosition(position);
			map.panTo(position);
		}
		
		//add flight marker
		function addMarker(lat, lon,name) {
			var location = new google.maps.LatLng(lat,lon);
			symbol = {
				path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
				scale: 4,
				strokeWeight: 3,
				strokeColor: 'red',
				rotation: 0
			};
			var marker = new google.maps.Marker({
				position: location,
				map: map,
				icon: symbol,
				title: name,
				optimized: false,
				pastLat: lat,
				pastLon: lon,
				animation: google.maps.Animation.DROP,
				selected: false
			});
			markers.push(marker);
		}
		
		//remove a flight marker
		function removeMarker(name) {
				for (var i = 0; i < markers.length; i++) {
					if(markers[i].title == name) {
						markers[i].setMap(null);
						markers.splice(i,1);
					}
			}
		}
		
		//update the flight marker
		function updateMarker(lat, lon,name,heading,selected) {
			var theIndex;
			var found = 0
			//add new flight marker
			if(markers.length == 0) {
				addMarker(lat,lon,name);
			}
			else {
				//update existing flight marker
				for(var i= 0;i<markers.length;i++)
				{
					if(markers[i].title == name)
					{
						//center Flight Zone radius over the user's flight.
						if(name == "Player") {
							FlightZone.setCenter(markers[i].position);
						}
						var newPosition = new google.maps.LatLng(lat,lon);
							//change the flight marker colors based on currently selected flight
							if(selected == 'yes') {
								symbol = {
									path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
									scale: 4,
									strokeWeight: 3,
									strokeColor: 'green',
									rotation: heading
								};
								markers[i].setIcon(symbol);
								markers[i].selected = true;
							}
							else {
								symbol = {
									path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
									scale: 4,
									strokeWeight: 3,
									strokeColor: 'red',
									rotation: heading
								};
								markers[i].setIcon(symbol);
								markers[i].selected = false;
							}

							markers[i].setPosition(newPosition);
							

							
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
							
							
						found = 1
					}
				}
				if(found == 0) {
					addMarker(lat,lon,name);
				}
			}
		}
		
		function animateLine(planeLine) {
			var count = 0;
			window.setInterval(function() {
				
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
