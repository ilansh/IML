'''
Created on May 29, 2014

@author: ilansh
'''

types = {"spam":1, "ham":-1}


class SpamDetector:
    
    def __init__(self):
        pass
    
    def loadData(self, fileName):
        samples = []       
        f = open(fileName, "r")
        for line in f:
            line = line.split()
            samples.append((tuple(line[1:]), types[line[0]]))
        self.trainingSet = set(samples[:len(samples)/2])
        self.testSet = set(samples[len(samples)/2:])
   
    def initBagOfWords(self):
        self.bow = {}
        index = 0
        for message in self.trainingSet:
            for word in message[0]:
                self.bow[word] = index
        for message in self.testSet:
            for word in message[0]:
                self.bow[word] = 1
        print self.bow
   
    def mapToFeatureSpace(self):
        phi = []
        for message in self.trainingSet:
            for word in message[0]:
                
                
   
   
def main():
    
    sd = SpamDetector()
    sd.loadData("SMSSpamCollection")
    sd.initBagOfWords()
    sd.mapToFeatureSpace()
    
    #for lam in [10, 1, 0.1, 0.01, 0.001]:
       #pass


if __name__ == "__main__":
    main()