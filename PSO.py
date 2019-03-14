

import random
import timeit
from datasetv2 import Dataset
from KMeans import KMeans as Clusterize

class Particle:
    def __init__ (self, w,c1,c2, posWall, velMin, velMax, data,ansDict,  numCen,itter):
    
        self.w = w 
        self.c1 = c1
        self.c2 = c2
        self.numCen = numCen
        self.posWall = posWall
        self.velMin = velMin
        self.velMax = velMax
        self.pos = [data[random.randrange(0,len(data))].copy()for i in range(numCen)]
        self.clust = Clusterize(data,self.pos, ansDict)
        #epsilon = c1 + c2
        #self.k = 2 / (2 - epsilon - (epsilon ** 2 - 4*epsilon)**0.5)
        self.velocity = [[random.uniform(velMin, velMax) for k in range(len(data[0]))] for i in range(numCen)]
        self.clust.clusterize()

        self.itter = itter
        self.pBest = self.pos.copy()
        self.fBest = self.clust.getaccsse()
        self.assignedNum = self.clust.sse

        #return self.fBest
    
    
    def updateVelocity (self, bestGlobal):
        #v i ( t + 1 ) = w  v i (  t ) + r 1 c 1 ( x pBest − x i ( t )) + r 2 c 2 ( x gBest − x i ( t ))
        #THIS!
        r1 = random.random()
        r2 = random.random()
        for i in range (self.numCen):
            for k in range (len(self.pos[0])):
                velocityCognition = r1 * self.c1 *(self.pBest[i][k] - self.pos[i][k])
                velocitySocial = r2 * self.c2 *(bestGlobal[i][k] - self.pos[i][k])
                self.velocity[i][k] = self.w * self.velocity[i][k] + velocityCognition + velocitySocial
                #self.velocity[a] = self.velocity[a] + velocityCognition + velocitySocial
                #self.velocity[a]= self.k * self.velocity[a]
                if self.velocity[i][k]<self.velMin:
                    self.velocity[i][k]= self.velMin
                elif self.velocity[i][k]>self.velMax:
                    self.velocity[i][k] = self.velMax
        
            
    def updatePosition (self):
        for a in range (self.numCen):
            for b in range(len(self.pos[0])):
                self.pos[a][b] += self.velocity[a][b]
                if self.pos[a][b]>self.posWall[b]:
                    self.pos[a][b]= self.posWall[b]
                if self.pos[a][b]< -self.posWall[b]:
                    self.pos[a][b]= -self.posWall[b]
        self.clust.newcentroid(self.pos.copy())
            
    def evaluation (self):
        #self.clust.run(self.itter)
        self.clust.clusterize()
        
        self.pos = self.clust.centroid
        fitness = self.clust.getaccsse()
        self.assignedNum = self.clust.sse
        if fitness <self.fBest :
            self.fBest = fitness
            self.pBest = self.pos.copy()
        return fitness
    
    def itterate(self, bestGlobal):
        self.updateVelocity(bestGlobal)
        self.updatePosition()
        return self.evaluation()


class Pso:
    def __init__ (self, numberParticle, w,c1,c2, posWall, velMin, velMax, filename,numCen, itterClust):
        self.data = Dataset(filename)
        self.data.run()
        self.swarm= []
        self.fbestGlobal = 0
        self.pbestGlobal = []
        self.numberParticle = numberParticle
        self.posWall = [len(self.data.dataDict[i])*posWall for i in range(len(self.data.dataDict))]
        for i in range(numberParticle):
            self.swarm.append (Particle (w,c1,c2, self.posWall, velMin, velMax, self.data.data, len(self.data.dataDict[-1]),numCen, itterClust))
            if i == 0:
                self.fbestGlobal =self.swarm[i].fBest
                self.pbestGlobal = self.swarm[i].pos.copy()
                self.final = self.swarm[i].assignedNum
            elif (self.swarm[i].fBest<self.fbestGlobal):
                self.fbestGblobal = self.swarm[i].fBest
                self.pbestGlobal = self.swarm[i].pos.copy()
                self.final = self.swarm[i].assignedNum
    
    def doCLI (self, numberItteration):
        i=0
        
        while (i<numberItteration):
        #for i in range (numberItteration):
            print ("===================================")
            print("itteration number: " + str(i))
            for a in range(self.numberParticle):
                current = self.swarm[a].itterate(self.pbestGlobal)
                if (current<self.fbestGlobal):
                    self.fbestGlobal = current
                    self.pbestGlobal = self.swarm[a].pos.copy()
                    self.final = self.swarm[a].assignedNum
                print ("=========================")
                print ("particle number: "+str(a))
                print ("fitness : " +str(current))
                print ("self best : " + str(self.swarm[a].fBest))
                #last = self.swarm[a].pos
            print ("=========================")
            print ("Global best : " + str(self.fbestGlobal))
            
            i+=1
        print ("=========================")
        
        #for i in range(len(self.pbestGlobal)):    
        #    print ("centroid-%s : %s" %(i,self.pbestGlobal[i]))
        clust = Clusterize(self.data.data, self.pbestGlobal,len(self.data.dataDict[-1]))
        clust.run(20)
        print("SSE : %s"%(clust.getaccsse()))
        print("Akurasi : %s"%(clust.getacc()))
        print ("=========================")
        #for a in clust.assignedNum:
        #        print("Clusterized data : %s"%(a))
    
        
"""
kk = 0
data = Dataset("nursery.txt")
data.loadDataset()
#data.intize()
data.tokenize()
#data.split()
a = data.data
b = data.dataDict
centroid = [a[random.randrange(0,len(a))], a[random.randrange(0,len(a))],a[random.randrange(0,len(a))], a[random.randrange(0,len(a))],a[random.randrange(0,len(a))]]
cluster = Clusterize(a,centroid, len(data.dataDict[-1]))
cluster.run(11)
"""

if __name__ == "__main__":
    #numberParticle, w,c1,c2, posWall, velMin, velMax, filename,numCen, itterClust)
    """
    
    data = Dataset('dataset4.csv')
    data.run()
    print(data.dataDict[-1])
    """
    random.seed()
    start = timeit.default_timer()
    #main = Pso(10,1,3,5,1,-0.1,0.1, 'nursery.txt',5,10)
    main = Pso(10,1,2,2,1,-0.1,0.1, 'nursery.txt',5,10)
    main.doCLI(20)
    stop = timeit.default_timer()
    print("================================================")
    print("================================================")
    print("TIME:%s"%(stop - start))