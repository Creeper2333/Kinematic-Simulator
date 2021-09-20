from asyncio.tasks import run_coroutine_threadsafe
import time
from tkinter import *
import asyncio,threading
from copy import deepcopy
import tkinter

CIRCLE_DIAMETER=1
class gui_controller():
    main_wnd=None
    cvs=None
    start_btn=None
    clear_btn=None
    save_btn=None
    info_box=None
    scroll_bar=None

    infobox_tmp=[]

    precision=float() #需要和坐标系的precision对应
    time_scale=float() #需要与animator的time scale对应
    time_precision=float() #需要与animator的time precision 对应
    absolute_time=0
    cvs_width=int()
    cvs_height=int()
    info_box_width=True

    zero_point_x=float()
    zero_point_y=float()

    data=[]
    def __init__(self,precision,time_scale,cvs_w=300,cvs_h=300,info_box_width=300):

        self.precision=precision
        self.time_scale=time_scale
        self.cvs_width=cvs_w
        self.cvs_height=cvs_h
        self.info_box_width=info_box_width

        self.zero_point_x=0.5*self.cvs_width
        self.zero_point_y=0.5*self.cvs_height
        
    def recv_data(self,dataset):
        tmp=dict()
        for d in dataset:
            tmp.update({d:dataset[d][0]})
        self.data.append(tmp)
        #tmp={}
        #tmp.clear()
    
    async def draw(self):
        count=0            
        for i in self.data:
            await asyncio.sleep(self.time_scale)
            for j in i:
                attr=i[j].get_attr()
                if len(self.data)>count+1:
                    attr2=self.data[count+1][i[j].get_attr()['name']].get_attr()
                else:attr2=deepcopy(attr)
                self.cvs.create_line(
                    self.zero_point_x+attr['point_x']*self.precision,
                    self.zero_point_y-attr['point_y']*self.precision,
                    self.zero_point_x+attr2['point_x']*self.precision,
                    self.zero_point_y-attr2['point_y']*self.precision,
                    fill=attr['color'],
                    tags=('line')
                    )
                
                count+=1

            self.absolute_time+=self.precision
            
    def draw_new(self):
        count=0            
        for i in self.data:
            for j in i:
                attr=i[j].get_attr()
                if len(self.data)>count+1:
                    attr2=self.data[count+1][i[j].get_attr()['name']].get_attr()
                else:attr2=deepcopy(attr)
                self.cvs.create_line(
                    self.zero_point_x+attr['point_x']*self.precision,
                    self.zero_point_y-attr['point_y']*self.precision,
                    self.zero_point_x+attr2['point_x']*self.precision,
                    self.zero_point_y-attr2['point_y']*self.precision,
                    fill=attr['color'],
                    #arrow='last',arrowshape=(5,5,5),
                    tags=('line')
                    )
                #print(attr['point_x'],attr['point_y'],attr2['point_x'],attr2['point_y'],count)
                #self.cvs.create_line(100,100,200,200)
                count+=1

        #self.cvs.create_line(100,100,200,200)
            self.absolute_time+=self.precision
    def override_set_zero_point(self,zp_x,zp_y):
        self.zero_point_x=zp_x
        self.zero_point_y=zp_y
    
    def make_coordinate_sys(self):
         #画x轴
        self.cvs.create_line(
            0,self.zero_point_y,
            self.cvs_width,
            self.zero_point_y,
        arrow='last',arrowshape=(10,10,10)
        )

        self.cvs.create_text(
            self.cvs_width-15,
            self.zero_point_y-10,
            text='x'
        )
         #画y轴
        self.cvs.create_line(
            self.zero_point_x,
            self.cvs_height,
            self.zero_point_x,0,
            arrow='last',arrowshape=(10,10,10)
        )
        self.cvs.create_text(
            self.zero_point_x-10,
            10,
            text='y'
        )
    
    def make_wnd(self):
         #self.main_wnd=Tk()
        self.main_wnd=Tk()
        self.cvs=Canvas(self.main_wnd,background='white')
        self.start_btn=Button(self.main_wnd,text='start',command=self.draw_new)
        self.clear_btn=Button(self.main_wnd,text='clear',command=self.clear_graph)
        self.save_btn=Button(self.main_wnd,text='save',command=self.save_records)
        self.info_box=Text(self.main_wnd,background='white')
        self.scroll_bar=Scrollbar()

        self.main_wnd.title('kinematic')
        self.main_wnd.geometry(str(self.cvs_width)+'x'+str(self.cvs_height))
        
        #self.cvs.grid(line=0,column=0)
        self.cvs.pack(fill='both')
        self.cvs.place(width=self.cvs_width,height=self.cvs_height)
        self.start_btn.pack()
        self.start_btn.place(x=0,y=0)
        self.clear_btn.place(x=50,y=0)
        self.save_btn.place(x=100,y=0)
        self.info_box.place(x=self.cvs_width,y=0,width=self.info_box_width,height=self.cvs_height)

        self.scroll_bar.place(
            x=self.cvs_width+self.info_box_width,
            y=0,
            height=self.cvs_height
        )
        self.scroll_bar.config(command=self.info_box.yview)
        self.info_box.config(yscrollcommand=self.scroll_bar.set)

        self.make_info()
        self.info_box['state']='disabled'
        self.make_coordinate_sys()

        self.main_wnd.mainloop()
    
    def output_info_box(self,info):
        self.infobox_tmp+=info
        #self.info_box['text']=self.info_box['text']+info+'\n'
    
    def make_info(self):
        for info in self.infobox_tmp:
            self.info_box.insert('end',info)
    
    def clear_graph(self):
        self.cvs.delete('line')

    def save_records(self):
        rec=self.info_box.get('1.0','end')
        with open('rec_'+time.strftime('%Y-%m-%d-%H-%M-%S')+'.txt','w') as f:
            f.write(rec) 
            f.close()
    
    def mk_loop(self,loop):
        self.my_loop=loop
        asyncio.set_event_loop(self.my_loop)
        self.my_loop.run_forever()
    
    def loop_ctrl(self):
        co=self.draw()
        _loop=asyncio.new_event_loop()
        thread=threading.Thread(target=self.mk_loop,args=(_loop,))
        thread.start()
        asyncio.run_coroutine_threadsafe(co,_loop)