import matplotlib.pyplot as  plt
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
    i = 0
    for points in pointsArray:
            xCoor.append(points[0])
            yCoor.append(points[1])
            colors.append(values[i])
            i+=1
            
    plt.scatter(array(xCoor),array(yCoor),c=colors,cmap='bwr')
    plt.show()
    


