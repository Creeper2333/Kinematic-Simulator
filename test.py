import guicontrol
from animator import animator
from coorsys import coordinate_system, mass_point


def terminate(self):
    if self.coordinates.get_objects()['A'][0].point_y<=0:
        self.stop_animation()

test_coorsys=coordinate_system(precision=0.01)
test_object=mass_point('A',color='red',x=0,y=25)

test_object.set_velocity_with_value(0,0)
test_object.set_acceleration(0,-10)

test_coorsys.add_object('A',test_object,False)

test_animator=animator(0.1,test_coorsys,True)
test_guictrl=guicontrol.gui_controller(10,0.1,cvs_w=1000,cvs_h=1000)

test_animator.bind_gui_controller(test_guictrl)
test_animator.update_events.append(terminate)

test_animator.start_animation()