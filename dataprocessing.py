import matplotlib
import matplotlib.pyplot as plt
import numpy as np

x=np.arange(0,100,2)
y=2*x+1
matplotlib.rcParams['toolbar']='None'
plt.plot(x,y)

plt.show()