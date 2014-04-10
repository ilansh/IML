
class TreeLearner:
    
    def __init__(self):
        self.trainingDomain = []
        self.trainingLabels = []
        self.testDomain = []
        self.testLabels = []
    
    def loadSet(self, domainFileName, labelsFileName):
        fDomain = open(domainFileName, 'r')
        fLabels = open(labelsFileName, 'r')
        domain = []
        for line in fDomain:
            domain.append(map(int, line.split()))
        labels = []
        for line in fLabels:
            labels.append(int(line))
        return domain, labels
    
    def load(self):
        self.trainingDomain, self.trainingLabels = self.loadData('DT/Xtrain','DT/Ytrain')
        self.testDomain, self.testLabels = self.loadData('DT/Xtest', 'DT/Ytest')
        
        
    def listify(self, domainSet, index):
        res = []
        for item in domainSet:
            res.append(item[index])
        return res
        
    def allIs(self, valueList, value):
        for item in valueList:
            if item != value:
                return False
        return True
    
    def majority(self, S):
        zeros = 0
        ones = 0
        
        for pair in S:
            if pair[1] == 0:
                zeros += 1
            else:
                ones += 1
        return 0 if zeros > ones else 1 
    
    def maxGainFeature(self):
        pass
    
    
    def ID3(self, S, A):
        if self.allIs(self.trainingSet, 1):
            return Tree(True, 1)
        if self.allIs(self.trainingSet, 0):
            return Tree(True, 0)
        if A.isEmpty() == 0:
            return Tree(True, self.majority(S))
        else:
            j = self.maxGainFeature(S)
            if 
        
class Tree:
    
    def __init__(self, isLeaf, val):
        self.isLeaf = isLeaf
    
    

def main():
    t = TreeLearner()
    t.load()
    
#     t.ID3()
    
if __name__ == "__main__":
    main()