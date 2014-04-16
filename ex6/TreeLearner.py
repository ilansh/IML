'''
Created on Apr 13, 2014
@author: yahav_be
'''

import numpy

class Parties:
    Democrat, Republican = range(2)

class Answers:
    Yes, No, Unanswered = 1, -1, 0

class TreeLearner:
    
    def __init__(self):
        self.trainingSet = {}
        self.testLabels = {}
    
    def loadSet(self, domainFileName, labelsFileName):
        fDomain = open(domainFileName, 'r')
        fLabels = open(labelsFileName, 'r')
        domain = []
        result = set()
        for line in fDomain:
            domain.append(map(int, line.split()))
        for i, line in enumerate(fLabels):
            result.add((tuple(domain[i]), int(line)))
        print result    
        return result
    
    def load(self):
        self.trainingSet = self.loadSet('Xtrain','Ytrain')
        self.testSet = self.loadSet('Xtest', 'Ytest')
        
    def allIs(self, valueSet, value):
        for item in valueSet:
            if item != value:
                return False
        return True
    
    def majority(self, domain):
        zeros, ones = 0, 0
        for item in domain:
            if(item[1] == 0):
                zeros += 1
            else:
                ones += 1
        return Parties.Republican if ones > zeros else Parties.Democrat

    def probability(self, domain, isLabel, value, index):
        counter = 0.0
        if isLabel:
            for item in domain:
                if item[1] == value:
                    counter += 1
        else:
            for item in domain:
                if item[0][index] == value:
                    counter += 1
        return counter / len(domain)
        
        

    def conditionalProbability(self, domain, labelValue, givenFeatureValue, index):
        relevantSet = self.splitDomainByFeature(domain, index, givenFeatureValue)
        counter = 0.0
        for item in relevantSet:
            if item[1] == labelValue:
                counter += 1   
        return counter / len(relevantSet)
        
            
        
    

    #def gain(self, index):
        #return self.C(self.conditionalProbability(domain, Parties.Republican, None, None)) - (self.probability(domain, False, Answers.No, index)*self.C(self.conditionalProbability(domain, labelValue, givenFeatureValue, index)))
        
        

     
    def C(self, a):
        return -a*numpy.log(a)-(1-a)*numpy.log(1-a)
            
    
    #def maxGainFeature(self, domain, features):
        #gains = []
        
       # for index in features:
            
        
        
        
    
    def allSameFeatureValue(self, domain, index):
        temp = None
        for item in domain:
            cur = item[0][index]
            if (temp != None & temp != cur):
                return False
        return True
    
    def splitDomainByFeature(self, domain, index, value):
        result = set()
        for item in domain:
            if item[0][index] == value:
                result.add(item)
        return result
              
        
    def ID3(self, domain, features):
        if self.allIs(domain, Parties.Republican):
            return Tree(True, Parties.Republican)
        if self.allIs(domain, Parties.Democrat):
            return Tree(True, Parties.Democrat)
        if not features:
            return Tree(True, self.majority(domain))
        else:
            index = numpy.min(features)
            if self.allSamefeatureValue(domain, index):
                return Tree(True, self.majority(domain))
            else:
                t= Tree(False, index)
                t.left = self.ID3(self.splitDomainByFeature(domain, index, Answers.No), features - index)
                t.middle = self.ID3(self.splitDomainByFeature(domain, index, Answers.Unanswered), features - index)
                t.right = self.ID3(self.splitDomainByFeature(domain, index, Answers.Yes), features - index)
                return t   
        
        
class Tree:
    
    def __init__(self, isLeaf, val):
        self.isLeaf = isLeaf
    
    

def main():
    t = TreeLearner()
    t.load()
    
#     t.ID3()
    
if __name__ == "__main__":
    main()