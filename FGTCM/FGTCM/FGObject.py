
class FGObject():

	def __init__(self, id, props):
	    self.id = id
	    self.prop_list = props

	def updateFromMessage(self,list):
	    for item in list:
	        self.prop_list[item] = list[item]
	    return
