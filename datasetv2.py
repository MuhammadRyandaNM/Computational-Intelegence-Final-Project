
import csv
import random
from sklearn.preprocessing import MinMaxScaler
class Dataset:
    def __init__(self, name):
        self.name = name

    def loadDataset(self):
        self.data = []
        with open(self.name, newline='') as f:
            reader = csv.reader(f)
            reader = list(reader)
        
        self.data = reader.copy()
        
    
    def intize(self):
        for a in range (len(self.data)):
            for b in range(len(self.data[0])):
                self.data[a][b]=int(self.data[a][b])
        dataTrans = []
        for i in range(len(self.data[0])):
            dataTrans.append([row[i] for row in self.data])
        dataToken=[]
        for i in range(len(self.data[0])):
            dataToken.append(set(dataTrans[i]))
        for i in range(len(dataToken)):
            dataToken[i] = list(dataToken[i])
        self.dataDict = []
        self.rang = []
        for i in dataToken:
            temp = {}
            temp2 = {}
            for a in range(len(i)):
                temp[i[a]] = a
                temp2[i[a]] = 0
            self.dataDict.append(temp)
            self.rang.append(temp2)
            
    def split(self):
        self.ans = [row.pop() for row in self.data]
    
    def tokenize(self):
        dataTrans = []
        for i in range(len(self.data[0])):
            dataTrans.append([row[i] for row in self.data])
        dataToken=[]
        for i in range(len(self.data[0])):
            dataToken.append(set(dataTrans[i]))
        for i in range(len(dataToken)):
            dataToken[i] = list(dataToken[i])
            
        self.dataDict = []
        self.rang = []
        for i in dataToken:
            temp = {}
            temp2 = {}
            for a in range(len(i)):
                temp[i[a]] = a
                temp2[i[a]] = 0
            self.dataDict.append(temp)
            self.rang.append(temp2)
        
        #self.rang = [[0 for i in range(len(self.data[i]))] for i in range (len(self.dataDict))]
        #self.rang = {[i = 0 for i in range(self.dataDict[k])]for k in range (len(self.dataDict))}
        for i in range (len(self.data)):
            for k in range(len(self.data[i])):
                
                self.rang[k][self.data[i][k]]+=1
                self.data[i][k] = self.dataDict[k][self.data[i][k]]
              
        return self.data
    
    def removeNoise(self):
        kelas = self.rang[-1]
        for a in range(len(kelas)):
            maxim = max(kelas.values())
            minim = min(kelas.values())
            if maxim > 100 * minim and minim != 0:
                for b in kelas:
                    if kelas[b]==minim:
                        toremove = self.dataDict[-1][b]
                        toremovestring = b
                leng = len(self.data[0])-1
                flag = 0
                topop = []
                for b in range(len(self.data)):
                    print(b)
                    if self.data[b][leng]==toremove:
                        self.rang[-1][toremovestring]-=1
                        topop.append(b)
                        flag+=1
                        if flag >= minim:
                            break
                for b in range(len(topop)):
                    self.data.pop(topop[b]-b)
                del (self.rang[-1][toremovestring])
    
    def equalizeClass(self):
        kelas = self.rang[-1]
        kelasval = kelas.values()
        minim = min(kelasval)
        for a in kelas:
            if kelas[a]== minim:
                tokeep = a
                break
        equalize = {}
        for b in self.rang[-1]:
            if b!=tokeep:
                equalize[b]= self.rang[-1][b]
        toclassify = [self.dataDict[-1][i] for i in equalize]
        dataclass = {self.dataDict[-1][i]:[] for i in self.rang[-1]}

        for a in range(len(self.data)):
            #print(self.data[a][-1])
            dataclass[self.data[a][-1]].append( self.data[a])
        tokeep = self.dataDict[-1][tokeep]
        wall = len(dataclass[tokeep])
        #print(wall)
        newdata=[]
        for i in toclassify:
            temp = []
            for j in range(wall):
                a = random.choice(dataclass[i])
                dataclass[i].remove(a)
                temp.append(a)
            newdata.append(temp)
        newdata.append(dataclass[tokeep])
        newdataset = []
        for i in newdata:
            for j in i:
                newdataset.append(j)
        self.data = newdataset.copy()   
        
    
    def run (self):
        self.loadDataset()
        self.tokenize()
        self.removeNoise()
        self.equalizeClass()
        #self.tokenize()
        #self.intize()
""" 
data = Dataset('nursery.txt')
data.run()
print(data.dataDict)
#print(data.rang[-1])
"""