from datetime import datetime
import math

class FGLog():
    def __init__(self, id, props):
        self.id = id
        startTime = datetime.now()
        self.prop_list = {}
        self.prop_list['startTime'] = startTime
        self.prop_list['lastLoggedTime'] = startTime
        self.prop_list['lat'] = []
        self.prop_list['lon'] = []
        self.prop_list['times'] = []
        self.prop_list['pastFlights'] = []
        self.prop_list['name'] = props['playername']
        self.prop_list['lat'].append(props['latitude-deg'])
        self.prop_list['lon'].append(props['longitude-deg'])
        self.prop_list['times'].append(startTime)
        #self.prop_list = props
    def updateLog(self,props):
		if('endtime' in self.prop_list):
			print("need to redo the log for player: %s" %self.prop_list['name'])
			old_prop_list = self.prop_list
			#self.prop_list['pastFlights'].append(self.prop_list)
			startTime = datetime.now()
			self.prop_list = {}
			self.prop_list['pastFlights'] = old_prop_list['pastFlights']
			self.prop_list['pastFlights'].append(old_prop_list)
			self.prop_list['startTime'] = startTime
			self.prop_list['lastLoggedTime'] = startTime
			self.prop_list['lat'] = []
			self.prop_list['lon'] = []
			self.prop_list['times'] = []
			self.prop_list['name'] = props['playername']
			self.prop_list['lat'].append(props['latitude-deg'])
			self.prop_list['lon'].append(props['longitude-deg'])
			self.prop_list['times'].append(startTime)
		else:
			currentTime = datetime.now()
			elapsedTime = currentTime - self.prop_list['lastLoggedTime']
			#print(elapsedTime)
			seconds = int(math.floor(elapsedTime.seconds))
			#print(seconds)
			if(seconds >= 59):
				#print("update the log positions")
				self.prop_list['lastLoggedTime'] = currentTime
				self.prop_list['lat'].append(props['latitude-deg'])
				self.prop_list['lon'].append(props['longitude-deg'])
				self.prop_list['times'].append(currentTime)
			if(props['updated'] == False):
				endTime = datetime.now()
				self.prop_list['endtime'] = endTime
