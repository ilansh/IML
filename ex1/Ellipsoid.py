'''
Created on Feb 26, 2014

@author: yahav_be
'''

import numpy as np
import matplotlib.pyplot as plt

class Elipsoid:
    def __init__(self):
        pass  
    
    d = 0 # Dimension
    X = None # Images matrix
    Y = None # Labels vector
    n = 0 # Number of iterations
    
    # Load Images and Labes from text files
    def load(self):
        self.X = np.loadtxt("train4vs7_data.txt.gz")
        self.Y = np.loadtxt("train4vs7_labels.txt.gz")
        self.d = self.X.shape[0]
        self.n = self.X.shape[1]
        
    # Show a particular image
    def show(self, index):
        plt.imshow(self.X[:,index].reshape(28,28),cmap="gray")
        plt.show()
    
    # Run the Elipsoid algorithm on the existing paremeters
    def run(self):
        w = np.zeros((self.d,))
        A = np.eye(self.d)
        M = 0 # counts mistakes
        eta = self.d*self.d/(self.d*self.d-1.0)
        
        for t in range(0, self.n):
            print (t)
            yHat = np.sign(np.dot(w, self.X[:,t]))
            if self.Y[t] != yHat:
                M = M+1
                Ax = np.dot(A , self.X[:,t])
                xAx = np.dot(self.X[:,t] , Ax)
                w = w + self.Y[t]/((self.d+1)*np.sqrt(xAx)) * Ax
                A = eta*(A - (2.0/((self.d+1.0)*xAx)) * np.outer(Ax,Ax))
        
        tmp = 1/(1+np.exp(-10*w/w.max()))
        plt.imshow(tmp.reshape(28,28),cmap="gray")
        plt.savefig("finalPred.png")
        plt.show()

        print("The Total Number of mistakes made by Elipsoid was:" + str(M))

def main():
    
    elip = Elipsoid()

    elip.load()
    elip.run()
    
if __name__ == "__main__":
    main()