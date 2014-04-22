from datetime import datetime
import math

#This class displays a log for a certain flight. Information displayed includes items such as past flights, position information, and time stamps

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
    def updateLog(self,props):
		if('endtime' in self.prop_list):
			old_prop_list = self.prop_list
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
			seconds = int(math.floor(elapsedTime.seconds))
			if(seconds >= 59):
				self.prop_list['lastLoggedTime'] = currentTime
				self.prop_list['lat'].append(props['latitude-deg'])
				self.prop_list['lon'].append(props['longitude-deg'])
				self.prop_list['times'].append(currentTime)
			if(props['updated'] == False):
				endTime = datetime.now()
				self.prop_list['endtime'] = endTime
