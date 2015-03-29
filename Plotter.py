import matplotlib.pyplot as  plt
import matplotlib.colors as col
from PyCamellia import *
from numpy import *
import itertools

debug = False


def plotMesh(pointsArray): #fo real
    mesh = self.form.solution().mesh()
    refCellVertexPoints = [[-1.,-1.],[1.,-1.],[1.,1.],[-1.,1.]] #update these based on the size
    aCIDs = mesh.getActiveCellIDs()
    xCoor = []
    yCoor = []
    for points in pointsArray:
        for point in points:
            xCoor.append(point[0])
            yCoor.append(point[1])
        
    plt.pcolormesh(array(xCoor), array(yCoor), blanks, cmap='bwr', vmin=-100,vmax = 100)
    
    
    
def plot(values,pointsArray):
    xCoor = []
    yCoor = []
    mergedVals = list(itertools.chain.from_iterable(values))
    for points in pointsArray:
        for point in points:
            xCoor.append(point[0])
            yCoor.append(point[1])
    
    i = 0

    if debug:
        for i,c in enumerate(mergedVals):        
            print "("+str(xCoor[i])+","+str(yCoor[i])+") : "+str(mergedVals[i])
        print i
        print len(xCoor)
        print len(yCoor)

    plt.scatter(array(xCoor),array(yCoor),array(mergedVals),cmap='bwr', vmin=-100,vmax=100)
    plt.show()
    


