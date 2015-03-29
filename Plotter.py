import matplotlib.pyplot as  plt
import matplotlib.colors as col
from PyCamellia import *
from numpy import *
import itertools


def plotError(perCellError, mesh):
    pass

def plotMesh(cellIds, mesh): 
    meshX = []
    meshY = []
    tempCell = []
    #for each active cell
    for cellID in cellIds:
        tempCell = mesh.verticesForCell(cellID)
        #for each separate vertex of the cell
        for vert in tempCell:
           meshX.append(vert[0]) #get the x value for the vertex
           meshY.append(vert[1])
           
    #dummy color values for the plot as to be 0
    colA = zeros((len(meshX)-1, len(meshY)-1))
    meshX = sorted(list(set(meshX))) #sort and remove duplicates 
    meshY = sorted(list(set(meshY))) #sort and remove duplicates
    meshX = around(meshX, decimals = 3) #round all x values to 3 decimal places
    meshY = around(meshY, decimals = 3) #round all y values to 3 decimal places
    #make the actual mesh plot
    plt.pcolormesh(array(meshX), array(meshY), colA, edgecolors='k', linewidths=2, 
                       cmap='bwr', vmin='-100', vmax='100') 

    plt.xticks(meshX) #plot the ticks on the x axis with all x points
    plt.yticks(meshY) #plot the ticks on the y axis with all y points
    plt.xlim(0, meshX[len(meshX)-1]) #limit the x axis to the maximum mesh dimension
    plt.ylim(0, meshY[len(meshY)-1]) #limit the y axis to the minimum mesh dimension
    plt.show() #show the plot
    
    
    
    
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
