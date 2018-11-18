from dateutil.parser import parse
import datetime
import os


from numpy import median



sector_name_remap={'SECTOR financial':'financial sector','SECTOR candidate':'political candidates','SECTOR property_man':'property management companies','SECTOR small donors':'small donors (< $150)','SECTOR developer':'property developers','SECTOR realestate':'real estate companies','SECTOR local individual ':'People in their ward','SECTOR pac':'PACs','SECTOR construction':'construction companies','SECTOR retail':'retail businesses','SECTOR unclassified local business':'Other business in their ward','SECTOR nonlocal individual ':'people from outside their ward','SECTOR union':'labor unions','SECTOR unclassified nonlocal business':'Other businesses outside their ward','SECTOR party':'Political parties'}

LAST_ELECTION=datetime.datetime(2015,2,24)
INTERESTING_THRESHOLD=0.85
import numpy as np
import numpy.linalg as la



#stuff for sector classification
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
from random import *


def preprocess(datain): #preprocess data to be fed into the classifier
    output=""
    allowed="abcdefghijklmnopqrstuvwxyz ,"
    datain=datain.lower()
    for item in datain:
        if item in allowed:
            output=output+item
        if item in "1234567890":
            output=output+"num "
    return output


def cleandonor(datain): #like preprocess but allows numbers
    output=""
    allowed="abcdefghijklmnopqrstuvwxyz ,1234567890"
    datain=datain.lower()
    for item in datain:
        if item in allowed:
            output=output+item
    return output
def trainClassifier():    
    allset=[]
    #categories=['financial','liquor', 'signs', 'transport', 'developer', 'candidate', 'entertainment', 'union', 'pac', 'property_man', 'party', 'business', 'hotel', 'construction', 'law', 'grocery', 'restaurant', 'car', 'industry', 'tech', 'retail', 'realestate']
    categories=['financial','developer', 'candidate', 'union', 'pac', 'property_man', 'party', 'construction', 'retail', 'realestate']

    for cat in categories:
        thiscat=[]
        print("Category:"+cat)
        inFile=open("donorclass3.csv",'r')
        for line in inFile.readlines():
            if cat in line.split(",")[1]: #is this a category match?
                line=preprocess(line)
                thiscat.append(line)
        inFile.close()
        itemsAdded=0

        while itemsAdded < 50:
            for item in thiscat:
                temp=(item.split(",")[0],item.split(",")[1])
                allset.append(temp)
                itemsAdded=itemsAdded+1
    cl = NaiveBayesClassifier(allset)
    print("Classifier training complete")
    return cl

def doClassify(text,classifier):
    MIN_CONFIDENCE=0.5 #if the bayesian system can't give at least this much confidence we will treat it as unclassified
    text=preprocess(text)
    result=(cl.prob_classify(text.lower().replace(",","").replace(".","")))
    called=(cl.classify(text.lower().replace(",","").replace(".","")))
    if (result.prob(called) < MIN_CONFIDENCE):
        return "unclassified"
    else:
        return called

def striptonum(datain):
    allowed="sle1234567890"
    dataout=""
    for item in datain:
        if item in allowed:
            dataout=dataout+item
    return dataout
def getComForPerson(person,comList):
    for line in comList:
        if person in line:
            return line.replace("\n","").replace("\r","").split(",")[1:] #if the name matches, return associated comittees

def getNotItemized(com): #get not itemized contributions (donations and transfers in) for a committee
    com=striptonum(com)
    try:
        comFile=open(com+".htm")
        data=comFile.read()
        comFile.close()
        donationsNI=float(data[data.find('''<span id="ctl00_ContentPlaceHolder1_lblIndivContribNI" class="BaseText">$''')+73:].split("</span>")[0].replace(",","")) #parse not itemized donations from file
        transferNI=float(data[data.find('''<span id="ctl00_ContentPlaceHolder1_lblXferInNI" class="BaseText">$''')+67:].split("</span>")[0].replace(",","")) #parse not itemized donations from file
        return donationsNI+transferNI
    except Exception:
        print("Couldn't open nonitemized file for "+com, ", not itemized donations will all be 0")
        return 0
    
    
