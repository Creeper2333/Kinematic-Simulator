import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

class data_set():
    name=str()
    data=list()
    def __init__(self,name:str) -> None:
        self.name=name
    def append_data(self,data:float):self.data.append(data)
    def get_len(self):return len(self.data)
    
class graph_manager():
    datasets=dict()
    def __init__(self):
        pass
    def add_dataset(self,name,dataset1:data_set,dataset2:data_set,xlim=(0,50),ylim=(0,50),plotname='graph'):
        if dataset1.get_len() == dataset2.get_len():    
            tmp={name:(dataset1,dataset2,xlim,ylim,plotname)}
            self.datasets.update(tmp)
        else:
            print('bad length')
    def draw(self):
        count=0
        for i in self.datasets:
            ax=plt.subplot(count+1,2,count)
            ax.set_xlim(self.datasets[i][2][0],self.datasets[i][2][1])
            ax.set_ylim(self.datasets[i][3][0],self.datasets[i][3][1])
            plt.plot(self.datasets[i][0].data,self.datasets[i][1].data,'ob')
            plt.title(self.datasets[i][4])
        plt.show


if __name__=='__main__':
    d1=data_set('a')
    d2=data_set('b')
    for i in range(10):
        d1.append_data(i)
    for j in range(10):
        d2.append_data(j)
