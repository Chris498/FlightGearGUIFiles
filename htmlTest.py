import wx
import wx.html2

data = '''<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <style type="text/css">
      html { height: 100% }
      body { height: 100%; margin: 0; padding: 0 }
      #map-canvas { height: 100% }
    </style>
    <script type="text/javascript"
      src="https://maps.googleapis.com/maps/api/js?sensor=false">
    </script>
    <script type="text/javascript">
      function initialize() {
        var mapOptions = {
          center: new google.maps.LatLng(-34.397, 150.644),
          zoom: 8,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        var map = new google.maps.Map(document.getElementById("map-canvas"),
            mapOptions);
      }
      google.maps.event.addDomListener(window, 'load', initialize);
    </script>
  </head>
  <body>
    <div id="map-canvas"/>
  </body>
</html>
'''

class AppFrame(wx.Frame):
    def __init__(self, parent):        
        super(AppFrame, self).__init__(parent, size=(350,365), style = wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)
        self.html_view = wx.html2.WebView.New(self)
        #sizer = wx.BoxSizer(wx.VERTICAL)
        #sizer.Add(self.html_view, 1, wx.EXPAND)
        #self.SetSizer(sizer)

if __name__ == '__main__':
    app = wx.App()

    frame = AppFrame(None)
    #Example 1: Works fine! ============================================
    #frame.html_view.SetPage("<html><body>Hello World</body></html>", "")
    #Example 2: Works fine! ============================================
    frame.html_view.LoadURL('file://C:/Users/TeamBoeing/Desktop/PytonActiveMQ/test.htm')
    #Example 3: Doesn't work!!! ========================================
    #frame.html_view.SetPage(data, 'http://maps.google.com/maps/api')

    frame.Show()
    app.MainLoop()
