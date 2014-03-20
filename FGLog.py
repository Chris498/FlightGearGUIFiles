from datetime import datetime

class FGLog():
    def __init__(self, id, props):
        self.id = id
        startTime = datetime.now()
        self.prop_list = {}
        self.prop_list['startTime'] = startTime
        self.prop_list['lat'] = []
        self.prop_list['lon'] = []
        self.prop_list['name'] = props['playername']
        self.prop_list['lat'].append(props['latitude-deg'])
        self.prop_list['lon'].append(props['longitude-deg'])
        #self.prop_list = props
    def updateLog(self,props):
        self.prop_list['lat'].append(props['latitude-deg'])
        self.prop_list['lon'].append(props['longitude-deg'])
        if(props['updated'] == False):
        	endTime = datetime.now()
        	self.prop_list['endtime'] = endTime
        return
