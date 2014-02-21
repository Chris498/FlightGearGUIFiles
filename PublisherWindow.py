import wx
import time
import sys
import os
import stomp



class TestFrame(wx.Frame):
	
	def __init__(self, parent, id):
		wx.Frame.__init__(self,parent,id,'Publisher',size = (400,400))
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


		#conn = stomp.Connection(host_and_ports = [(host, port)])
		conn = stomp.Connection(host_and_ports = [("35.9.22.201", port)])
		#conn = stomp.Connection(host_and_ports = [("10.0.1.17", port)])
		conn.start()
		conn.connect(login=user,passcode=password)
		
		textString = self.textBox.GetValue()

		conn.send(body=textString, destination='TEST.FOO')
  

		conn.disconnect()
	
	def closewindow(self,event):
		self.Destroy()
		
if __name__ == '__main__':
	app=wx.PySimpleApp()
	frame = TestFrame(parent = None, id=-1)
	frame.Show()
	app.MainLoop()