from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob


class donation_classifier:
    MIN_CONFIDENCE=0.5 #if the bayesian system can't give at least this much confidence we will treat it as unclassified

    def preprocess(self,datain): #preprocess data to be fed into the classifier
        output=""
        allowed="abcdefghijklmnopqrstuvwxyz ,"
        datain=datain.lower()
        for item in datain:
            if item in allowed:
                output=output+item
            if item in "1234567890":
                output=output+"num "
        return output


    def trainClassifier(self):    
        allset=[]
        #categories=['financial','liquor', 'signs', 'transport', 'developer', 'candidate', 'entertainment', 'union', 'pac', 'property_man', 'party', 'business', 'hotel', 'construction', 'law', 'grocery', 'restaurant', 'car', 'industry', 'tech', 'retail', 'realestate']
        categories=['financial','developer', 'candidate', 'union', 'pac', 'property_man', 'party', 'construction', 'retail', 'realestate']

        for cat in categories:
            thiscat=[]
            print("Category:"+cat)
            inFile=open("donorclass3.csv",'r')
            for line in inFile.readlines():
                if cat in line.split(",")[1]: #is this a category match?
                    line=self.preprocess(line)
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

    def bayesClassify(text,classifier):
        text=preprocess(text)
        result=(cl.prob_classify(text.lower().replace(",","").replace(".","")))
        called=(cl.classify(text.lower().replace(",","").replace(".","")))
        if (result.prob(called) < MIN_CONFIDENCE):
            return "unclassified"
        else:
            return called

    def classify(self, donations):
        
        

        
    def __init__(self):
        self.trainClassifier()

classy=donation_classifier()