def updateList(listIn, amount, entity):#returns a dictionary containing total funds for each donor, with the new donor information added
    if entity not in listIn: #if the donor does not exist, create it, otherwise add the amount to the existing record
        listIn[entity]=float(amount)
    else:
        listIn[entity]=listIn[entity]+float(amount)
    return listIn

def getDistance(targetVec,targetTotal,searchVec,searchTotal):
    distance=0
    for itemid in range(0,len(targetVec)):
        distance=distance+abs((float(targetVec[itemid])/float(targetTotal))-(float(searchVec[itemid])/float(searchTotal)))
    return distance

def simpleSimilaritySearch():
    1+1

def getSimilarPeople(alderData,donorList,allPeople, names): #find aldermen with similar donation patterns to the target
    targetVec=[]
    targetTotal=0.00000000000001
    distances=[]
    for donor in donorList:
        if donor in alderData:
            targetTotal=targetTotal+alderData[donor]
            targetVec.append(alderData[donor])
        else:
            targetVec.append(0)
    for pData in allPeople:
        searchVec=[]
        searchTotal=0.0000000000001
        for donor in donorList:
            if donor in pData:
                searchTotal=searchTotal+pData[donor]
                searchVec.append(pData[donor])
            else:
                searchVec.append(0)
        result=getDistance(targetVec,targetTotal,searchVec,searchTotal)
        distances.append(result)
        #print(str(result))


    distout=[]
    nameout=[]
    for item in np.argsort(distances):
        nameout.append(names[item])
        distout.append(distances[item])

    return [nameout, distout]

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


def getStats(inList,cl): #compute metrics for a list of donations. Cl is the bayesian classifier object
    
    totalValue=0.0000000000001
    medianValue=0.0000000000001
    totalN=0
    individualN=0
    smallN=0
    individualMoney=0.0000000000001
    smallMoney=0.0000000000001 # less than 175
    bigMoney=0.0000000000001 #more than 500
    inChicagoValue=0.0000000000001
    inWardValue=0.0000000000001
    inWardN=0

    
    values=[]
    donorList={}
    
    for donation in inList:
        #print(donation)
        dsplit=donation.split(",")
        #print(str(len(dsplit)))
        amount=float(dsplit[7])
        ward=int(dsplit[31])
        inHomeWard=int(dsplit[32])
        if (ward > -1 or "ch" in dsplit[14].lower() ): #resolvable ward means it's in chicago, the second check lets us see if an address was given in chicago but it couldn't be resolved to a ward.
            inChicagoValue=inChicagoValue+amount
            if inHomeWard > -1:
                inWardValue=inWardValue+amount
                inWardN=inWardN+1
        totalN=totalN+1
        totalValue=totalValue+amount
        if (amount <= 175):
            smallN=smallN+1
            smallMoney=smallMoney+amount
        if (amount > 500):
            bigMoney=bigMoney+amount
            
        if len(dsplit[5]) > 2: #the entity has a first name, this is a good sign that it's a person
            individualN=individualN+1
            individualMoney=individualMoney+amount
            donorList=updateList(donorList,amount,"PERSON:"+cleandonor(dsplit[4] +" "+dsplit[5])) #update the person's donor list
            if (inHomeWard > -1):
                donorList=updateList(donorList, amount,"SECTOR local individual ") #write the sector result to the donor list
            else:
                 donorList=updateList(donorList, amount,"SECTOR nonlocal individual ") #write the sector result to the donor list
        else: #this is a business, let's classify the sector
            bname=dsplit[4]
            result=doClassify(bname,cl)
            if "unclass" in result: #the classifier didn't know what kind of business this is, but we can still figure out if local!
                if inHomeWard > -1:
                    result="unclassified local business"
                else:
                    result="unclassified nonlocal business"
            donorList=updateList(donorList, amount,"SECTOR "+cleandonor(result)) #write the sector result to the donor list
            donorList=updateList(donorList,amount,cleandonor(dsplit[4])) #update the business name to the list too
        values.append(amount) #for median calculation

    return [totalValue,median(values),float(individualMoney)/float(totalValue),float(smallMoney),float(individualN)/float(totalN), donorList, float(inChicagoValue)/float(totalValue), float(inWardValue)/float(totalValue),inWardN,bigMoney]

