from manim import *
from dataclasses import dataclass

class test_video(ThreeDScene, MovingCameraScene):
    def construct(self):
        axes = ThreeDAxes(x_max=20, y_max=20, z_max = 20)
        self.set_camera_orientation(phi=140*DEGREES, theta=60*DEGREES, distance = 100)
        obj = solid_of_revolution_object()

        create_slope_list(obj)
        parametrics_group = create_parametrics(obj)
        circle_group = create_circles(obj)

        self.add(axes, circle_group)
        self.wait()

@dataclass
class Info:
    f: str
    upper: int
    lower: int
    interval: int
    starting_x: int
    scale: float

    def fix_datatype(self):
        if type(self.upper) == str:
            self.upper = int(self.upper)
        if type(self.lower) == str:
            self.lower = int(self.lower)
        if type(self.interval) == str:
            self.interval = int(self.interval)
        if type(self.starting_x) == str:
            self.starting_x = int(self.starting_x)
        if type(self.scale) == str:
            self.scale = float(self.scale)
        
        self.real_f = lambda x: eval(self.f)
 
def create_slope_list(obj: Info):
    """
    cannot use @cache because it takes in an object which is unhashable. Speed can double if that works but who cares.
    """
    slope_list = []
    points_list = []
    interval_value = (obj.upper - obj.lower) / obj.interval

    for i in range(obj.interval - 1):
        x1, x2 = i*interval_value + obj.lower, (i+1)*interval_value + obj.lower
        y1, y2 = obj.real_f(x1), obj.real_f(x2)

        rise, run = y1-y2, x1-x2
        m = rise/run
        b = y1 - m*x1 

        slope_list.append([m, b])
        if [x1, y1] not in points_list:
            points_list.append([x1, y1])

        points_list.append([x2, y2])

    setattr(obj, "point_list", points_list)
    setattr(obj, "slope_list", slope_list)  
    return slope_list

def create_parametrics(obj: Info):
    parametrics_list = []

    for index, item in enumerate(obj.slope_list):
        _m = item[0]
        _b = item[1]
        _x_intercept = -_b / _m

        slope = ParametricSurface(lambda u, v: np.array([
        	((u-_b)/_m)*obj.scale + obj.starting_x,
        	u*np.cos(v)*obj.scale,
        	u*np.sin(v)*obj.scale]),
        u_min = ((obj.upper - obj.lower)/obj.interval*index - (_x_intercept-obj.lower)) * _m, u_max = ((obj.upper - obj.lower)/obj.interval*(index+1) - (_x_intercept-obj.lower)) * _m, v_max = 2*PI)
        parametrics_list.append(slope)

    parametrics_group = VGroup(*parametrics_list)
    setattr(obj, "parametrics_group",  parametrics_group)
    return parametrics_group

def create_circles(obj: Info):
    circle_list = []

    for index, item in enumerate(obj.point_list):
        y = item[1]

        c =  ParametricSurface(lambda u, v: np.array([
			((obj.upper-obj.lower)/obj.interval*index*obj.scale) + obj.starting_x,
			y * np.cos(v) * obj.scale,
			y * np.sin(v) * obj.scale]),
		v_max = 2*PI)

        circle_list.append(c)
    
    circle_group = VGroup(*circle_list)
    setattr(obj, "circle_group", circle_group)
    return circle_group

def solid_of_revolution_object():
    f = "-1.33527273*10**-(6)*x**4 - 1.40072727*10**(-4)*x**3 + 2.03945455*10**(-2)*x**2 - 1.45922078*10**(-1)*x + 6.42164502"
    upper = "50"
    lower = "-10"
    interval = "20"
    starting_x = "-3"
    scale = "0.1"

    obj = Info(f = f, upper = upper, lower = lower, interval = interval, starting_x = starting_x, scale = scale)
    obj.fix_datatype()
    return obj
