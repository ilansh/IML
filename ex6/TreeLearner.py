
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
    
    def majority(self, labelSet):
        return 0 if sum(labelSet) < len(labelSet)/2 else 1 
    
    def maxGainFeature(self):
        pass
    
    def splitByFeature(self, domainSet, labelSet, index):
        leftDomain, middleDomain, rightDomain = [], [], []
        leftLabels, middleLabels, rightLabels = [], [], []
        
        for i in range(len(domainSet)):
            if domainSet[i][index] == -1:
                leftDomain.append(domainSet[i])
                leftLabels.append(labelSet[i])
            elif domainSet[i][index] == 0:
                middleDomain.append(domainSet[i])
                middleLabels.append(labelSet[i])
            else:
                rightDomain.append(domainSet[i])
                rightLabels.append(labelSet[i])
        
        return leftDomain, middleDomain, rightDomain, leftLabels, middleLabels, rightLabels 
        
        
    
    def ID3(self, domainSet, labelSet, featureSet):
        if self.allIs(labelSet, 1):
            return Tree(True, 1)
        if self.allIs(labelSet, 0):
            return Tree(True, 0)
        if featureSet.isEmpty():
            return Tree(True, self.majority(labelSet))
        else:
            j = self.maxGainFeature(S)
            if self.allIs(self.listify(domainSet, j), 0) or self.allIs(self.listify(domainSet, j), 1):
                return Tree(True, self.majority(labelSet))
            
            else:
                leftDomain, middleDomain, rightDomain, leftLabels, middleLabels, rightLabels = self.splitByFeature(self, domainSet, labelSet, j)
            
            t.left = ID3(self, )
            
        
        
        
class Tree:
    
    def __init__(self, isLeaf, val):
        self.isLeaf = isLeaf
    
    

def main():
    t = TreeLearner()
    t.load()
    
#     t.ID3()
    
if __name__ == "__main__":
    main()