def getPercentile(value,dist):
    isBigger=0
    for item in dist:
        if value < item:
            isBigger=isBigger+1
    return 1.0-(float(isBigger)/float(len(dist)))

def summarizeStatistics(value, dist): #Generate a string summarizing statistical information
    DESCRIPTION_THRESHOLD=3 #needs to be in the top 3 or bottom 3 to use a rank description as opposed to percent
    isBigger=0
    for item in dist:
        if value < item:
            isBigger=isBigger+1
    #if (isBigger == 0):
    if (value == max(dist)):
        description=" the highest of any alderman"
    elif (value==min(dist)):
        description=" the lowest of any alderman"
    else:
        sortedDist=sorted(dist) #initial thought was to copy the array. However, because of something with python memory management we end up changing the original array which is bad
        higherThan=0 #the value is higher than this many
        lowerThan=0
        for item in range(0,len(sortedDist)):
            if sortedDist[item]==value: #go through the sorted array, when we reach this value we know we've already found all the ones that are lower
                higherThan=higherThan+1
                break
            else:
                higherThan=higherThan+1
        for item in range(len(sortedDist)-1,0,-1):
            if sortedDist[item]==value: #go through the sorted array, when we reach this value we know we've already found all the ones that are lower
                lowerThan=lowerThan+1
                break
            else:
                lowerThan=lowerThan+1
        print(str(higherThan))
        print(str(lowerThan))
        if (lowerThan >= 47):
            description=" less than all but "+str(50-lowerThan)+" aldermen"
        elif (higherThan >= 47):
            description=" more than all but "+str(50-higherThan)+" aldermen"
        else:
            percentile=(1.0-(float(isBigger)/float(len(dist))))*100
            print(str(percentile))
            if (percentile > 50):
                description=" more than "+str(percentile)+" percent of aldermen"
            else:
                description=" less than "+str(100-percentile)+" percent of aldermen"
    return description


unfilt=os.listdir(os.getcwd())
allFiles=[]
for item in unfilt:
    if "_donations.csv" in item and "~" not in item:
        allFiles.append(item)

def processDonors(donorList, allDonors, person,value,aldernames):
    AMOUNT_CUTOFF=1000
    PERSON_AMOUNT_CUTOFF=10000
    INTERESTING_THRESHOLD=0.85
    SINGLE_THRESHOLD=0.2
    MASSIVE_THRESHOLD=100000
    myDonors=donorList[person]
    myValue=value[person]
    sectorList=""
    interestingList=""
    simList=""
    feoEligible=0
    #scan through my donor list and see if any of the donations are under the FEO limit
    for donor in myDonors:
        if myDonors[donor] < 175: #this is FEO eligible, mark it
            feoEligible=feoEligible+myDonors[donor]

