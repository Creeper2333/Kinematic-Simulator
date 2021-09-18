from . import coorsys,exception
default_coorsys=coorsys.coordinate_system(precision=0.01,dimension=2)
class animator():
    time_precision=float()
    coordinates=None

    update_flag=False
    update_events=[]

    def __init__(self,t_precision,coorsys=default_coorsys):
        self.time_precision=t_precision
        self.coordinates=coorsys

    def update(self):
        self.coordinates.update(self.time_precision)
        for e in self.update_events:
            e(self)

    def start_animation(self):
        self.update_flag=True
        while self.update_flag:
            self.update()

    def stop_animation(self):
        self.update_flag=False
