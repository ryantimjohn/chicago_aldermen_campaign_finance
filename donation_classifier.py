from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob


MIN_CONFIDENCE=0.5 #if the bayesian system can't give at least this much confidence we will treat it as unclassified

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


def add_class(donations):
    classes=[]
    for index in range(0,donations.shape[0]):
        row=donations.iloc[index]
        if len(str(row.first_name)) > 3:
            donation_type="Individual"
        else: #fall back on the bayesian classifier
            donation_type=bayesClassify(preprocess(row.last_name))
        classes.append(donation_type)
    donations['classified_type']=classes
    return donations
        
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
        while itemsAdded < 50: #For balancing categories; we'll eventualy find a different way to do this
            for item in thiscat:
                temp=(item.split(",")[0],item.split(",")[1])
                allset.append(temp)
                itemsAdded=itemsAdded+1
    cl = NaiveBayesClassifier(allset)
    print("Classifier training complete")
    return cl

def bayesClassify(text):
    text=preprocess(text)
    result=(cl.prob_classify(text.lower().replace(",","").replace(".","")))
    called=(cl.classify(text.lower().replace(",","").replace(".","")))
    if (result.prob(called) < MIN_CONFIDENCE):
        return "unclassified"
    else:
        return called
    
cl=trainClassifier()