##    #similarity check
##    similarity=[]
##    for thing in donorList:
##        simscore=0
##        for donor in allDonors:
##            if donor in thing.keys():
##                if donor in myDonors.keys():
##                    simscore=simscore+1
##            else:
##                if donor not in myDonors.keys():
##                    simscores=simscore+1
##        similarity.append(simscore)
##    
##    sortedNames=[x for _,x in sorted(zip(similarity,aldernames))]
##    similarity.sort()
##    similarity.reverse()
##    sortedNames.reverse()
##    for item in range(0,5):
##        simList=simList+(sortedNames[item]+":"+str(similarity[item]))+"\n"
    for donor in allDonors:
        if donor in myDonors.keys(): #check if this person is present
            donorVals=[]
            relDonorVals=[] #relative
            donatedCount=0
            similarities=[]
            for item in range(0,len(donorList)):
                td=donorList[item]
                if donor in td.keys():
                    donorVals.append(td[donor])
                    donatedCount=donatedCount+1
                    relDonorVals.append(float(td[donor]) / float(value[item]))
                else:
                    donorVals.append(0)
                    relDonorVals.append(0)
            absolutepercentile=(getPercentile(myDonors[donor],donorVals))
            relativepercentile=(getPercentile(float(myDonors[donor])/float(myValue),relDonorVals))
            if ("SECTOR" in donor):
                if  (relativepercentile > INTERESTING_THRESHOLD or relativepercentile < 1-INTERESTING_THRESHOLD):
                    interestingList=interestingList+str(round((float(myDonors[donor]))/float(myValue)*100))+"% of their total funding($"+str(myDonors[donor])+") comes from "+sector_name_remap[donor]+", "+summarizeStatistics(float(myDonors[donor])/float(myValue),relDonorVals)+"\n"
    return "INTERESTING DONATIONS\nRanks and percentiles refer to the percentage of their funding, not absolute dollar amount.\n"+interestingList+"\nOTHER INTERESTING THINGS\n"

#set up distribution variables--these are lists that will hold a value of the attribute for each alderman so we can figure out percentiles
totalValue=[] #value of all donations
totalValueSLE=[] #value of donations since last election
medianValue=[] #median value of a donation
medianValueSLE=[]
percentIndividualDonors=[] #what % of money came from individual donors
percentIndividualDonorsSLE=[]
percentSmallDonations=[] #what percent of the total # of donations were less than $200
percentSmallDonationsSLE=[]
percentBigDonationsSLE=[]

nDonors=[] #raw number of individual donors
nDonorsSLE=[]


percentInWard=[] #percentage of money coming from inside ward
percentInWardSLE=[]
nInWard=[] #number of donors in ward
nInWardSLE=[]
percentInChicago=[] #percent of money coming form inside Chicago
percentInChicagoSLE=[] 

percentItemized=[] #percent of money from itemized donations
valueNotItemized=[] #total unitemized money

percentSmallDonations=[]
percentBigDonations=[]
percentItemizedSLE=[] 
valueNotItemizedSLE=[]

aldernames=[] #names of each alderman, go go in the same order as the statistics
dataList=[]
SLEList=[]

dlSLE=[] #donation lists, for finding interesting donors
allDonorsSLE=[]
dl=[]
allDonors=[]

print("Training classifier...")
cl=trainClassifier()
print "Loading data..."
alderFile=open('aldermen.csv','r') #read in the alderman/committee mapping
alderData=alderFile.readlines()
alderFile.close()

