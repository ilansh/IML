'''
Created on May 29, 2014
@author: ilansh, yahav_be
'''
import re
import random
import numpy


types = {"spam":1, "ham":-1}


class SpamDetector:
    
    def __init__(self):
        pass
    
    def loadData(self, fileName):
        self.samples = []       
        f = open(fileName, "r")
        for line in f:
            print line
            line = line.lower()
            line = re.sub("[^a-z-\s]",'', line)
            line = re.split("\s+", line, 1)
            line[1] = re.split("\n", line[1])[0]
            self.samples.append((line[1], types[line[0]]))

    
    def buildBow(self):
        self.bow = {}
        i = 0
        for message in self.samples:
            for word in message[0].split():
                if not self.bow.has_key(word):
                    self.bow[word] = i
                    i += 1
        print len(self.bow)
        print self.bow
        
    def calcCommonSubstrings(self):
        f = open("K-Matrix", "w+")
        for i in range(len(self.samples)):
            for j in range(len(self.samples)):
                f.write(str(self.CS(self.samples[i][0], self.samples[j][0])))
                if j != len(self.samples)-1:
                    f.write(" ")
                else:
                    f.write("\n")
        f.close()
    
    
    def CS(self, str1, str2):
        s1 = set(str1.split())
        s2 = set(str2.split())
        return len(s1 & s2)


    def loadMatrix(self, fileName):
        f = open("K-Matrix", "r")
        self.kMatrix = []
        for row in f:
            self.kMatrix.append([float(k) for k in row.split()])
        f.close()
    
    def train(self, lam):
        m = len(self.samples)/2
        alpha = [0.0]*m
        beta = [0.0]*m
        T = 10*m
        sumAlphas = [0.0]*m
        
        for t in range(1, T+1):
            print t
            
            for k in range(m):
                alpha[k] = beta[k]/(lam*t)
                sumAlphas[k] += alpha[k]
            
            i = random.sample(range(m), 1)[0]
            
            temp = [0.0]*m
            for j in range(m):
                temp[j] += alpha[j]*self.kMatrix[i][j]
        
            if self.samples[i][1]*temp < 1:
                beta[i] += self.samples[i][1]
            
        res = [0.0]*len(self.bow)
        for j in range(1,m+1):
            print j
            tmp = [(1/T)*sumAlphas[j]*(self.psi(self.samples[j])[k]) for k in range(len(self.bow))]
            print j
            res = [res[l]+tmp[l] for l in range(len(self.bow))]
            print j
        print res
        return res
        
        
    def psi(self, message):
        message = set(message[0].split())
        res = [0]*len(self.bow)
        for word in message:
            res[self.bow[word]] = 1
        return res
        
def main():
    sd = SpamDetector()
    sd.loadData("SMSSpamCollection")
    sd.buildBow()
    #sd.calcCommonSubstrings()
    sd.loadMatrix("K-Matrix")
    for lam in [10, 1, 0.1, 0.01, 0.001]:
        res = sd.train(lam)
        f = open("lambda" + str(lam), "w+")
        f.write(str(res))
        f.close()
        #sd.test()
    
    
    #sd.calcCommonSubstrings()
    #sd.initBagOfWords()
    #sd.mapToFeatureSpace()
    
    #for lam in [10, 1, 0.1, 0.01, 0.001]:
    #pass


if __name__ == "__main__":
    main()
