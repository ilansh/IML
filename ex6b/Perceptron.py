'''
Created on May 7, 2014

@author: ilansh
'''

import numpy as np

class Perceptron:
    
    def __init__(self):
        pass


    def loadData(self, domainFile, labalsFile):
        fDomain = open(domainFile, 'r')
        fLabels = open(labalsFile, 'r')
        domain = []
        result = []
        for line in fDomain:
            domain.append(map(float, line.split()))
        for i, line in enumerate(fLabels):
            result.append((tuple(domain[i]), int(line)))
        return result


    def percept(self, sampleData):
        w = tuple([0] * 784)
        for sample in sampleData:
            y = sample[1]
            x = sample[0]
            if (y * np.inner(w, x) <= 0):
                w = np.add(w , np.multiply(y, x))
        return w
        


    def test(self, w, sampleData):
        numErrors = 0
        for sample in sampleData:
            x = sample[0]
            prediction = np.inner(w, x)
            if np.sign(prediction) != sample[1]:
                numErrors += 1
        print numErrors
        return float(numErrors) / len(sampleData) 
                



def main():
    p = Perceptron()
    trainData = p.loadData('Xtrain', 'Ytrain')
    testData = p.loadData('Xtest', 'Ytest')
    w = p.percept(trainData)
    print p.test(w, testData)


if __name__ == "__main__":
    main()