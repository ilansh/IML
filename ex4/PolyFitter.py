
import numpy as np
import matplotlib.pyplot as plt


TRAINING_SET_SIZE = 20
VALIDATION_SET_SIZE = 101
TEST_SET_SIZE = 100

class PolyFitter:

    def __init__(self):
        self.trainingSet = []
        self.validationSet = []  
        self.testSet = [] 
        pass  
    
    def loadData(self, domainFileName, labelsFileName):
        fDomain = open(domainFileName, 'r')
        fLabels = open(labelsFileName, 'r')
        domain = fDomain.read().split()
        labels = fLabels.read().split()
        for i in range(TRAINING_SET_SIZE):
            self.trainingSet.append((float(domain[i]), float(labels[i])))
        for i in range(TRAINING_SET_SIZE, VALIDATION_SET_SIZE):
            self.validationSet.append((float(domain[i]), float(labels[i])))
        for i in range(TRAINING_SET_SIZE + VALIDATION_SET_SIZE, TEST_SET_SIZE):
            self.testSet.append((float(domain[i]), float(labels[i])))
          
    def train(self, d):
        X = np.zeros(shape=(d + 1, TRAINING_SET_SIZE))
        for i in range(d + 1):
            for j in range(TRAINING_SET_SIZE):
                X[i][j] = self.trainingSet[j][0] ** i
        X = np.matrix(X)

def main():
    p = PolyFitter()
    p.loadData('X.txt','Y.txt')
    p.train(4)
    
if __name__ == "__main__":
    main()