import wx
import wx.lib.scrolledpanel as scrolled

#This class is in charge of the panel: 'Select a Flight' in FlightTracker. The user may decide what flight is the currently selected flight from here.

class PlaneSelectPanel(wx.Panel):
	def __init__(self,parent,id):
		wx.Panel.__init__(self,parent,id)
		self.SetBackgroundColour("Black")
		self.SetDoubleBuffered(True)
		self.parent = parent
		self.FlightInfoClass = ""
		self.panel = scrolled.ScrolledPanel(self, -1)
		self.panel.SetupScrolling()
		self.panel.SetBackgroundColour("white")
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.boldFont = wx.Font(14,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_ITALIC,wx.FONTWEIGHT_BOLD)

		self.vbox = wx.BoxSizer(wx.VERTICAL)



		main_vbox = wx.BoxSizer(wx.VERTICAL)
		main_vbox.Add(self.vbox,1,wx.EXPAND)

		self.panel.SetSizer(main_vbox)
		self.panel.Layout()
		main_vbox.Fit(self.panel)
		mainSizer.Add(self.panel,1,wx.EXPAND)
		self.SetSizer(mainSizer)
		self.panel.Layout()
		
		self.group1_ctrls = []

		self.Centre()

		
		self.SelectionInfo = wx.StaticText(self.panel, label = "  Select A Flight:")
		self.SelectionInfo.SetFont(self.boldFont)
		self.vbox.Add(self.SelectionInfo)

		self.panel.SetAutoLayout(1)
		self.panel.SendSizeEvent()
		self.GetParent().SendSizeEvent()



		
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
		self.Layout()
	
	def OnGroup1Select( self, event ):
		global currentDisplayFlight
		radio_selected = event.GetEventObject()
		self.parent.GetParent().currentDisplayFlight = radio_selected.GetLabel()
		
	def deleteRadio(self,name):
		if name in self.group1_ctrls: self.group1_ctrls.remove(name)
		buttons = self.vbox.GetChildren()
		
		for button in buttons:
			widget  = button.GetWindow()
			if (widget.GetLabel() == name):
				self.vbox.Remove(widget)
				widget.Destroy()
				
		remainingButtons = self.vbox.GetChildren()
		
		if(self.parent.GetParent().currentDisplayFlight == name):
			for button in remainingButtons:
				widget  = button.GetWindow()
				if(widget.GetName() == 'radioButton'):
					widget.SetValue(1)
					self.parent.GetParent().currentDisplayFlight = widget.GetLabel()
					break

				
		

	def updateFlightInfoObject(self,object):
		self.FlightInfoClass = object
		

