'''
parse will accept a string of the form

'Player,latitude-deg 37.6136,langitude-deg -122.357,altitude 3.99158\nJAL_777,latitude-deg 37.9206,longitude-deg -122.549\nUS-NAVY\nlatitude-deg 37.6783\nlongitude-deg -122.124\n\nklock\nlatitude-deg 37.619\nlongitude-deg -122.375\n
\nBAW2346\nlatitude-deg 37.6136\nlongitude-deg -122.387\n\nPA-DE\nlatitude-deg 38.3643\nlongitude-deg -123.413\n
:
\nLuke_13\nlatitude-deg 37.6187\nlongitude-deg -122.397\n\nEND'

and return 

'''
import re
import string

def parse(string):
    
    RecordsList = re.split("\n+",string)
    #print("length of list is: %s"% len(playerRecordsList))
    PropDictList = []
    
    
    for prop in RecordsList:
        print("received prop: %s"%prop)
        props = re.split(",",prop)
        
        propDict = {}
        for pair in props:
            kv = re.split(" ",pair)
            if len(kv) == 2:
                propDict[kv[0]] = kv[1]
                #print("%s   %s"%(kv[0],kv[1]))
            elif(len(kv) == 1 and kv[0] == "Environment"):
                propDict[kv[0]] = 'Information'
            elif(kv[0] == 'weather-scenario'):
                weatherScenario = ''
                counter = 0
                for item in kv:
					if(counter>0):
						weatherScenario+=str(item)
						weatherScenario+=' '
					counter+=1
                propDict[kv[0]] = weatherScenario
                #print(weatherScenario)
				
            else:
                #print("%s <----BAD"%(kv[0]))
                continue
			
        PropDictList.append(propDict)
                #print('key value 1: %s, key value 2: %s\n'% (kv[0],kv[1]))
    return PropDictList