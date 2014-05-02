'''
Created on Apr 13, 2014
@author: yahav_be
'''

import numpy
import random
import matplotlib.pyplot as plt
from graphviz import Digraph

Parties = {
    'Democrat' : 0,
    'Republican' : 1 }

Answers = {'Yes' : 1 , 
           'No' : -1 , 
           'Unanswered' : 0 }

dot = Digraph(comment = 'Decision Tree')
nodeCount = 0

class TreeLearner:
    
    def __init__(self):
        pass
   
# Loads data from file
    def loadSet(self, domainFileName, labelsFileName):
        counter = 0
        fDomain = open(domainFileName, 'r')
        fLabels = open(labelsFileName, 'r')
        domain = []
        result = set()
        for line in fDomain:
            domain.append(map(int, line.split()))
        for i, line in enumerate(fLabels):
            result.add((tuple(domain[i]), int(line), counter))
            counter += 1
        return result
    
# Checks if all the examples in the given set has the same label
    def allIs(self, value, sampleSet):
        for sample in sampleSet:
            if sample[1] != value:
                return False
        return True

# Returns the label value of the majority of the given sample set    
    def majority(self, sampleSet):
        zeros, ones = 0, 0
        for sample in sampleSet:
            if(sample[1] == Parties['Democrat']):
                zeros += 1
            else:
                ones += 1
        return Parties['Republican'] if ones > zeros else Parties['Democrat']

# checks the probability of a democrat senator amongst the given set
    def probability(self, sampleSet):
        counterDemocrat = 0
        
        for sample in sampleSet:
            if sample[1] == Parties['Democrat']:
                counterDemocrat += 1

        probDemocrat = float(counterDemocrat) / len(sampleSet)
        
        return probDemocrat          
        
    

    def gain(self, sampleSet, feature):
        sumEntropies = 0.0
        #calculate sum entropies 
        for answer in Answers.values():
            answerSubset = self.subsetWithVal(answer, sampleSet, feature)
            sumEntropies += (float(len(answerSubset)) / len(sampleSet)) * self.entropy(answerSubset, feature)
        return self.entropy(sampleSet, feature) - sumEntropies
        
     
    def entropy(self, sampleSet, feature):
        if not sampleSet:
            return 0
        a = self.probability(sampleSet)
        if a == 0 or a == 1:
            return 0
        return -a * numpy.log(a) - (1 - a) * numpy.log(1 - a)
            

    def maxGainFeature(self, sampleSet, featureSet):
        maxGain = self.gain(sampleSet, next(iter(featureSet)))
        maxGainIndex = 0
        for feature in featureSet:
            curGain = self.gain(sampleSet, feature)
            if curGain > maxGain:
                maxGain = curGain
                maxGainIndex = feature
        return maxGainIndex

# Returns a subset of the given sample set according to the provided feature and value
    def subsetWithVal(self, value, sampleSet, feature):
        resultSet = set()
        for sample in sampleSet:
            if sample[0][feature] == value:
                resultSet.add(sample)
        return resultSet     
    
# Returns true/false based on the values of the given feature
    def allSameFeatureValue(self, sampleSet, index):
        first = next(iter(sampleSet))[0][index]
        for sample in sampleSet:
            if (sample[0][index] != first):
                return False
        return True

# The ID3 algorithm. "fathername" is used for graph visualization
    def ID3(self, sampleSet, featureSet, fatherName, isRandomForests, D):
        if self.allIs(Parties['Republican'], sampleSet):
            return Tree(True, Parties['Republican'], fatherName)
        if self.allIs(Parties['Democrat'], sampleSet):
            return Tree(True, Parties['Democrat'], fatherName)
        if not featureSet:
            return Tree(True, self.majority(sampleSet), fatherName)
        else:
            if isRandomForests:
                tempSet = set(random.sample(range(15), D)) & featureSet
                if not tempSet:
                    return Tree(True, self.majority(sampleSet), fatherName)
                index = self.maxGainFeature(sampleSet, tempSet)
            else:
                index = self.maxGainFeature(sampleSet, featureSet)
            #index = min(featureSet)
            if self.allSameFeatureValue(sampleSet, index):
                return Tree(True, self.majority(sampleSet), fatherName)
            else:
                t = Tree(False, index, fatherName)
                t.left = self.ID3(self.subsetWithVal(Answers['No'], sampleSet, index), featureSet - set([index]),t.getName(), isRandomForests, D)
                t.middle = self.ID3(self.subsetWithVal(Answers['Unanswered'], sampleSet, index), featureSet - set([index]),t.getName(), isRandomForests, D)
                t.right = self.ID3(self.subsetWithVal(Answers['Yes'], sampleSet, index), featureSet - set([index]),t.getName(), isRandomForests, D)
                return t
            
    def getPrediction(self, sample, tree): 
        curNode = tree 
        while not curNode.isLeaf:
            if sample[0][curNode.val] == Answers['No']:
                curNode = curNode.left
            elif sample[0][curNode.val] == Answers['Unanswered']:
                curNode = curNode.middle
            else:
                curNode = curNode.right
        return curNode.val
          
    def testError(self, root, testSet):
        errorNum = 0
        for sample in testSet:
            if self.getPrediction(sample, root) != sample[1]:
                errorNum += 1
        return float(errorNum) / len(testSet)
        
    def randomForest(self, sampleSet, featureSet, D, numTrees):
        forest = []
        for i in range(numTrees):
            baggedSet = self.bagging(sampleSet)
            forest.append(self.ID3(baggedSet, featureSet, '0', True, D))
        return forest
            

    def bagging(self, sampleSet):
        counter = 0
        resultSet = set()
        
        for i in range(len(sampleSet)):
            x = random.sample(sampleSet, 1)
            resultSet.add((x[0][0], x[0][1], counter))
            counter += 1
        return resultSet 

    def testErrorForest(self, forest, testSet):
        errorCount = 0
        for sample in testSet:
            demCount = 0
            repCount = 0
            for tree in forest:
                p = self.getPrediction(sample, tree)
                if p == Parties["Democrat"]:
                    demCount += 1
                else:
                    repCount += 1
            finalPred = Parties["Democrat"] if demCount > repCount else Parties["Republican"]
            if finalPred != sample[1]:
                errorCount += 1
        return float(errorCount) / len(testSet)
   
   
# For forming the decision tree    
class Tree:
    
    def __init__(self, isLeaf, val, fatherName):
        global nodeCount
        nodeCount += 1
        self.name = str(nodeCount)
        self.val = val
        #print self.name
        if isLeaf:
            if val == 0:
                dot.node(self.name, 'Democrat')
            else:
                dot.node(self.name, 'Republican')
        else:
            dot.node(self.name, str(val))
        if fatherName != '0':
            dot.edge(fatherName, str(nodeCount))
        self.isLeaf = isLeaf
        
    def getName(self):
        return self.name
    
    

def main():
    t = TreeLearner()
    trainingSet = t.loadSet('DT/Xtrain','DT/Ytrain')
    testSet = t.loadSet('DT/Xtest', 'DT/Ytest')
    featureSet = set(range(16))
    dTree = t.ID3(trainingSet, featureSet, '0', False, 0)
    print t.testError(dTree, testSet)
    dot.render('DecisionTree.gv', view=True)
    
    testErrors = []
    for i in range(15):
        forest = t.randomForest(trainingSet, featureSet, 4, i+1)
        testErrors.append(t.testErrorForest(forest, testSet))
    print testErrors
    plt.plot(range(1,16), testErrors)
    plt.xlabel("Number Of Trees")
    plt.ylabel("Test Error")
    plt.show()
 
if __name__ == "__main__":
    main()
