import exception,coorsys
import math

class coordinate_system():
    precision=float() #单位长度，实际的精度是由动画器里设置的Δt决定
    dimension=2
    objects={}
    update_events=[] #用户自定义事件

    def __init__(self,precision=0.1,dimension=2):
        self.precision=abs(precision)
        if dimension<=2 and dimension>0:
            self.dimension=dimension
        else:raise(exception.UnsupportedDimension())

    def add_object(self,name,object_type,is_static=False):
        dic={name:(object_type,is_static)}
        self.objects.update(dic)
    
    def rm_object(self,object_name):
        self.objects.pop(object_name)

    def set_static(self,object_name,is_static=False):
        object_type=self.objects.get(object_name)[0]
        dic={object_name:(object_type,is_static)}
        self.objects.update(dic)
    
    def get_attr(self):
        return(
            {
                'precision':self.precision,
                'dimension':self.dimension,
            }
        )
    
    def get_objects(self):
        return self.objects
    
    def add_customized_event(self,event):
        self.update_events.append(event) #备注：event是一个函数，可以带参数，用于接收传入的self
    
    def rm_customized_event(self,event):
        self.update_events.remove(event)
    
    def update(self,deltatime):
        for obj in self.objects:
            if not self.objects[obj][1]:
                self.objects[obj][0].update(deltatime)
        for e in self.update_events:
            try:
                e(self) #用户自定义函数必须带有至少一个参数用于接收这个self
            except:
                e()

class mass_point():
    name=str()
    mass=float()
    color=str()

    point_x=float()
    point_y=float()
    velocity_x=float()
    velocity_y=float()
    acceleration_x=float()
    acceleration_y=float()

    update_events=[]
    
    def __init__(self,name:str,mass=1,color='#0x000000',x=0,y=0):
        self.name=name
        self.mass=mass
        self.color=color
        self.point_x=x
        self.point_y=y

    def get_attr(self):
        return(
            {
                'name':self.name,
                'mass':self.mass,
                'color':self.color,
                'point_x':self.point_x,
                'point_y':self.point_y
            }
        )

    def set_velocity_with_value(self,initial_velocity_x=0,initial_velocity_y=0):
        self.velocity_x=initial_velocity_x
        self.velocity_y=initial_velocity_y

    def set_velocity_with_vector(self,velocity=0,vector=0):
        velocity=abs(velocity)
        quadrant=(vector-(vector%90))/90+1 #求象限，其中0度为一象限，90度为二象限，以此类推
        angle=vector%90 #在象限内的角度
        rad=angle*math.pi/180 #只能先转弧度制，又要损失精度，淦

        if vector==0:
            if quadrant==1:
                self.velocity_y=velocity
                self.velocity_x=0 #方向沿y轴时
            if quadrant==3:
                self.velocity_y=-velocity
                self.velocity_x=0
            
            if quadrant==2:
                self.velocity_x=velocity
                self.velocity_y=0 #方向沿x轴时
            if quadrant==4:
                self.velocity_x=-velocity
                self.velocity_y=0

        else:
            if quadrant==1:
                velocity_x=velocity*math.sin(rad)
                velocity_y=velocity*math.cos(rad)
            if quadrant==2:
                velocity_x=velocity*math.sin(rad)
                velocity_y=-(velocity*math.cos(rad))
            if quadrant==3:
                velocity_x=-(velocity*math.sin(rad))
                velocity_y=-(velocity*math.cos(rad))
            if quadrant==4:
                velocity_x=-(velocity*math.sin(rad))
                velocity_y=velocity*math.cos(rad)
            self.velocity_x=velocity_x
            self.velocity_y=velocity_y
    
    def set_acceleration(self,acc_x,acc_y):
        self.acceleration_x=acc_x
        self.acceleration_y=acc_y

    def update(self,deltatime):
        original_velocity_x=self.velocity_x
        original_velocity_y=self.velocity_y
        self.velocity_x+=deltatime*self.acceleration_x+original_velocity_x
        self.velocity_y+=deltatime*self.acceleration_y+original_velocity_y

        delta_x=original_velocity_x*deltatime+0.5*self.acceleration_x*deltatime**2 #使用匀加速位移公式
        delta_y=original_velocity_y*deltatime+0.5*self.acceleration_y*deltatime**2

        self.point_x+=delta_x
        self.point_y+=delta_y

        for e in self.update_events:
            try:
                e(self) #同上
            except:
                e()
