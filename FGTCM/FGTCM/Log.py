import wx

class Log(wx.MiniFrame):
	def __init__(self, parent, id):
		wx.Frame.__init__(self,parent,id,'',size = (300,400), style = wx.DEFAULT_FRAME_STYLE)
		panel=wx.Panel(self)
		panel.SetBackgroundColour('White')
		self.SetTitle("Log")
		self.Bind(wx.EVT_CLOSE,self.closewindow)
		
	def closewindow(self,event):
		self.Destroy()		