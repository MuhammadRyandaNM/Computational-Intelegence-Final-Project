
import random
from dataset import Dataset
from KMeans import KMeans

Data = Dataset('nursery.txt')
Data.run()
numCen=5
centroid = [Data.data[random.randrange(0,len(Data.data))].copy()for i in range(numCen)]
Clust = KMeans(Data.data, centroid, 5)
Clust.run(10)
print(Clust.getaccsse())
print(Clust.getacc())