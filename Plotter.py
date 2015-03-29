import matplotlib.pyplot as  plt
import matplotlib.colors as col
from PyCamellia import *
from numpy import *
import itertools

debug = False

def plotError(cellIds,perCellError, mesh, title=""):
    
    xCoor = []
    yCoor = []
    currentCell = []
    errorVals = []
    #Runs through the activecellid's getting the current cell's vertices and adding the correct points to the two arrays
    for cellID in cellIds:
        currentCell = mesh.verticesForCell(cellID)
        for vert in currentCell:
           xCoor.append(vert[0]) 
           yCoor.append(vert[1])
    #Runs through the percellerror array and creates a two-dimensional array out of the given values      
    for i in range(0,len(yCoor)-1):       
        errorVals.append((array(perCellError)[0:len(xCoor)-1]).tolist())
    print(errorVals)
    #Sorts the given lists and removes the duplicates
    xCoor = sorted(list(set(xCoor))) 
    yCoor = sorted(list(set(yCoor))) 
    #Rounds the x and y vals to 3 places
    xCoor = around(xCoor, decimals = 3) 
    yCoor = around(yCoor, decimals = 3) 
    # Creates a pcolormesh using the two coor arrays and the errorvals
    plt.pcolormesh(array(xCoor), array(yCoor), array(errorVals), edgecolors='k', linewidths=2, cmap='bwr', vmin='-100', vmax='100') 

    plt.xticks(xCoor) 
    plt.yticks(yCoor) 
    plt.xlim(0, xCoor[len(xCoor)-1]) 
    plt.ylim(0, yCoor[len(yCoor)-1]) 
    plt.title(title)
    plt.colorbar()
    plt.show() 
    

def plotMesh(cellIds, mesh,title=""): 
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
    print(colA)
    plt.pcolormesh(array(meshX), array(meshY), colA, edgecolors='k', linewidths=2, 
                       cmap='bwr', vmin='-100', vmax='100') 

    plt.xticks(meshX) #plot the ticks on the x axis with all x points
    plt.yticks(meshY) #plot the ticks on the y axis with all y points
    plt.xlim(0, meshX[len(meshX)-1]) #limit the x axis to the maximum mesh dimension
    plt.ylim(0, meshY[len(meshY)-1]) #limit the y axis to the minimum mesh dimension
    plt.title(title)
    plt.colorbar()
    plt.show() #show the plot
    
    
    
    
def plot(values,pointsArray, title=""):
    # Creates the x and y coor arrays that will hold the xy coordinates to plot
    xCoor = []
    yCoor = []
    # Turns the pargument into a usable list
    mergedVals = list(itertools.chain.from_iterable(values))
    # Runs through the list of lists and puts the first coor from each list and puts it into the xCoor array
    # Similarily but with the second coor for the yCoor array
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

    #Makes a hexbin plot with the x and y coor with a cmap. Adds on the title given. It then shows plot, revealing it from 
    #the command line.
    plt.hexbin(xCoor,yCoor,mergedVals,cmap='bwr', vmin=min(mergedVals),vmax=max(mergedVals),mincnt=0)
    plt.title(title)
    plt.colorbar()
    plt.show()
