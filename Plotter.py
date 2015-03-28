import matplotlib.pyplot as  plt
import matplotlib
from PyCamellia import *
from numpy import *




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
    colors = []
    fColors = []
    i = 0
    for cell in pointsArray:
        for points in cell:
        
            xCoor.append(points[0])
            yCoor.append(points[1])

        #print "i: "+str(i)+" is "+str(values[i])

        totalValue = 0
        for val in values[i]:
            totalValue += val

        #if totalValue < 0:
        #    totalValue = -totalValue

        colors.append(totalValue/len(values[i]))
            
        i += 1

    xCoor = sorted(list(set(xCoor)))
    yCoor = sorted(list(set(yCoor)))
    

    print "xCoor: " + str(xCoor)
    print "yCoor: " + str(yCoor)
    print "colors: "+ str(len(colors)) +" "+str(colors)

    print "points per cell: " + str(len(pointsArray[0]))

    n = 0
    for i in range(0, (len(yCoor)-1)):
        fColors.append([])
        for j in range(0, (len(xCoor)-1)): 
            print "i,j: " + str(i) +","+ str(j)
            fColors[i].append(colors[n])
            print "fColors: "+str(fColors)
            n += 1

    xCoor = around(xCoor, decimals = 3) #rounding
    yCoor = around(yCoor, decimals = 3) #rounding
    area = pi * (4) # 0 to 15 point radiuses
            
    #plt.scatter(array(xCoor),array(yCoor),c=colors,cmap='bwr')
    plt.scatter(array(xCoor),array(yCoor),s = area,c = array(fColors),cmap = 'bwr',vmin = '-100', vmax = '100')
    plt.title("Cell Values")
    plt.xticks(xCoor)
    plt.yticks(yCoor)
    plt.xlim(0,xCoor[len(xCoor)-1])
    plt.ylim(0,yCoor[len(yCoor)-1])
    plt.show()
    