for fileName in allFiles: #go through the files, and load those that are download donation files

    print(fileName)
    if "_donations.csv" in fileName and "~" not in fileName:
        #first, figure out the candidate committees and process the files containing non-itemized contributions.
        committees=getComForPerson(fileName.replace("_donations.csv","").replace("_"," "),alderData) #look up committee numbers associated
        totalNotItemized=0
        totalNotItemizedSLE=0
        for com in committees: #iterated through each comittee and update total not itemized funds
            totalNotItemized=totalNotItemized+getNotItemized(com)
            totalNotItemizedSLE=totalNotItemizedSLE+getNotItemized("sle"+com)

        dataFile=open(fileName)
        dataLines=dataFile.readlines()
        dataFile.close()
        allDonations=[] #we will split the donation list into two groups and process them seperately with the same function
        donationsSLE=[]
        for donation in dataLines:
            donation=fixCSV(donation) #clean up commas in quoted txt which will interfere with the split
            if "last_name" not in donation and len(donation) >3:
                allDonations.append(donation)
                dsplit=donation.split(",")
                if parse(dsplit[6]) >= LAST_ELECTION: #donation ocurred after last election
                    donationsSLE.append(donation)
    
        SLEData=getStats(donationsSLE,cl)
        SLEList.append(SLEData)
        totalValueSLE.append(SLEData[0]+totalNotItemizedSLE)
        medianValueSLE.append(SLEData[1])
        percentIndividualDonorsSLE.append(SLEData[2])
        percentSmallDonationsSLE.append((SLEData[3]+totalNotItemizedSLE)/(SLEData[0]+totalNotItemizedSLE)) #small donations as a portion of total
        percentBigDonationsSLE.append(SLEData[9]/(SLEData[0]+totalNotItemizedSLE))
        nDonorsSLE.append(SLEData[4])
        dlSLE.append(SLEData[5])
        percentInChicagoSLE.append(SLEData[6])
        percentInWardSLE.append(SLEData[7])
        nInWardSLE.append(SLEData[8])

        valueNotItemizedSLE.append(totalNotItemizedSLE)
        percentItemizedSLE.append(float(SLEData[0])/float(SLEData[0]+totalNotItemizedSLE))

        
        for donor in SLEData[5].keys():
            if donor not in allDonorsSLE:
                allDonorsSLE.append(donor)
        fulldata=getStats(allDonations,cl)
        dataList.append(fulldata)
        totalValue.append(fulldata[0]+totalNotItemized) #include itemized and not-itemeized donations in calculating total value
        medianValue.append(fulldata[1])
        percentIndividualDonors.append(fulldata[2])
        nDonors.append(fulldata[4])
        dl.append(fulldata[5])
        percentInChicago.append(fulldata[6])
        percentInWard.append(fulldata[7])
        nInWard.append(fulldata[8])
        valueNotItemized.append(totalNotItemized)
        percentSmallDonations.append((float(fulldata[3])+float(totalNotItemized))/(float(fulldata[0])+float(totalNotItemized))) #small donations as a portion of total
        percentBigDonations.append(float(fulldata[9])/(float(fulldata[0])+float(totalNotItemized)))
        print(fileName)
        print(str(float(fulldata[3])))
        print(str((float(fulldata[3])+float(totalNotItemized))/(float(fulldata[0])+float(totalNotItemized))))
        percentItemized.append(float(fulldata[0])/float(fulldata[0]+totalNotItemized))

        donorlist=fulldata[5]
        donorlist['SECTOR small donors']=totalNotItemized
        for donor in donorlist.keys():
            if donor not in allDonors:
                allDonors.append(donor)
            
                
        aldernames.append(fileName.replace("_donations.csv",""))
print("Data loaded, analyzing aldermen...")
facts=[""]*50
output=open("results simple.csv",'w')
output.write("ALL TIME TOTAL\n")
descriptions="Person,Total donations, total raw, median donation, median raw, percent itemized, percent itemized raw, total not itemized, total not itemized raw, percent individual donors, percent individual donors raw, percent from ward, percent from ward raw, percent from chicago, percent from chicago raw\n"
splitdesc=descriptions.split(",")
output.write(descriptions)
for personID in range(0,len(aldernames)):
    print("Computing stats:"+aldernames[personID])
    temp=(aldernames[personID]+","+str(getPercentile(totalValue[personID],totalValue))+","+str(totalValue[personID])+","+str(getPercentile(medianValue[personID],medianValue))+","+str(medianValue[personID])+","+str(getPercentile(percentItemized[personID],percentItemized))+","+str(percentItemized[personID])+","+str(getPercentile(valueNotItemized[personID],valueNotItemized))+","+str(valueNotItemized[personID])+","+str(getPercentile(percentIndividualDonors[personID],percentIndividualDonors))+","+str(percentIndividualDonors[personID])+","+str(getPercentile(percentInWard[personID],percentInWard))+","+str(percentInWard[personID])+","+str(getPercentile(percentInChicago[personID],percentInChicago))+","+str(percentInChicago[personID]))
    output.write(temp)
    output.write("\n")
    #now this has been written, highlight any spots that are unusual in the report
    splitdata=temp.split(",")
    for item in range(1,len(temp.split(","))-1):
        if "raw" not in splitdesc[item]: #use only the percentile values to detect irregularities, the raw value for each percentile is its index plus one
            if float(splitdata[item]) > INTERESTING_THRESHOLD or float(splitdata[item]) < 1-INTERESTING_THRESHOLD:
                facts[personID]=facts[personID]+"Alderman is in the "+str(float(splitdata[item])*100)+"th percentile for "+splitdesc[item]+ " with a value of "+splitdata[item+1]+"\n"
