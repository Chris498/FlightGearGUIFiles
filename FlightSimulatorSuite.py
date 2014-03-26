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
from FGEnvironmentObject import FGEnvironmentObject
import FGParser
from EnvironmentPanel import EnvironmentPanel
from PlaneSelectPanel import PlaneSelectPanel
from GPSPanel import GPSPanel
from FlightPanel import FlightPanel
from MyListener import MyListener
from PyMap import PyMap
from Log import Log
from FGLog import FGLog
from ConnectionDialog import ConnectionDialog



EXIT = wx.NewId()
LOG = wx.NewId()
CONNECTION = wx.NewId()

class FlightSimulatorSuite(wx.Frame):
	def __init__(self, parent, id,):  
		
		
		super(FlightSimulatorSuite, self).__init__(parent, size=(1024,700), style = wx.DEFAULT_FRAME_STYLE)#^wx.RESIZE_BORDER)
		self.currentDisplayFlight = "Player"
		
		self.menubar = wx.MenuBar()
		self.fileMenu = wx.Menu()
		self.optionsMenu = wx.Menu()
		self.connectionMenu = wx.Menu()
		
		
		self.fileMenu.Append(EXIT, 'Exit', 'Exit')
		self.connectionMenu.Append(CONNECTION,'Edit Connection','Edit Connection')
		
		self.menubar.Append(self.fileMenu,'File')
		self.menubar.Append(self.optionsMenu,'Logs')
		self.menubar.Append(self.connectionMenu,'Connection')
		
		self.SetMenuBar(self.menubar)
		
		self.Bind(wx.EVT_MENU, self.ExitProgram, id=EXIT)
		self.Bind(wx.EVT_MENU, self.EditConnection, id=CONNECTION)
		#self.Bind(wx.EVT_MENU, self.Log, id=LOG)
		
		#The top most sizer that splits the screen horizontally
		TopHorizSizer = wx.BoxSizer(wx.HORIZONTAL)
		
		#The rest of the sizers
		self.RightVertSizer = wx.BoxSizer(wx.VERTICAL)
		LeftVertSizer = wx.BoxSizer(wx.VERTICAL)
		GPSSizer = wx.BoxSizer()
		
		#The main panel all others will be parented to
		self.MainPanel = wx.Panel(self)
		self.MainPanel.SetBackgroundColour("black")
		#The other sub panels
		self.EnvironmentInfo = EnvironmentPanel(self.MainPanel,-1)
		self.FlightInfo = FlightPanel(self.MainPanel,-1)
		self.GPS = GPSPanel(self.MainPanel,-1)
		self.PlaneSelectPanel = PlaneSelectPanel(self.MainPanel,-1)
		self.PlaneSelectPanel.updateFlightInfoObject(self.FlightInfo)

		#add sub panels to the right sizer
		self.RightVertSizer.Add(self.GPS,2,wx.EXPAND|wx.ALL,5)
		self.RightVertSizer.Add(self.FlightInfo,1,wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT,5)#|wx.ALL,5)
		
		LeftVertSizer.Add(self.EnvironmentInfo,2,wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM,5)#|wx.ALL,5)
		LeftVertSizer.Add(self.PlaneSelectPanel,1,wx.EXPAND|wx.BOTTOM|wx.LEFT,5)#|wx.ALL,5)
		

		
		#add the left sub panel and right sizer to the main horizontal sizer
		TopHorizSizer.Add(LeftVertSizer,1,wx.EXPAND)
		TopHorizSizer.Add(self.RightVertSizer,3,wx.EXPAND)
		
		#set the main panel's sizer
		self.MainPanel.SetSizer(TopHorizSizer)
		self.MainPanel.Fit()
		
		self.CenterOnScreen()
		self.CreateStatusBar()
		self.SetStatusText("Boeing - 2014")


		#initiate timer and timer event
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
		
		self.timer.Start(300)
		
		self.fgObjects = {}
		self.fgEnvironmentObject = {}
		self.fgLogObjects = {}
	
	#called on every timer event, updates the main panel
	def OnTimer(self, event):
		self.updateLogs()
		self.updateTheView()
		
	def updateLogs(self):
		for name,playerDict in self.fgObjects.items():
			if(name in self.fgLogObjects):
				#update
				#print("update: %s log"% name)
				self.fgLogObjects[name].updateLog(self.fgObjects[name].prop_list)
			else:
				#add
				#print("add to logs: %s" % name)
				newLog = FGLog(name, self.fgObjects[name].prop_list)
				self.fgLogObjects[name] = newLog
				
				#add new menubar item
				newID = wx.NewId()
				
				
				item = wx.MenuItem(self.optionsMenu, newID, name)
				self.optionsMenu.AppendItem(item)
				
				
				self.Bind(wx.EVT_MENU, self.Log, id=newID)

	#updates main panel which will update all sub panels
	def updateTheView(self):
		
		#self.EnvironmentInfo.Update()
		#self.FlightInfo.Update()
		

		for name,playerDict in self.fgObjects.items():
			if(self.fgObjects[name].prop_list['updated'] == False):
				#Remove marker from map
				scriptString = """removeMarker("%s")""" %(str(name))
				self.MainPanel.html_view.RunScript(scriptString)
				print("remove: %s"%name)
				
				#Remove player from fgObjects
				del self.fgObjects[name]
				
				self.PlaneSelectPanel.deleteRadio(name)
				
				#remove radio
				#remove from self.fgObjects
			else:
				lat = ""
				lon = ""
				speed = ""
				alt = ""
				heading = ""
				currentFuel = ""
				fuelCapacity = ""
				localTime = ""
				for property,value in playerDict.prop_list.iteritems():
					if(property == "latitude-deg"):
						lat = value
					elif(property == "longitude-deg"):
						lon = value
					elif(property == "airspeed-kt"):
						speed = value
					elif(property == "altitude"):
						alt = value
					elif(property == "heading-deg"):
						heading = value
					elif(property == "total-fuel-gals"):
						currentFuel = value
					elif(property == "total-fuel-capacity"):
						fuelCapacity = value 
					
					#print("property: %s, value: %s"%(property,value))

					
				currentTime = datetime.now()
				elapsedTime = currentTime - self.fgObjects[name].prop_list['startTime']
				self.fgObjects[name].prop_list['timeElapsed'] = elapsedTime
				self.fgObjects[name].prop_list['pastLat'] = lat;
				self.fgObjects[name].prop_list['pastLon'] = lon;
				selected = self.fgObjects[name].prop_list['selected']
				scriptString = """updateMarker(%s,%s,"%s",%s,"%s")""" % (str(lat),str(lon),str(name),str(heading),selected)
				self.MainPanel.html_view.RunScript(scriptString)
				self.PlaneSelectPanel.addRadio(name)

				if(name == self.currentDisplayFlight):
					self.fgObjects[name].prop_list['selected'] = "yes"
					self.FlightInfo.updateText(name,lat,lon,speed,heading,alt,currentFuel,fuelCapacity,self.fgObjects[name].prop_list['timeElapsed'])
				else:
					self.fgObjects[name].prop_list['selected'] = "no"
			
			
		
		stationID = ""
		skyConditions = ""
		temperature = ""
		windSpeed = ""
		windDirection = ""
		pressure = ""
		for property,value in self.fgEnvironmentObject.iteritems():
			if(property == "station-id"):
				stationID = value
			elif(property == "temperature-degf"):
				temperature = value
			elif(property == "wind-from-heading-deg"):
				windDirection = value
			elif(property == "wind-speed-kt"):
				windSpeed = value
			elif(property == "pressure"):
				pressure = value
		#print(stationID)
		print(pressure)
		self.EnvironmentInfo.UpdateText(stationID,temperature,windSpeed,windDirection,pressure)

		
	def updateFGObjs(self, string):
		if string is not None:
			fgDictsList = FGParser.parse(string)
			if len(fgDictsList) == 0:
				return
			for player,dict in self.fgObjects.iteritems():
				self.fgObjects[player].prop_list['updated'] = False;
				
			for dict in fgDictsList:
				if "playername" in dict:
					playerid = dict["playername"]
					if playerid in self.fgObjects:
						self.fgObjects[playerid].updateFromMessage(dict)
					else:
						newPlayer = FGObject(playerid, dict)
						self.fgObjects[playerid] = newPlayer

				elif "Environment" in dict:
					self.fgEnvironmentObject = dict
					

	
	
	def Log(self,e):
		item = self.GetMenuBar().FindItemById(e.GetId())
		name = item.GetText()
		#name = e.GetEventObject().GetName()
		#print("selected menu item: %s"%name)
		log = Log(parent = frame,player = name,logObject =self.fgLogObjects[name], id = -1)
		log.Show()
	def ExitProgram(self,e):
		self.Destroy()
	def EditConnection(self,e):
		dlg = ConnectionDialog(self,-1, "Edit Connection", size=(300,300),style = wx.DEFAULT_DIALOG_STYLE,)
		dlg.CenterOnScreen()
		
		val = dlg.ShowModal()
		
		if val == wx.ID_OK:
			#print(dlg.text.GetValue())
			try:
				float(dlg.text.GetValue())
				print(dlg.text.GetValue())
				user = os.getenv("ACTIVEMQ_USER") or "admin"
				password = os.getenv("ACTIVEMQ_PASSWORD") or "password"
				host = os.getenv("ACTIVEMQ_HOST") or "localhost"
				port = os.getenv("ACTIVEMQ_PORT") or 61613
				conn = stomp.Connection(host_and_ports = [(host, port)])
				conn.start()
				conn.connect(login=user,passcode=password)
				
				conn.send(body = dlg.text.GetValue(),destination='MESSAGE_INTERVAL')
				conn.disconnect()
				
			except ValueError:
				print("not a number")
		else:
			print("You pressed Cancel\n")

		dlg.Destroy()

		
if __name__ == '__main__':

	g = PyMap()                         
	open('test.htm','wb').write(g.showhtml())   # generate test file
	

	
	app=wx.PySimpleApp()
	frame = FlightSimulatorSuite(parent = None, id=-1)
	frame.SetTitle("Flight Simulator Suite")
	
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