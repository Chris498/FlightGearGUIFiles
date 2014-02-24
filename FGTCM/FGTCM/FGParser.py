'''
parse will accept a string of the form

'Player\nlatitude-deg 37.6136\nlangitude-deg -122.357\naltitude 3.99158\n\nJAL_777\nlatitude-deg 37.9206\nlongitude-deg -122.549\n
\nUS-NAVY\nlatitude-deg 37.6783\nlongitude-deg -122.124\n\nklock\nlatitude-deg 37.619\nlongitude-deg -122.375\n
\nBAW2346\nlatitude-deg 37.6136\nlongitude-deg -122.387\n\nPA-DE\nlatitude-deg 38.3643\nlongitude-deg -123.413\n
:
\nLuke_13\nlatitude-deg 37.6187\nlongitude-deg -122.397\n\nEND'

and return 

'''
import re

def parse(string):
    
    playerRecordsList = re.split("\n+",string)
    playerPropDictList = []
    
    
    for prop in playerRecordsList:
        props = re.split(",",prop)
        
        propDict = {}
        for pair in props:
            kv = re.split(" ",pair)
            if len(kv) == 2:
                propDict[kv[0]] = kv[1]
                playerPropDictList.append(propDict)
    return playerPropDictList