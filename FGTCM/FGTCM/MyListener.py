import wx
import stomp
from datetime import datetime
import time

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