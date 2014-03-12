import wx

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
		var symbols = [];
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
			var path = poly.getPath();
			path.push(position);
			marker.setPosition(position);
			map.panTo(position);
		}
		

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
				animation: google.maps.Animation.DROP
			});
			markers.push(marker);
		}
		
		function addSymbol() {
			//var symbol = new planeSymbol;
		}
		
		function updateMarker(lat, lon,name,heading,selected) {
			var theIndex;
			var found = 0
			if(markers.length == 0) {
				addMarker(lat,lon,name);
			}
			else {
				for(var i= 0;i<markers.length;i++)
				{
					if(markers[i].title == name)
					{
						
						var newPosition = new google.maps.LatLng(lat,lon);
						//if((parseFloat(markers[i].getPosition().lat()) == parseFloat(lat)) && (parseFloat(markers[i].getPosition().lng()) == parseFloat(lon))) {
						//	markers[i].icon.rotation = parseFloat(heading);
						//}
						//else {

							if(selected == 'yes') {
								symbol = {
									path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
									scale: 4,
									strokeWeight: 3,
									strokeColor: 'green',
									rotation: heading
								};
								markers[i].setIcon(symbol);
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
							}

							markers[i].setPosition(newPosition);
							//markers[i].setIcon(symbol);
							

							
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
							
							
						//}
						found = 1
					}
				}
				if(found == 0) {
					addMarker(lat,lon,name);
					addSymbol();
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
