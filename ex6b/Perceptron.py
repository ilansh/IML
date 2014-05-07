'''
Created on May 7, 2014

@author: ilansh
'''



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









def main():
    p = Perceptron()
    trainData = p.loadData('Xtrain', 'Ytrain')
    testData = p.loadData('Xtest', 'Ytest')
    


if __name__ == "__main__":
    main()