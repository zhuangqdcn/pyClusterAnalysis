import math
from collections import deque
from itertools import product
class Configure:
    def __init__(self,well, boxXYZ):
        # @param well double
        # @param boxXYZ (double, double, double)
        self.n = 0
        self.well = well
        self.well2 = well*well
        self.coords = [] # [double x, double y, double z]
        self.clusters = [] # [set(Clusters)]
        self.box = boxXYZ
        self.nxCell = int(boxXYZ[0]/self.well2/1.5)
        self.nyCell = int(boxXYZ[1]/self.well2/1.5)
        self.nzCell = int(boxXYZ[2]/self.well2/1.5)
        self.lxCell = float(boxXYZ[0]/self.nxCell)
        self.lyCell = float(boxXYZ[1]/self.nyCell)
        self.lzCell = float(boxXYZ[2]/self.nzCell)
        self.cells = [[[ [] for i in xrange(self.nzCell)] for j in xrange(self.nyCell)] for k in xrange(self.nxCell)]
        self.clusterCOM = [] #[double x, double y, double z]
        self.clusterInertia = [] # [double Ix, double Iy, double Iz]
        
    def add(self, x, y, z):
        ixCell, iyCell, izCell = self.cellDetermine(x,y,z)
        self.cells[ixCell][iyCell][izCell].append(self.n)
        self.coords.append(((x,y,z), (ixCell,iyCell, izCell)))
        self.n += 1
        return

    def cellDetermine(self, x,y,z):
        ixCell = min(int(x/self.lxCell), self.nxCell-1)
        iyCell = min(int(y/self.lyCell), self.nyCell-1)
        izCell = min(int(z/self.lzCell), self.nzCell-1)
        return (ixCell, iyCell, izCell)

    def neighborIndex(self, idx):
        ixCell, iyCell, izCell = self.coords[idx][1]
        xLeftCell = self.nxCell - 1 if ixCell==0 else ixCell - 1
        xRightCell = 0 if ixCell==self.nxCell -1 else ixCell + 1
        yLeftCell = self.nyCell - 1 if iyCell==0 else iyCell - 1
        yRightCell = 0 if iyCell==self.nyCell -1 else iyCell + 1
        zLeftCell = self.nzCell - 1 if izCell==0 else izCell - 1
        zRightCell = 0 if izCell==self.nzCell -1 else izCell + 1
        neighbors = list(product([ixCell, xLeftCell, xRightCell],[iyCell, yLeftCell, yRightCell],[izCell, zLeftCell, zRightCell]))
        # print neighbors
        return neighbors

    
    def finishInput(self):
        self.calcCluster()
        self.calcClusterCOM()
        self.calcClusterInertia()
        # print self.clusterCOM
        # print self.clusterInertia
        # for cluster in self.clusters:
        #     print cluster
        return

    def calcCluster(self):
        # distances = [[0. for i in xrange(self.n)] for j in xrange(self.n)]
        # for i in xrange(self.n):
        #     for j in xrange(i,self.n):
        #         distances[i][j] = self.distance(self.coords[i],self.coords[j])
        #         distances[j][i] = distances[i][j]
        searchSet = set(range(self.n))
        while searchSet:
            idx = searchSet.pop()
            self.clusters.append(set([]))
            self.clusters[-1].add(idx)
            self.dfs(idx, searchSet)
        return

    def calcClusterCOM(self):
        for cluster in self.clusters:
            nc = 0
            for idxParticle in cluster:
                if nc==0:
                    com = [self.coords[idxParticle][0][0],self.coords[idxParticle][0][1],self.coords[idxParticle][0][2]]
                    nc += 1
                else:
                    for i in [0,1,2]:
                        if abs(self.coords[idxParticle][0][i] - com[i]/nc)<self.box[i]/2.:
                            com[i] += self.coords[idxParticle][0][i]
                        else:
                            com[i] += com[i] + (self.box[i]-abs(self.coords[idxParticle][0][i] - com[i]/nc))
            for i in [0,1,2]:
                com[i] /= nc
            self.clusterCOM.append(com)
        return

    def calcClusterInertia(self):
        for idxCluster in xrange(len(self.clusters)):
            sum2 = [0.,0.,0.]
            for idxParticle in self.clusters[idxCluster]:
                for i in [0,1,2]:
                    r = abs(self.coords[idxParticle][0][i] - self.clusterCOM[idxCluster][i]/len(self.clusters[idxCluster]))
                    if r>self.box[i]/2.:
                        r = self.box[i]-r
                    sum2[i] += r*r
            for i in [0,1,2]:
                sum2[i] /= len(self.clusters[idxCluster])
            #print sum2
            self.clusterInertia.append(sum2)
        return

    def dfs(self, idx, searchSet):
        # dfs using neighbor list
        idxs = deque([idx])
        while idxs:
            idxOld = idxs.popleft()
            for cell in self.neighborIndex(idxOld):
                # print cell
                for j in self.cells[cell[0]][cell[1]][cell[2]]:
                    if j in searchSet and self.distance2(self.coords[idxOld][0], self.coords[j][0])<self.well2: 
                        self.clusters[-1].add(j)
                        searchSet.remove(j)
                        idxs.append(j)
        return

    def dfsSlow(self, idx, searchSet):
        # brute force DFS
        idxs = deque([idx])
        while idxs:
            idxOld = idxs.popleft()
            for j in xrange(self.n):
                if j in searchSet and self.distance2(self.coords[idxOld][0], self.coords[j][0])<self.well2: 
                    self.clusters[-1].add(j)
                    searchSet.remove(j)
                    idxs.append(j)
        return

    
            
    def averageClusterSize(self, lowerBound=1):
        count, sumN = 0,0
        for cluster in self.clusters:
            if len(cluster)>=lowerBound:
                count += 1
                sumN += len(cluster)
        return float(sumN)/float(count)
    
    def distance(self, r1, r2):
        d2 = 0
        for i in xrange(len(r1)):
            d = min(abs(r1[i]-r2[i]),abs(self.box[i]-abs(r1[i]-r2[i])))
            d2 += d*d
        return math.sqrt(d2)

    def distance2(self, r1, r2):
        d2 = 0.
        for i in xrange(len(r1)):
            d = min(abs(r1[i]-r2[i]),abs(self.box[i]-abs(r1[i]-r2[i])))
            d2 += d*d
        return d2

    
    def getN(self):
        return self.n

    def getNumberOfClusters(self):
        return len(self.cluster)

    def getSizeRaw(self):
        return map(len,self.clusters)

    def getInertiaRaw(self):
        return self.clusterInertia

    def printAll(self):
        print self.coords
        print self.clusters
