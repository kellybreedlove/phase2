#So I believe for Plotting what we need to do is have the parsing be done for each possible choice outside of the 
plotting functions. We need to handle Error and mesh plotting differently from the other functions(u1,u2, stream 
function and p). For error, we need to pass in the perCellError. For mesh we need to pass in the ?number of elements?
not sure on that one. For the functions though we need to pass in the values and points after they have been computed
from the function solution. See bottom of refcellpoints for example






from PyCamellia import *
from matplotlib import *


def plotError(perCellError):
  

def plot(values, points):
  
  
def plotMesh():
