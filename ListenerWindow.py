import wx
import time
import sys
import os
import stomp


class TestFrame(wx.Frame):

	def __init__(self, parent, id):
		wx.Frame.__init__(self,parent,id,'Listener',size = (400,400))
		panel=wx.Panel(self)

		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
		self.custom=wx.StaticText(panel,-1,"This is custom", (0,0), (260,-1),wx.ALIGN_CENTER)
		#c = wx.TextCtrl(bkg, style=wx.TE_MULTILINE | wx.HSCROLL)
		self.custom.SetLabel("test text")

		self.timer.Start(100)

	def closewindow(self,event):
		self.Destroy()

	def update(self):
		#self.custom.SetLabel("update")
		#print("updated")
		return

	def OnTimer(self, event):
		self.update()

	def updateText(self, string):
		self.custom.SetLabel(string)



class MyListener(object):
  
  def __init__(self, conn, frame):
    self.conn = conn
    self.count = 0
    self.start = time.time()
    self.frame = frame
  
  def on_error(self, headers, message):
    print('received an error %s' % message)

  def on_message(self, headers, message):
	#custom.SetLabel(message)
	#TestFrame.updateText(message)
    self.frame.updateText(message)

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



if __name__ == '__main__':


	app=wx.PySimpleApp()
	frame = TestFrame(parent = None, id=-1)

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
	conn.subscribe(destination="TEST.FOO2", id=1, ack='auto')
	print("Waiting for messages...")

	frame.Show()
	app.MainLoop()