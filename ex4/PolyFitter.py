
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter

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
        for i in range(TRAINING_SET_SIZE, VALIDATION_SET_SIZE + TRAINING_SET_SIZE):
            self.validationSet.append((float(domain[i]), float(labels[i])))
        for i in range(TRAINING_SET_SIZE + VALIDATION_SET_SIZE, TEST_SET_SIZE + TRAINING_SET_SIZE + VALIDATION_SET_SIZE):
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
          
    def errorOnSample(self, h, X, y, sampleSize):
        err = 0
        for i in range(sampleSize):
            err += float(np.dot(h, X[:,i]) - y[i]) ** 2
        return err / sampleSize
    
    def train(self, d):
        X, y = self.toMatrixForm(d, self.trainingSet, TRAINING_SET_SIZE)
        U, s, V = np.linalg.svd(X.transpose(), full_matrices = False)
        S = np.matrix(np.diag(s))
        return np.hstack((V.H * S.I * U.H * y).tolist())
        
    def validate(self, H):
        errList = []
        for h in H:
            X, y = self.toMatrixForm(len(h) - 1, self.validationSet, VALIDATION_SET_SIZE)
            errList.append(self.errorOnSample(h, X, y, VALIDATION_SET_SIZE))
        return errList
    
    def trainingErrors(self, H):
        errList = []
        for h in H:
            X, y = self.toMatrixForm(len(h) - 1, self.trainingSet, TRAINING_SET_SIZE)
            errList.append(self.errorOnSample(h, X, y, TRAINING_SET_SIZE))
        return errList
        
    def test(self, h):
        err = 0
        X, y = self.toMatrixForm(len(h) - 1, self.testSet, TEST_SET_SIZE)
        return self.errorOnSample(h, X, y, TEST_SET_SIZE)
    
    def fit(self):
        H = []
        for i in range(1, MAX_DEGREE + 1):
            H.append(self.train(i))
        validationErrors = self.validate(H)
        h = H[validationErrors.index(min(validationErrors))] # h is the one with the minimal validation error over H
        trainingErrors = self.trainingErrors(H) #get the training sample errors for H
        print 'Test error of best fitting polynomial is: ' + str(self.test(h))
        print 'The degree of the best fitting polynomial is: ' + str(len(h))
        plt.plot(range(1,11), validationErrors[:10])
        plt.plot(range(1,11), trainingErrors[:10])
        plt.xlabel('degree')
        plt.ylabel('err')
        plt.show()
        

        
    
def main():
    p = PolyFitter()
    p.loadData('X.txt','Y.txt')
    p.fit()
    
if __name__ == "__main__":
    main()