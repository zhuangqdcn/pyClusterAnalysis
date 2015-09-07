import Configure
import sys
import shutil
import numpy as np

def time2index(time):
    return time-1

def isSphere(inertia, th_sphere):
    i01 = (inertia[0]-inertia[1])
    i12 = (inertia[1]-inertia[2])
    i02 = (inertia[0]-inertia[2])
    if i01*i01+i12*i12+i02*i02>2.*th_sphere*(inertia[0]*inertia[0]+inertia[1]*inertia[1]+inertia[2]*inertia[2]):
        return False
    else:
        return True

finput = open("Analysis.input","r")
line = finput.readline()
lineSplit = line.split()
temp = float(lineSplit[0])
rho = float(lineSplit[1])
n = int(lineSplit[2])
line = finput.readline()
lineSplit = line.split()
lx,ly,lz = float(lineSplit[0]),float(lineSplit[1]),float(lineSplit[2])
line = finput.readline()
oneFinished = True
finput.close()

timeStart = int(sys.argv[2])
well = float(sys.arg[3])
th_sphere = float(sys.argv[4])
fmovie = open(sys.argv[1],"r")
configurations = []
for lines in fmovie:
    lineSplit = lines.split()
    if len(lineSplit)<4 and len(lineSplit)>0:
        oneFinished = True
        t = int(lineSplit[0])
    elif len(lineSplit)==4:
        if oneFinished==True:
            oneFinished = False
            configurations.append(Configure.Configure(well,(lx,ly,lz)))
            configurations[-1].add(float(lineSplit[1]),float(lineSplit[2]),float(lineSplit[3]))
        else:
            configurations[-1].add(float(lineSplit[1]),float(lineSplit[2]),float(lineSplit[3]))
        if configurations and configurations[-1].getN()==n:
            configurations[-1].finishInput()
            # print "finish", len(configurations)

fmovie.close()

iT = time2index(timeStart)
count, sumN1, sumN2 = 0, 0, 0
sizeDict = {}
sphereDict = {}
nonsphereDict = {}
# print iT,len(configurations)
f_raw_inertia = open("raw_inertia.dat", "w")
f_inertia_sphere = open("sphere_dist.dat", "w")
f_inertia_nonsphere = open("nonsphere_dist.dat", "w")

for i in xrange(iT,len(configurations)):
    count += 1
    rawSize = configurations[i].getSizeRaw()
    rawInertia = configurations[i].getInertiaRaw()
    for idxCluster in xrange(len(rawSize)):
        if rawSize[idxCluster]>3:
            f_raw_inertia.write('%d %f %f %f\n'%(rawSize[idxCluster], rawInertia[idxCluster][0], rawInertia[idxCluster][1], rawInertia[idxCluster][2]))
            if isSphere(rawInertia[idxCluster], th_sphere):
                if rawSize[idxCluster] not in sphereDict:
                    sphereDict[rawSize[idxCluster]] = 1
                else:
                    sphereDict[rawSize[idxCluster]] += 1
            else:
                if rawSize[idxCluster] not in nonsphereDict:
                    nonsphereDict[rawSize[idxCluster]] = 1
                else:
                    nonsphereDict[rawSize[idxCluster]] += 1
    for size in rawSize:
        # if size!=1 and size!=2:
        #     print size
        if size not in sizeDict:
            sizeDict[size] = 1
        else:
            sizeDict[size] += 1
    
res=sorted(sizeDict)
sphereRes = sorted(sphereDict)
nonsphereRes = sorted(nonsphereDict)
for i in res:
    print i, sizeDict[i]
for i in sphereRes:
    f_inertia_sphere.write('%d %d\n' % (i, sphereDict[i]))
for i in nonsphereRes:
    f_inertia_nonsphere.write('%d %d\n' % (i, nonsphereDict[i]))
    
f_raw_inertia.close()
f_inertia_sphere.close()
f_inertia_nonsphere.close()
# print configurations[-1].getSizeRaw()
# print configurations[-2].getSizeRaw()

#configurations[-1].printAll()
    # print count, configurations[i].averageClusterSize(1), sumN1, configurations[i].averageClusterSize(2), sumN2
    

