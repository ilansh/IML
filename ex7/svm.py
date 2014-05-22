'''
Created on May 21, 2014

@author: ilansh
'''

import random
import numpy as np
import matplotlib.pyplot as plt
from scipy import io

class svm:
    
    def __init__(self):
        pass
    
    def show_SVM_linear(self, X, Y, w):
        # Given data (X,Y) and a classifier w, display the result.
        plt.plot(X[Y==1,0],X[Y==1,1],"+",markeredgecolor="b",markersize=10,linestyle="none",linewidth=3)
        plt.plot(X[Y==-1,0],X[Y==-1,1],"o",markeredgecolor="r",markersize=10,linestyle="none",linewidth=3)
        minx = np.min(X[:,0])
        maxx = np.max(X[:,0])
        miny = np.min(X[:,1])
        maxy = np.max(X[:,1])
        A = np.arange(minx,maxx,0.01)
        plt.plot(A,-(w[0]/w[1])*A,"k")
        plt.axis([minx, maxx, miny, maxy])
    
    def show_SVM_gaussian(self, X, Y, alphas, sigma2):
        # Given data (X,Y) and a kernel classifier alpha, display the result.
        plt.plot(X[Y==1,0],X[Y==1,1],"+",markeredgecolor="b",markersize=10,linestyle="none",linewidth=3)
        plt.plot(X[Y==-1,0],X[Y==-1,1],"o",markeredgecolor="r",markersize=10,linestyle="none",linewidth=3)
        minx = np.min(X[:,0])
        maxx = np.max(X[:,0])
        miny = np.min(X[:,1])
        maxy = np.max(X[:,1])
        X_range = np.arange(minx,maxx,0.05)
        Y_range = np.arange(miny,maxy,0.05)
        Z = np.zeros((len(X_range),len(Y_range)))
        plt.axis([minx, maxx, miny, maxy])
        m = X.shape[0]
        for i in range(len(X_range)):
            for j in range(len(Y_range)):
                Z[i,j] = alphas.dot(np.exp(-np.sum((np.tile([X_range[i], Y_range[j]],(m,1))-X)**2,1))/sigma2)
        [A, B] = np.meshgrid(Y_range,X_range)
        plt.contour(B,A,Z,[0, 0],colors="k")
    
    
    def sgd_linear(self, X, y, T, lam):
        m = T / 10
        theta = [0] * 2
        sumW = [0] * 2
        for t in range(1, T + 1):
            w = np.multiply((1.0 / (lam * t)), theta)
            i = random.sample(range(m), 1)[0]
            if y[i,:] * np.inner(w, X[i,:]) < 1:
                theta += np.multiply(y[i,:],X[i,:])
#             self.show_SVM_linear(X, y.squeeze(), w)
            plt.show()
            sumW = np.add(sumW, w)
        return sumW / T
    
    def computeG(self, X):
        Z = X * sp
        
    
    def sgd_gaussian(self, X, y, T, lam, sigma2):
        m = T / 10
        beta = [0] * m
        for t in range(1, T + 1):
            alpha = (1.0 / (lam *t)) * beta
            i = random.sample(range(m), 1)[0]
            if
           
    
def main():
    
    s = svm()
    linearData = io.loadmat("SVM_linear_data")
    w_linear = s.sgd_linear(linearData["X"], linearData["Y"], 10 * len(linearData), 0.01)
    s.show_SVM_linear(linearData["X"], linearData["Y"].squeeze(), w_linear);
    plt.show()
    
    gausianData = io.loadmat("SVM_gaussian_data")
#     plt.show()


#     X_linear, y_linear = s.loadData('X_linear', 'Y_linear')
#     print X_linear, y_linear
#     w_linear = s.sgd_linear(X_linear, y_linear, 10 * len(y_linear), 0.01)
#     print w_linear
#     s.show_SVM_linear(X_linear, y_linear, w_linear)
#     w_linear

if __name__ == "__main__":
    main()