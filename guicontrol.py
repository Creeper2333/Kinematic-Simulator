from tkinter import *
import asyncio,threading

CIRCLE_DIAMETER=1
class gui_controller():
    main_wnd=None
    cvs=None

    precision=float()#需要和坐标系的precision对应
    time_scale=float()#需要与animator的time scale对应
    cvs_width=int()
    cvs_height=int()
    use_info_box=True

    zero_point_x=float()
    zero_point_y=float()

    data=[]
    def __init__(self,precision,time_scale,cvs_w=300,cvs_h=300):
        self.main_wnd=Tk()
        self.cvs=Canvas(self.main_wnd,'white')

        self.precision=precision
        self.time_scale=time_scale
        self.cvs_width=cvs_w
        self.cvs_height=cvs_h

        self.zero_point_x=0.5*self.cvs_width
        self.zero_point_y=0.5*self.cvs_height
        
    def recv_data(self,dataset):
        tmp=[]
        for d in dataset:
            tmp.append(dataset[d][0])
        self.data.append(tmp)
        tmp.clear()
    
    async def draw(self):
        for i in self.data:
            for j in i:
                await asyncio.sleep(self.time_scale)
                attr=j.get_attr()
                self.cvs.create_oval(
                    self.zero_point_x+attr['point_x']-CIRCLE_DIAMETER,
                    self.zero_point_y+attr['point_y']-CIRCLE_DIAMETER,
                    self.zero_point_x+attr['point_x']+CIRCLE_DIAMETER,
                    self.zero_point_y+attr['point_y']+CIRCLE_DIAMETER,
                    fill=attr['color']
                    )
    def make_wnd(self):
        #self.main_wnd=Tk()
        self.main_wnd.title('kinematic')
        self.main_wnd.geometry(str(self.cvs_width)+'x'+str(self.cvs_height+100))