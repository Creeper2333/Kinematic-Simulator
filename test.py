import guicontrol
from animator import animator
from coorsys import coordinate_system, mass_point


def terminate(self):
    self.output_info('t='+str(self.absolute_time)+': '+str(self.coordinates.get_objects()['A'][0].point_x)+' '+
        str(self.coordinates.get_objects()['A'][0].point_y)+'\n')
    if self.coordinates.get_objects()['A'][0].point_y<=0:
        self.stop_animation()

test_coorsys=coordinate_system(precision=0.01)
test_object=mass_point('A',color='red',x=0,y=200)

test_object.set_velocity_with_value(10,0)
test_object.set_acceleration(0,-10)

test_coorsys.add_object('A',test_object,False)

test_animator=animator(0.01,test_coorsys,True)
test_guictrl=guicontrol.gui_controller(1,0.1,cvs_w=500,cvs_h=500,info_box_width=500)
test_guictrl.override_set_zero_point(250,470)

test_animator.bind_gui_controller(test_guictrl)
test_animator.update_events.append(terminate)

test_animator.start_animation()