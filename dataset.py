
import csv


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
    def run (self):
        self.loadDataset()
        self.tokenize()
        #self.intize()
    