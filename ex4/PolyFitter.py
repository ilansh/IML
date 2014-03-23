
import numpy as np
import matplotlib.pyplot as plt


TRAINING_SET_SIZE = 20
VALIDATION_SET_SIZE = 101
TEST_SET_SIZE = 100
MAX_DEGREE = 15

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
      
    def toMatrixForm(self, d, data, dataSize):
        y = list(sample[1] for sample in data)
        y = np.matrix(y).transpose()
        X = np.zeros(shape=(d + 1, dataSize))
        for i in range(d + 1):
            for j in range(dataSize):
                X[i][j] = data[j][0] ** i
        X = np.matrix(X)
        return X, y
          
    def train(self, d):
        X, y = self.toMatrixForm(d, self.trainingSet, TRAINING_SET_SIZE)
        U, s, V = np.linalg.svd(X.transpose(), full_matrices = False)
        S = np.diag(s)
        return V * np.linalg.inv(S) * U.transpose() * y
        
    def validate(self, H):
        X, y = toMatrixForm(d, self.validationSet, VALIDATION_SET_SIZE)
        err = 0
        for h in H:
            for sample in self.validationSet:
                err += (h * X[i] - y[i]) ** 2 
    
    def fit(self):
        H = []
        print self.train(5)
        #for i in range(1, MAX_DEGREE + 1):
        #    H.append(p.train(i))
        
    
def main():
    p = PolyFitter()
    p.loadData('X.txt','Y.txt')
    p.fit()
    
if __name__ == "__main__":
    main()