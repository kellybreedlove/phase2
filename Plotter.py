
import matplotlib.pyplot as  plt
import matplotlib.colors as col
from PyCamellia import *
from numpy import *
import itertools




def plotMesh(pointsArray): 
    mesh = self.form.solution().mesh()
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
     
    plt.hexbin(xCoor,yCoor,mergedVals,cmap='bwr', vmin=min(mergedVals),vmax=max(mergedVals),mincnt=0)
    
    plt.show()
