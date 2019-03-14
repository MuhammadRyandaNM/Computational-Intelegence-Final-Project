
from numpy.random import choice
import math
class KMeans:
    def __init__(self, data, centroid, ansdict):
        """
        #centroid is list of list
        #ansdict is count of the cluster
        """
        self.data = data
        self.ansdict = ansdict
        self.centroid = centroid.copy()
    
    def euclidean(self, v1,v2):
        
        length = len(v1)
        distance = 0
        for i in range(length):
            distance += pow(v1[i] - v2[i],2)
        return math.sqrt(distance)
    
    def newcentroid(self, centroid):
        self.centroid = centroid
    
    def getaccsse(self):
        self.sse = [0 for i in range(len(self.assignedDist))]
        for i in range(len(self.assignedDist)):
            for k in range(len(self.assignedDist[i])):
                self.sse[i]+=self.assignedDist[i][k]
        tot =0
        for i in self.sse:
            tot+=i
        return tot
    
    def getacc(self):
        accom = []
        #print([len(self.assigned[i])for i in range(len(self.assigned))])
        k =0
        self.assignedNum= [[] for i in range(len(self.assigned))]
        for v in self.assigned:
            acc = {i: 0 for i in range(self.ansdict)}
            if v == []:
                continue
            leng = len(v[0])-1
            
            if leng<0:
                continue
            for i in v:
                #print(i)
                #print(leng)
                acc[i[leng]]+=1
            self.assignedNum[k].append(acc)
            k+=1
            jumlah = 0
            for i in acc.values():
                jumlah+=i
            maxi = max(acc.values())
            acc = maxi/jumlah *100
            accom.append(acc)
        tot = 0
        for i in accom:
            tot += i
        tot = tot/len(accom)
        
        return tot
    
    
    def clusterize (self):
        distance = []
        for i in range(len(self.data)):
            distance.append([self.euclidean(self.data[i], self.centroid[k]) for k in range(len(self.centroid))])
        
        distanceDict = []
        for i in distance:
            temp = {}
            for a in range(len(i)):
                temp[i[a]] = a
            distanceDict.append(temp)
        self.assigned = [[] for i in range(len(self.centroid)) ]
        self.assignedAndIndex = [[] for i in range(len(self.centroid)) ]
        self.assignedAndIndex2 = [[] for i in range(len(self.centroid)) ]
        self.assignedDist = [[] for i in range(len(self.centroid)) ]
        self.assignedNum= [[0 for i in range(self.ansdict) ] for i in range(len(self.centroid))]
        for i in range (len(self.data)):
            temp = min(distanceDict[i].keys())
            tempDist = temp
            temp = distanceDict[i][temp]
            self.assignedDist[temp].append(tempDist)
            self.assigned[temp].append( self.data[i])
            templist = [tempDist, i]
            self.assignedAndIndex[temp].append(  templist )
            self.assignedAndIndex2[temp].append(  templist )

            self.assignedNum[temp][self.data[i][len(self.data[i])-1]]+=1
            #self.updatecentroid()
    def print_Output(self):
        #self.clusterize()
        with open('outputnya.txt', 'w') as f:
            for item in self.assignedAndIndex2:
                for y in item:
                    f.write("%s\n" % y)
                print("=======================")
    def getClosestData(self):
        self.clusterize()
        self.closest = []
        self.closestDist = []
        for i in self.assignedAndIndex:
            temp = i.copy()
            temp.sort()
            templist = [k[1] for k in temp]
            self.closest.append(templist[1:6].copy())
            templist = [k[0] for k in temp]
            self.closestDist.append(templist[1:6].copy())
    
    def getRandomData(self, num):
        self.clusterize()
        self.random=[]
        self.randomDist=[]
        for a in range(len(self.centroid)):
            templist = []
            temp2 = [i for i in range(len(self.assignedAndIndex[a]))]
            for b in range(num):
                temp = choice(temp2)
                
                temp2.remove(temp)
                temp = self.assignedAndIndex[a][temp]
                #print(temp)
                templist.append(temp)
            #print(templist)
            tempdata = [templist[i][1] for i in range(len(templist))]
            tempdist = [templist[i][0] for i in range(len(templist))]
            self.random.append(tempdata)
            self.randomDist.append(tempdist)
                
                
    
    def updatecentroid(self):
        centroid = [[0 for k in range (len(self.centroid[0]))]for i in range(len(self.centroid))]
        a =0    
        for i in self.assigned:
            for k in i:
                b = 0
                for j in k:
                    #if(j == k):
                        #break
                    centroid[a][b]+=j
                    b+=1
            a+=1
        leng = []
        for i in self.assigned:
            leng.append(len(i))
        
        for i in range(len(centroid)):
            for j in range(len(centroid[0])):
                if leng[i] == 0:
                    continue
                centroid[i][j]/=leng[i]
        self.centroid = centroid
        
    def run(self, itteration):
        for a in range(itteration):
            self.clusterize()
            self.updatecentroid()
        
