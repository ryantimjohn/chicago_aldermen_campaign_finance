from threading import Thread
import threading
import time
totalToDo=0
totalDone=0
def fixCSV(dataIn): #this removes commas in quoted text that would otherwise mess up the alignment of the CSV
    dataOut=""
    quoted=False
    for item in dataIn:
        if "," in item:
            if not quoted:
                dataOut=dataOut+","
        else:
            dataOut=dataOut+item
        if '"' in item:
            quoted=not quoted
    return dataOut


def geoLookup(address): #get a ward number for an address in chciago, or return -1 for an invalid address or error.
    #print(address)
    payload='''{ForwardGeocodeServiceInput3:{"systemId":"WARD_LOOKUP","offsetFt":"20","fullAddress":"'''+address+'''", "getGeos":{"geographyName":"WARD"}}}'''
    keepRunning=True
    while keepRunning:
        try:
            test=requests.post("https://gisapps.cityofchicago.org/ElsProxy/fwdGeocode3",payload)
            keepRunning=False
        except Exception:
            print("Network error, retrying")
            time.sleep(1)
    if "geographyValue" in test.text:
        result=test.text[test.text.find('"geographyValue":')+17:]
        try:
            return int(result.split("}")[0].replace('"',''))
        except EnvironmentError:
            return -1
    else: #lookup failure
        return -1

def downloadPerson(splitup):
    global totalToDo
    global totalDone
    donationData=""
    donationBuffer=""
    print("Downloading "+splitup[0])
    for committee in splitup[1:]: #some people have more than 1 supporting comittee
        keepTrying=True
        while keepTrying:
            try:
                donationData=requests.get("https://illinoissunshine.org/api/receipts/?committee_id="+committee+"&limit=10000&datatype=csv")
                keepTrying=False
            except requests.exceptions.RequestException: #some sort of network problem happened, so retry
                print("Network or server error, trying again...")
        donationBuffer=donationBuffer+donationData.text.encode('ascii',errors='ignore')
    #print("Finding geographical sources of donations...")
    outFile=open(splitup[0].replace(" ","_")+"_donations.csv",'w')
    numDone=0
    stuff=donationBuffer.split("\n")
    totalToDo=totalToDo+len(stuff)
    
    for item in stuff:
        splitup=fixCSV(item).split(",") #fix issues with commas inside quited text
        try:
            if len(splitup) > 3:
                if "ch" not in splitup[14].lower(): #city of address is not chicago, say invalid ward
                    ward=-1
                    inWard=-1
                else:
                    ward=geoLookup(splitup[12])
                    if (ward == -1):
                        inWard=-1
                    else:
                        if thisWard == ward:
                            inWard=1
                        else:
                            inWard=0
                outBuffer=fixCSV(item).replace("\n","").replace("\r","")+","+str(ward)+","+str(inWard)+"\n"
                outFile.write(outBuffer)
            totalDone=totalDone+1
        except Exception:
            print("Error parsing donation for "+str(splitup))
        #time.sleep(1)
    
    outFile.flush()
    outFile.close()

import requests #use the requests library to make http requests simpler
print("This will update the donations and expenditures data with new data from Illinois Sunshine. Press enter to continue")
raw_input()
alderFile=open("aldermen.csv",'r')
alder=alderFile.readlines()
alderFile.close()
thisPerson=1
thisWard=1
for person in alder:
    splitup=person.split(",")
    print("Downloading "+str(thisPerson)+"/" +str(len(alder)))
    t=Thread(target=downloadPerson,args=(splitup,))
    t.start()
while (True): #Each download runs in its own thread, this lets us know when they're all done.
    print(str(threading.active_count()-1) +" downloads in progress")
    time.sleep(5)
        
