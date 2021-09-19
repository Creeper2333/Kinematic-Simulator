from guicontrol import gui_controller
from . import coorsys,exception,guicontrol
import time

default_coorsys=coorsys.coordinate_system(precision=0.01,dimension=2)
default_gui_ctrl=gui_controller()

class animator():
    time_precision=float()#表示时间取值的间隔
    time_scale=float()#表示n s对应的单位时间间隔
    
    coordinates=None
    gui_controller=None

    update_flag=False
    disable_time_interval=False
    update_events=[]

    def __init__(self,t_precision,coorsys=default_coorsys,d_t_intrval=False):
        self.time_precision=t_precision
        self.coordinates=coorsys
        self.disable_time_interval=d_t_intrval

    def update(self):
        self.coordinates.update(self.time_precision)
        self.data_transmit(self.coordinates.getobjects())

        for e in self.update_events:
            try:
                e(self)
            except:
                e()
    
    def bind_gui_controller(self,gui_ctrl):
        self.gui_controller=gui_ctrl#绑定一个gui控制器，用来传输数据
    
    def data_transmit(self,data):
        self.gui_controller.recv_data(data)
    
    def start_animation(self):
        self.update_flag=True
        while self.update_flag:
            if not self.disable_time_interval:time.sleep(self.time_scale)
            self.update()

    def stop_animation(self):
        self.update_flag=False
