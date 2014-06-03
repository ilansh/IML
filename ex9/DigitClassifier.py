'''
Created on Jun 2, 2014
@author: yahav_be
'''
import numpy as np
import time


class DigitClassifier:
    
    def init(self):
        pass
    
    # Load data
    def load(self):
        # (60000 X 784) matrix
        self.Xtrain = np.loadtxt("Xtrain.gz")
        # (60000 X 1) matrix
        self.Ytrain = np.loadtxt("Ytrain.gz")
        # (10000 X 784) matrix
        self.Xtest = np.loadtxt("Xtest.gz")
        # (10000 X 1) matrix
        self.Ytest = np.loadtxt("Ytest.gz")
        print 'loaded'
    
    
    def train(self, lam):
        # Dimension of psi mapping = (Number of x features * Number of y classes)
        d = self.Xtrain.shape[1] * 10
        # Number of samples
        m = self.Xtrain.shape[0]
        # Number of iterations
        T = 10 * m
        w = np.zeros(d)
        sum_w = np.zeros(d)
        
        yRange = xrange(10)
        
        start = time.time()
        
        for t in xrange(1, T + 1):
            eta = 1.0 / (lam * t)
            i = np.random.randint(m)
            Xi = self.Xtrain[i,:]
            Yi = int(self.Ytrain[i])
            psiArr = [self.psi(Xi, y) for y in yRange];
            
            y_hat = np.argmax([self.zeroOneLoss(y, Yi) + np.dot(w, np.subtract(psiArr[y], psiArr[Yi])) for y in yRange])
            v = np.multiply(lam, w) + np.subtract(psiArr[y_hat], psiArr[Yi])
            w = w - (eta * v)
            sum_w = np.add(sum_w, w)
    
        end = time.time()
        print 'calc time for lambda ' + str(lam) + ' is ' + str(end - start)
        return np.multiply(1.0 / T, sum_w) 
    
    
    def zeroOneLoss(self, y1, y2):
        if int(y1) == int(y2):
            return 0.0
        else:
            return 1.0
    
    
    def psi(self, x, y):
        y = int(y) + 1
        n = self.Xtrain.shape[1]
        k = 10
        return np.concatenate([np.zeros(n * (y - 1)), x, np.zeros(n * (k - y))])


    def test(self, w):
        sumErrors = 0.0
        m = self.Xtest.shape[0]
        for i in xrange(m):
            prediction = np.argmax([np.dot(w, self.psi(self.Xtest[i,:], y)) for y in xrange(10)])
            if prediction != self.Ytest[i]:
                sumErrors += 1.0
        return sumErrors / m

def main():
    dc = DigitClassifier()
    dc.load()
    
    for lam in [1.0, 0.1, 0.01]:
        w = dc.train(lam)
        print 'test error for lambda ' + str(lam) + ' is: ' + str(dc.test(w))
    
if __name__ == "__main__":
    main()