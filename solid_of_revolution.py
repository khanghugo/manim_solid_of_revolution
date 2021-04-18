from manim import *
from functools import cache

class test_video(ThreeDScene, MovingCameraScene):
    def construct(self):
        axes = ThreeDAxes(x_max=20, y_max=20, z_max = 20)
        self.set_camera_orientation(phi=140*DEGREES, theta=60*DEGREES, distance = 100)

        f = "-1.33527273*10**-(6)*x**4 - 1.40072727*10**(-4)*x**3 + 2.03945455*10**(-2)*x**2 - 1.45922078*10**(-1)*x + 6.42164502"
        upper = "50"
        lower = "-10"
        interval = "20"
        starting_x = "-3"
        scale = "0.1"

        obj = MANIMRevolvingSolid(f = f, upper = upper, lower = lower, interval = interval, starting_x = starting_x, scale = scale)
        parametrics_group = obj.create_parametrics()
        # create_slope_list(obj)
        # parametrics_group = create_parametrics(obj)
        # circle_group = create_circles(obj)

        self.add(axes, parametrics_group)
        self.wait()


class MANIMRevolvingSolid:
    def __init__(self, f, upper, lower, interval, starting_x, scale):
        self.f = f
        self.upper = upper
        self.lower = lower
        self.interval = interval
        self.starting_x = starting_x
        self.scale = scale

        self.slope_list = []
        self.point_list = []

        self.circle_group = []
        self.parametrics_group = []

        self.fix_datatype()
        self.create_slope_list()

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

    @cache
    def create_slope_list(self):
        """
        cannot use @cache because it takes in an object which is unhashable. Speed can double if that works but who cares.
        """
        slope_list = []
        points_list = []
        interval_value = (self.upper - self.lower) / self.interval

        for i in range(self.interval - 1):
            x1, x2 = i*interval_value + self.lower, (i+1)*interval_value + self.lower
            y1, y2 = self.real_f(x1), self.real_f(x2)

            rise, run = y1-y2, x1-x2
            m = rise/run
            b = y1 - m*x1 

            slope_list.append([m, b])
            if [x1, y1] not in points_list:
                points_list.append([x1, y1])

            points_list.append([x2, y2])

        self.point_list = points_list
        self.slope_list = slope_list
        return slope_list

    def create_parametrics(self):
        parametrics_list = []

        for index, item in enumerate(self.slope_list):
            _m = item[0]
            _b = item[1]
            _x_intercept = -_b / _m

            slope = ParametricSurface(lambda u, v: np.array([
                ((u-_b)/_m)*self.scale + self.starting_x,
                u*np.cos(v)*self.scale,
                u*np.sin(v)*self.scale]),
            u_min = ((self.upper - self.lower)/self.interval*index - (_x_intercept-self.lower)) * _m, u_max = ((self.upper - self.lower)/self.interval*(index+1) - (_x_intercept-self.lower)) * _m, v_max = 2*PI)
            parametrics_list.append(slope)

        parametrics_group = VGroup(*parametrics_list)
        self.parametrics_group = parametrics_group
        return parametrics_group

    def create_circles(self):
        circle_list = []

        for index, item in enumerate(self.point_list):
            y = item[1]

            c =  ParametricSurface(lambda u, v: np.array([
                ((self.upper-self.lower)/self.interval*index*self.scale) + self.starting_x,
                y * np.cos(v) * self.scale,
                y * np.sin(v) * self.scale]),
            v_max = 2*PI)

            circle_list.append(c)
        
        circle_group = VGroup(*circle_list)
        self.circle_group = circle_group
        return circle_group

# def solid_of_revolution_object():
#     f = "-1.33527273*10**-(6)*x**4 - 1.40072727*10**(-4)*x**3 + 2.03945455*10**(-2)*x**2 - 1.45922078*10**(-1)*x + 6.42164502"
#     upper = "50"
#     lower = "-10"
#     interval = "20"
#     starting_x = "-3"
#     scale = "0.1"

#     obj = Info(f = f, upper = upper, lower = lower, interval = interval, starting_x = starting_x, scale = scale)
#     obj.fix_datatype()
#     return obj
