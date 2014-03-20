from datetime import datetime

class FGObject():
    def __init__(self, id, props):
        self.id = id
        self.prop_list = props
        startTime = datetime.now()
        self.prop_list['startTime'] = startTime
        self.prop_list['selected'] = "no"
        self.prop_list['updated'] = True
    def updateFromMessage(self,list):
        for item in list:
            self.prop_list[item] = list[item]
        self.prop_list['updated'] = True
        self.prop_list['pastLat'] = 'none'
        self.prop_list['pastLon'] = 'none'
        return
