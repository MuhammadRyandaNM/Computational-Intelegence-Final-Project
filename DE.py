

import numpy as np
import random
import timeit
from datasetv2 import Dataset
from KMeans import KMeans


class Particle:
    def __init__(self,data,numCen,ansdict):
        self.centroid = [data[random.randrange(0,len(data))].copy()for i in range(numCen)]
        self.clust = KMeans(data, self.centroid, ansdict)
        self.lastfitness = self.getfitness()
    
    def getfitness(self, centroid = None):
        if centroid != None:
            self.clust.newcentroid(centroid)
        self.clust.clusterize()
        fitness = self.clust.getaccsse()
        self.clust.newcentroid(self.centroid)
        return fitness

class De:
    def __init__(self,dataset, mut = 0.2, crossp=0.8, population=10, itter= 10, centroidNum = 4, itterkmeans = 10):
        self.itterkmeans = itterkmeans
        self.centroidNum = centroidNum
        
        self.mut = mut
        self.crossp = crossp
        self.populationsize = population
        self.itter = itter
        self.data = Dataset(dataset)
        self.data.run()
        self.dimension = len(self.data.data[0])
        self.boundup = [len(self.data.dataDict[i])for i in range(len(self.data.dataDict))]
        self.bounddown = [-len(self.data.dataDict[i])for i in range(len(self.data.dataDict))]
        
        ansdict = len(self.data.dataDict[-1])
        self.ansdict = ansdict
        #print(centroid)
        self.population = [Particle(self.data.data, centroidNum, ansdict) for i in range(population) ]
        self.fitness = [self.population[i].lastfitness for i in range(self.populationsize)]
    
    def Evolutionize(self):
        bestGeneration = []
        bestCentroid = None
        bestFitness = np.inf
        for i in range(self.itter):
            tempBestGen = np.inf
            for j in range(self.populationsize):
                particles = [k for k in range(self.populationsize) if k!=j] #not current
                randomparticle = []
                for a in range(3):
                    ran = random.choice(particles)
                    randomparticle.append(ran)
                    particles.remove(ran)
                
                a,b,c = randomparticle
                mutant = []
                for z in range( self.centroidNum  ):
                    mutant.append([])
                    for x in range(self.dimension):
                        #print(len(self.population[a].centroid))
                        #print(len(self.population[a].centroid[z]))
                        tempa = self.population[a].centroid[z][x]
                        tempb = self.population[b].centroid[z][x] 
                        tempc = self.population[c].centroid[z][x] 
                        temp = tempa - self.mut * (tempb - tempc)
                        mutant[z].append(temp)
                    #temp = [self.population[a].centroid[z][itt] + 
                     #        self.mut * (self.population[b].centroid[z][itt] 
                      #       - self.population[c].centroid[z][itt]) for itt in range(len(self.population[0].centroid[z])-1)]
                    #print (temp)
                #print(mutant)
                for a in range(len(mutant)):
                    for b in range(len(mutant[a])):
                        mutant[a][b]= np.clip(mutant[a][b],self.bounddown[a], self.boundup[a])
                        
                crossTruth =  [np.random.rand(self.dimension) <self.crossp for a in range(self.centroidNum)]
                #print(crossTruth)
                
                trial = self.population[j].centroid.copy()
                for a in range(len(crossTruth)):
                    for b in range(len(crossTruth[a])):
                        if(crossTruth[a][b]):
                            trial[a][b] = mutant[a][b]
                temp = self.population[j].getfitness(trial)
                print ("=========================")
                print ("particle number: "+str(j))
                print ("fitness trial : " +str(temp))
                print ("self best : " + str(self.population[j].lastfitness))
                #print("%s, %s" %(self.population[j].lastfitness,tempBestGen))
                #print("%s" %(self.population[j].lastfitness<tempBestGen))
                if self.population[j].lastfitness<tempBestGen:
                    #recording best fitness each generation
                    tempBestGen= self.population[j].lastfitness
                
                if (self.population[j].lastfitness<bestFitness):
                    bestFitness = self.population[j].lastfitness
                    bestCentroid = self.population[j].centroid
                    
                if temp < self.population[j].lastfitness:
                    self.population[j].lastfitness = temp
                    self.population[j].centroid = trial
                
            bestGeneration.append(tempBestGen)
            print("=====================================")
            print("Itteration : %s"%(i))
            print("=====================================")
            print("bestfitness : %s"%(min(self.fitness)))
                
                
        
        for i in range(len(bestGeneration)):
            print("best fitness at generation -%s : %s" %(i, bestGeneration[i]))
        print("---------------------------------------------------")
        print("Centroid")
        print("---------------------------------------------------")
        for i in range(len(bestCentroid)):
            print("centroid-%s :%s"%(i, bestCentroid[i]))
        clust = KMeans(self.data.data,bestCentroid, self.ansdict)
        clust.run(self.itterkmeans)
        print("===================================================")
        print("====================K-Means========================")
        print("===================================================")
        print("SSE : %s"%(clust.getaccsse()))
        print("Akurasi : %s"%(clust.getacc()))
        print("Assigned data : %s"%(clust.assignedNum))
        print("---------------------------------------------------")
        print("Centroid")
        print("---------------------------------------------------")
        for i in range(len(clust.centroid)):
            print("centroid-%s :%s"%(i, clust.centroid[i]))
        clust.print_Output()
        #for i in range(len(clust.centroid)):
        #    print("centroid-%s :%s"%(i, clust.centroid[i]))
        
                
        
if __name__ == "__main__":
    start = timeit.default_timer()
    main = De("nursery.txt")
    main.Evolutionize()
    stop = timeit.default_timer()

    print("================================================")
    print("================================================")
    
    print("TIME:%s"%(stop - start))