output.write("\n\nSINCE LAST ELECTION\n")
descriptions="Person,Total donations SLE, total raw SLE, median donation SLE, median raw SLE,percent itemized, percent itemized raw, total not itemized, total not itemized raw, percent individual donors SLE, percent individual donors raw SLE, percent from ward SLE, percent from ward raw SLE, percent from chicago SLE, percent from chicago raw SLE, Donations \n"
splitdesc=descriptions.split(",")
output.write(descriptions)
for personID in range(0,len(aldernames)):
    print("Real 1 "+str(percentSmallDonations[personID]))    
for personID in range(0,len(aldernames)):
    print("Getting donor info:"+aldernames[personID])

    donorResult=processDonors(dl,allDonors, personID, totalValue, aldernames)
    facts[personID]=donorResult
##
##    temp=(aldernames[personID]+","+str(getPercentile(totalValueSLE[personID],totalValueSLE))+","+str(totalValueSLE[personID])+","+str(getPercentile(medianValueSLE[personID],medianValueSLE))+","+str(medianValueSLE[personID])+","+str(getPercentile(percentItemizedSLE[personID],percentItemizedSLE))+","+str(percentItemizedSLE[personID])+","+str(getPercentile(valueNotItemizedSLE[personID],valueNotItemizedSLE))+","+str(valueNotItemizedSLE[personID])+","+str(getPercentile(percentIndividualDonorsSLE[personID],percentIndividualDonorsSLE))+","+str(percentIndividualDonorsSLE[personID])+","+str(getPercentile(percentInWardSLE[personID],percentInWardSLE))+","+str(percentInWardSLE[personID])+","+str(getPercentile(percentInChicagoSLE[personID],percentInChicagoSLE))+","+str(percentInChicagoSLE[personID]))
##    output.write(temp)
##    output.write("\n")
##    #now this has been written, highlight any spots that are unusual in the report, using the same slot that we used when writing the unusual features in the original report
##    splitdata=temp.split(",")
##    for item in range(1,len(temp.split(","))-1):
##        if "raw" not in splitdesc[item]: #use only the percentile values to detect irregularities, the raw value for each percentile is its index plus one
##            if float(splitdata[item]) > INTERESTING_THRESHOLD or float(splitdata[item]) < 1-INTERESTING_THRESHOLD:
##                facts[personID]=facts[personID]+"Alderman is in the "+str(float(splitdata[item])*100)+"th percentile for "+splitdesc[item]+ " with a value of "+splitdata[item+1]+"\n"

    facts[personID]=facts[personID]+"Median donation value is "+str((medianValue[personID]))+", "+summarizeStatistics(medianValue[personID],medianValue)+"\n"
    facts[personID]=facts[personID]+str(round(percentBigDonations[personID]*100))+"% of their money comes from donations over $500, "+summarizeStatistics(percentBigDonations[personID],percentBigDonations)+"\n"
    facts[personID]=facts[personID]+str(round(percentSmallDonations[personID]*100))+"% of their money comes from donations over of $175 or lower, "+summarizeStatistics(percentSmallDonations[personID],percentSmallDonations)+"\n"
    
   
output.flush()
output.close()
for personID in range(0,len(aldernames)):
    print("Real 1 "+str(percentSmallDonations[personID])) 

for personID in range(0,len(aldernames)):
    factFile=open(aldernames[personID]+" report highlights.txt",'w')
    factFile.write(facts[personID])
    factFile.flush()
    factFile.close()
    

print("Done")
        
