
from datasetv2 import Dataset
from KMeans import KMeans
from numpy.random import choice
import copy as cp
import random
import numpy as np
import timeit

class Ant():
    def __init__(self,data, ansdict,numCen, tabuindex, pheromap, alpha, beta, max_itter, decay):
        self.centroid = [data[random.randrange(0,len(data))].copy()for i in range(numCen)]
        self.defCentroid = self.centroid.copy()
        self.clust = KMeans(data, self.centroid, ansdict)
        self.max_itter = max_itter
        self.alpha = alpha
        self.beta = beta
        self.pheromap = pheromap
        self.tabu = {}
        self.decay = decay
        self.fitness = 0
        self.numCen = numCen
        self.data = data
        self.tabuIndex = tabuindex
    def init(self):
        self.centroid = self.defCentroid.copy()
        self.tabu = {}
    
    def spreadPheromon(self):
        self.clust.getRandomData(5)
        self.possibleMove = self.clust.random
        self.distMove = self.clust.randomDist
        #print(self.possibleMove)
        #print(type(self.pheromap))
        for nodeList in range(len(self.possibleMove)):
            for node in range(len(self.possibleMove[nodeList])):
                a = self.possibleMove[nodeList][node]
                try:
                    self.pheromap[a] = self.pheromap[a] *self.decay
                    try:
                        self.pheromap [a]+=1.0/self.distMove[nodeList][node]
                    except:
                        self.pheromap [a]+=0
                except KeyError:
                    self.pheromap[a] = self.distMove[nodeList][node]
        #print(self.pheromap)
        #print(self.distMove)
    def probMov(self):
        self.poss_mov = [[] for i in range(self.numCen)]
        self.prob_mov=[[]for i in range(self.numCen)]
        for nodeList in range(len(self.possibleMove)):
            for node in range(len(self.possibleMove[nodeList])):
                a = self.possibleMove[nodeList][node]
                try:
                    temp = self.tabu[a]
                except KeyError:
                    self.poss_mov[nodeList].append(a)    
                    temp = (self.pheromap[a]**self.alpha)*(self.distMove[nodeList][node]**self.beta)
                    self.prob_mov[nodeList].append(temp)
                
        temp_mov = len(self.possibleMove)
        for a in range(len(self.poss_mov)):
            for b in range(len(self.poss_mov[a])):
                self.prob_mov[a][b] = self.prob_mov[a][b] / (temp_mov)
        #print(self.prob_mov)
        
    def decaytabu(self):
        todel = []
        for node in self.tabu:
            self.tabu[node]-=1
            if (self.tabu[node]==0):
                todel.append(node)
        for node in todel:
            del self.tabu[node]
    
    def mov(self):
        self.decaytabu()
        newcen = []
        #print(self.poss_mov)
        for i in range(self.numCen):
            
            a = list(range(len(self.poss_mov[i])))
            
            movement = choice(a,1,self.prob_mov[i])
            movement = movement[0]
            #print(self.poss_mov[i][movement])
            newcen.append(self.data[self.poss_mov[i][movement]])
            self.tabu[self.poss_mov[i][movement]]=self.tabuIndex
        self.centroid = newcen.copy()
        self.clust.newcentroid(self.centroid)
        #self.clust.clusterize()
        #print(self.centroid)
        
    
    def run(self):
        for a in range(self.max_itter):
            self.spreadPheromon()
            self.probMov()
            self.mov()
        self.fitness = self.clust.getaccsse()
            


class Colony:
    def __init__(self, filename,numcen = 4, nant =10, maxitter= 10 ,alpha = 1,beta =2,decay=0.8, tabuindex =3):
      
        self.alpha = alpha
        self.beta = beta
        self.decay= decay
        self.maxitter = maxitter
        self.data = Dataset(filename)
        self.data.run()
        self.pheromap = {}
        self.ants = []
        ansdict = len(self.data.dataDict[-1])
        self.ansdict = ansdict
        self.ants = [Ant(self.data.data,ansdict, numcen, tabuindex, self.pheromap, alpha, beta, maxitter, decay) for a in range(nant)]
    
    def run(self, itter):
        bestFitness = np.inf
        bestGen = []
        bestCentroid = None
        for a in range(itter):
            i = 0
            for ant in self.ants:
                ant.init()
                ant.run()
                #print(ant.tabu)
                if( ant.fitness<bestFitness):
                    bestFitness= ant.fitness
                    bestCentroid = ant.centroid
                print ("=========================")
                print ("ant number: "+str(i))
                print ("fitness : " +str(ant.fitness))
                i+=1
            print("=====================================")
            print("Itteration : %s"%(a))
            print("=====================================")
            print("bestfitness : %s"%(bestFitness))
            bestGen.append(bestFitness)
        for i in range(len(bestGen)):
            print("best fitness at generation -%s : %s" %(i, bestGen[i]))
        clust = KMeans(self.data.data,bestCentroid, self.ansdict)
        clust.run(20)
        print("===================================================")
        print("====================K-Means========================")
        print("===================================================")
        print("SSE : %s"%(clust.getaccsse()))
        print("SSE : %s"%(clust.getacc()))
        print("Assigned data : %s"%(clust.assignedNum))
        #print(self.pheromap)
        return self.pheromap
                
                    
        
if __name__ == "__main__":
    start = timeit.default_timer()
    
    #filename,numcen = 5, nant =10, maxitter= 20 ,alpha = 1,beta =2,decay=0.8, tabuindex =3
    main = Colony("nursery.txt")
    main.run(10)
    stop = timeit.default_timer()
    print("TIME: %s"%(stop-start))
