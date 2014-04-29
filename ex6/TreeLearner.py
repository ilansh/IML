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
        self.trainingSet = self.loadSet('DT/Xtrain','DT/Ytrain')
        self.testSet = self.loadSet('DT/Xtest', 'DT/Ytest')
        
    def allIs(self, value, sampleSet):
        for sample in sampleSet:
            if sample[1] != value:
                return False
        return True
    
    def majority(self, sampleSet):
        zeros, ones = 0, 0
        for sample in sampleSet:
            if(sample[1] == Parties.Democrat):
                zeros += 1
            else:
                ones += 1
        return Parties.Republican if ones > zeros else Parties.Democrat

#     def probability(self, sampleSet, isLabel, value, index):
#         counter = 0.0
#         if isLabel:
#             for sample in sampleSet:
#                 if sample[1] == value:
#                     counter += 1
#         else:
#             for sample in sampleSet:
#                 if sample[0][index] == value:
#                     counter += 1
#         return counter / len(sampleSet)

    def probability(self, sampleSet):
        counterNo = 0
        counterYes = 0
        
        for sample in sampleSet:
            if sample[1] == Answers.No:
                counterNo += 1
            elif sample[1] == Answers.Yes:
                counterYes += 1

        probNo = counterNo / len(sampleSet)
        probYes = counterYes / len(sampleSet)
        probUnAnswered = 1 - probNo - probYes
        
        return probNo, probYes, probUnAnswered
        
        
        

#     def conditionalProbability(self, domain, labelValue, givenFeatureValue, index):
#         relevantSet = self.splitDomainByFeature(domain, index, givenFeatureValue)
#         counter = 0.0
#         for item in relevantSet:
#             if item[1] == labelValue:
#                 counter += 1   
#         return counter / len(relevantSet)
#         
#             
        
    

    def gain(self, sampleSet, feature):
        sumEntropies = 0
        #calculate sum entropies 
        for answer in Answers:
            answerSubset = self.subsetWithVal(answer, sampleSet)
            sumEntropies += len(answerSubset) / len(sampleSet) * self.entropy(answerSubset)
        return self.entropy(sampleSet) - sumEntropies
        #return self.C(self.conditionalProbability(domain, Parties.Republican, None, None)) - (self.probability(domain, False, Answers.No, index)*self.C(self.conditionalProbability(domain, labelValue, givenFeatureValue, index)))
        
    def subsetWithVal(self, value, sampleSet):
        resultSet = set()
        for sample in sampleSet:
            if sample[1] == value:
                resultSet.add(sample)
        return resultSet 

     
    def entropy(self, sampleSet):
        a, b, c = self.probablity(sampleSet)
        return -a * numpy.log(a) - b * numpy.log(b) - c * numpy.log(c)
            
    
    #def maxGainFeature(self, domain, features):
        #gains = []  
        # for index in features:
            
    def maxGainFeature(self, sampleSet, featureSet):
        maxGain = self.gain(sampleSet, next(iter(featureSet)))
        for feature in featureSet:
            curGain = self.gain(feature)
            if curGain > maxGain:
                maxGain = curGain
        return maxGain
            
        
        
    
    def allSameFeatureValue(self, sampleSet, index):
        first = next(iter(sampleSet))[0][index] #feature value in location index of some sample
        for sample in sampleSet:
            if (sample[0][index] != first):
                return False
        return True
    
    def splitSamplesByFeature(self, sampleSet, index, value):
        result = set()
        for sample in sampleSet:
            if sample[0][index] == value:
                result.add(sample)
        return result
              
        
    def ID3(self, sampleSet, featureSet):
        if self.allIs(Parties.Republican, sampleSet):
            return Tree(True, Parties.Republican)
        if self.allIs(Parties.Democrat, sampleSet):
            return Tree(True, Parties.Democrat)
        if not featureSet:
            return Tree(True, self.majority(sampleSet))
        else:
            index = numpy.min(featureSet)
            if self.allSamefeatureValue(sampleSet, index):
                return Tree(True, self.majority(sampleSet))
            else:
                t = Tree(False, index)
                t.left = self.ID3(self.splitSamplesByFeature(sampleSet, index, Answers.No), featureSet - index)
                t.middle = self.ID3(self.splitSamplesByFeature(sampleSet, index, Answers.Unanswered), featureSet - index)
                t.right = self.ID3(self.splitSamplesByFeature(sampleSet, index, Answers.Yes), featureSet - index)
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