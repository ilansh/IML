'''
Created on Apr 13, 2014
@author: yahav_be
'''

import numpy

class Parties:
    Democrat, Republican = range(2)

Answers = {'Yes' : 1 , 
           'No' : -1 , 
           'Unanswered' : 0 }

class TreeLearner:
    
    def __init__(self):
        pass
    
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
    
#     def load(self):
#         self.trainingSet = self.loadSet('DT/Xtrain','DT/Ytrain')
#         self.testSet = self.loadSet('DT/Xtest', 'DT/Ytest')
        
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

    def probability(self, sampleSet, feature):
        counterDemocrat = 0
#         counterRepublican = 0
        
        for sample in sampleSet:
            if sample[1] == Parties.Democrat:
                counterDemocrat += 1
#             else:
#                 counterRepublican += 1

        probDemocrat = float(counterDemocrat) / len(sampleSet)
        
        return probDemocrat
        
        
        

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
        for answer in Answers.values():
            answerSubset = self.subsetWithVal(answer, sampleSet, feature)
            sumEntropies += (len(answerSubset) / len(sampleSet)) * self.entropy(answerSubset, feature)
        return self.entropy(sampleSet, feature) - sumEntropies
        #return self.C(self.conditionalProbability(domain, Parties.Republican, None, None)) - (self.probability(domain, False, Answers.No, index)*self.C(self.conditionalProbability(domain, labelValue, givenFeatureValue, index)))
        
    def subsetWithVal(self, value, sampleSet, feature):
        resultSet = set()
        for sample in sampleSet:
            if sample[0][feature] == value:
                resultSet.add(sample)
        return resultSet 

     
    def entropy(self, sampleSet, feature):
        a = self.probability(sampleSet, feature)
        return -a * numpy.log(a) - (1 - a) * numpy.log(1 - a)
            
    
    #def maxGainFeature(self, domain, features):
        #gains = []  
        # for index in features:
            
    def maxGainFeature(self, sampleSet, featureSet):
        maxGain = self.gain(sampleSet, next(iter(featureSet)))
        i = 0
        maxGainIndex = 0
        for feature in featureSet:
            curGain = self.gain(sampleSet, feature)
            if curGain > maxGain:
                maxGain = curGain
                maxGainIndex = i
            i += 1
        return maxGainIndex
            
        
        
    
    def allSameFeatureValue(self, sampleSet, index):
        first = next(iter(sampleSet))[0][index] #feature value in location index of some sample
        for sample in sampleSet:
            if (sample[0][index] != first):
                return False
        return True
    
#     def splitSamplesByFeature(self, sampleSet, index, value):
#         result = set()
#         for sample in sampleSet:
#             if sample[0][index] == value:
#                 result.add(sample)
#         return result
              
        
    def ID3(self, sampleSet, featureSet):
        if self.allIs(Parties.Republican, sampleSet):
            return Tree(True, Parties.Republican)
        if self.allIs(Parties.Democrat, sampleSet):
            return Tree(True, Parties.Democrat)
        if not featureSet:
            return Tree(True, self.majority(sampleSet))
        else:
            index = self.maxGainFeature(sampleSet, featureSet)
#             index = min(featureSet)
            if self.allSameFeatureValue(sampleSet, index):
                return Tree(True, self.majority(sampleSet))
            else:
                t = Tree(False, index)
                t.left = self.ID3(self.subsetWithVal(Answers['No'], sampleSet, index), featureSet - set([index]))
                t.middle = self.ID3(self.subsetWithVal(Answers['Unanswered'], sampleSet, index), featureSet - set([index]))
                t.right = self.ID3(self.subsetWithVal(Answers['Yes'], sampleSet, index), featureSet - set([index]))
                return t
        
        
class Tree:
    
    def __init__(self, isLeaf, val):
        self.isLeaf = isLeaf
    
    

def main():
    t = TreeLearner()
    trainingSet = t.loadSet('DT/Xtrain','DT/Ytrain')
    testSet = t.loadSet('DT/Xtest', 'DT/Ytest')
    featureSet = set(range(16))
#     print featureSet
    t.ID3(trainingSet, featureSet)
    
if __name__ == "__main__":
    main()