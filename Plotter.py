import matplotlib.pyplot as  plt
from PyCamellia import *
from numpy import *




def plot(): #example
    xCoor = [-1,0,1]
    yCoor = [-1,0,1]
    values = random.random_integers(-100, 100, (len(xCoor)-1, len(yCoor)-1))
    #for loc in points:
     #   xCoor.append(loc[0])
      #  yCoor.append(loc[1])
    
    plt.pcolormesh(array(xCoor), array(yCoor), values, cmap='RdBu', vmin=-100, vmax = 100)
    plt.show()

plot()

def plotMesh(points): #fo real
    xCoor = []
    yCoor = []
    for points in pointsArray:
      for point in points:
        xCoor.append(point[0])
        yCoor.append(point[1])
        
    plt.pcolormesh(array(xCoor), array(yCoor), blanks, cmap='bwr', vmin=-100,vmax = 100)
