import re
import string

#This class is in charge of 'parsing' the message strings received from the ActiveMQ broker sent from FlightGear.

def parse(string):
    
    RecordsList = re.split("\n+",string)
    PropDictList = []
    
    
    for prop in RecordsList:
        props = re.split(",",prop)
        
        propDict = {}
        for pair in props:
            kv = re.split(" ",pair)
            if len(kv) == 2:
                propDict[kv[0]] = kv[1]
            elif(len(kv) == 1 and kv[0] == "Environment"):
                propDict[kv[0]] = 'Information'
            else:
                continue
			
        PropDictList.append(propDict)
    return PropDictList