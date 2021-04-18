from manim import *
import math

class FunnyVideo(ThreeDScene, MovingCameraScene):
	def construct(self):
		# predefined stuff
		#theta = side
 		#phi = vertical
		self.CIRCLE_DIAMETERS = [12.6, 14.0, 16.8, 25.2, 36.4, 42.0, 48.8]
		self.WIDTH = 50
		self.SCALE = 0.1
		self.POINTS = 7
		self.INTERVALS = self.POINTS - 1
		self.STARTING_POINT = -3

		axes = ThreeDAxes(x_max=20, y_max=20, z_max = 20)
		self.set_camera_orientation(phi=140*DEGREES, theta=60*DEGREES, distance = 100)
		# self.set_camera_orientation(distance = 100)
		# self.add(axes)

		# dont touch, already overengineered
		line_list = [self.return_a_vertical_line(self.WIDTH/self.INTERVALS*index*self.SCALE, diameter/2*self.SCALE, 0) for index, diameter in zip(range(self.POINTS), self.CIRCLE_DIAMETERS)]
		line_group = VGroup(*line_list)

		circle_list = [self.return_a_circle(diameter*self.SCALE, self.WIDTH/self.INTERVALS*index*self.SCALE) for index, diameter in enumerate(self.CIRCLE_DIAMETERS)]
		circle_group = VGroup(*circle_list)

		slope_value_list = [[0.01353246785069448, 6.42164502], [0.2842597414270834, 4.165584406863426], [0.46880519687847233, 1.0898268160069424], [0.5486233796215276, -0.9056277525694405], [0.5051688350729164, 0.5428570657175982], [0.3198961086493062, 8.262554000034694]]
		# slope_value_list_mock = slope_value_list
		slope_group = self.return_the_graph_from_slopes(slope_value_list, self.SCALE)
		parametrics_group = self.return_the_parametrics_from_slopes(slope_value_list, self.SCALE)
		# parametrics_group_mock = self.return_the_parametrics_from_slopes_mock(slope_value_list_mock, self.SCALE)
		"""
		directions:
		axes drawing
		liens drawing
		axes disappearing
		lines spinning
		circles drawing
		lines disappear
		curve making solid
		circles disappear

		"""
		# self.play(Create(axes))
		# self.wait(0.5)
		# self.play(Create(line_group), Uncreate(axes))
		# self.wait()
		# self.play(ro)

		self.play(Create(axes))
		self.wait()
		self.play(Create(line_group), Uncreate(axes))
		self.wait()
		self.play(Rotating(line_group, axis=np.array([1., 0., 0.]), run_time=0.7, radian=4*PI), Create(circle_group))
		self.wait()
		self.play(Create(parametrics_group), Uncreate(circle_group), Uncreate(line_group))
		self.wait()


	def return_a_vertical_line(self, x_value, y_max, starting_place):
			# return FunctionGraph(lambda u: x_value + starting_place, x_min = -radius_, x_max = radius_)
		return ParametricSurface(lambda u, v: np.array([
			x_value+self.STARTING_POINT,
			u,
			0]),
		u_max = y_max
		)

	def return_a_circle(self, diameter, distance_between):
		return ParametricSurface(lambda u, v: np.array([
			distance_between + self.STARTING_POINT,
			diameter/2 * np.cos(v),
			diameter/2 * np.sin(v)]),
		v_max = 2*PI, stroke_width = 3, fill_color = "#FF0000", stroke_color = "#FF0000")

	def return_the_graph_from_slopes(self, list_la: "list of slopes with b-value included", scale=1):
		bigger_group = []

		for index, item in enumerate(list_la):
			slope = ParametricSurface(lambda u, v: np.array([
				u*scale,
				(item[0]*u+item[1])*scale+self.STARTING_POINT,
				0]),
			u_min = (index*self.WIDTH/self.INTERVALS), u_max = ((index+1)*self.WIDTH/self.INTERVALS))
			bigger_group.append(slope)

		return VGroup(*bigger_group)

	def return_the_parametrics_from_slopes(self, list_la: "list of slopes with b-value included", scale=1):
		bigger_group = []

		for index, item in enumerate(list_la):
			x_int = -item[1] / item[0]
			ratio_of_increment = abs(x_int/item[1])

			slope = ParametricSurface(lambda u, v: np.array([
				((u-item[1])/item[0])*scale+self.STARTING_POINT,
				u*np.cos(v)*scale,
				u*np.sin(v)*scale]),
			u_min = (self.WIDTH/self.INTERVALS*index-(x_int))/ratio_of_increment, u_max = (self.WIDTH/self.INTERVALS*(index+1)-(x_int))/ratio_of_increment, v_max = 2*PI)

			bigger_group.append(slope)

		return VGroup(*bigger_group)

	def return_the_parametrics_from_slopes_mock(self, list_la: "list of slopes with b-value included", scale=1):
		bigger_group = []
		# first slope: [0.01353246785069448, 6.42164502], x_intercept = -474.536
		# second slope: [0.2842597414270834, 4.165584406863426], x_int = -14.654

		for index, item in enumerate(list_la):
			"""
			x-intercept is where u=0
			by finding where x intercept is, we can
			find u min and max for the cone.

			x-intercept = b
			u_min = b means it will start at origin
			
			for the first point, b+50/6 will go over the x=50 line, b+50/6/7 still go over it, 50/6/7 = 1.190, b/6 still goes over it.

			b*unknown = 50, still not quite
			it has something to do with x-intercept

			everu increment of times of b, x increases by x_int of the graph. 
			ex: min, max = 0, b; x ranges from x_int to x_int+|x_int|
			ex: x_int = -14, b = 4.1. min, max = 0, 4.1 then the graph will range from x_int to x_int+|-14|, which is 0
			ex: min, max = 0, 2*4.1 (2*b) then the graph will range from x_int to x_int + |-14*2|

			ratio of increasing = 4.1/|-14| = 0.29 means as x increases by 1, b increases by 0.29

			for the second slope: 0.2842626181836649 b per x
			3.517873740802212 x per b
			since x_int = -14.654, to get x starts at 0, take |0-x_int|/3.517873740802212 = 4.16, which is b value and this wil work
			to get it starts at 50/6, take |50/6-x_int|/the_number

			hypothesis is correct
			"""
			x_int = -item[1] / item[0]
			ratio_of_increment = abs(x_int/item[1])

			slope = ParametricSurface(lambda u, v: np.array([
				((u-item[1])/item[0])*scale+self.STARTING_POINT,
				u*np.cos(v)*scale,
				u*np.sin(v)*scale]),
			u_min = (self.WIDTH/self.INTERVALS*index-(x_int))/ratio_of_increment, u_max = (self.WIDTH/self.INTERVALS*(index+1)-(x_int))/ratio_of_increment, v_max = 2*PI)
			bigger_group.append(slope)

		return VGroup(*bigger_group)

	def return_the_infinite_cone(self, in_wow):
		return ParametricSurface(lambda u, v: np.array([
			eval(in_wow),
			u*np.sin(v),
			u*np.cos(v)]),
		v_max = 2*PI, u_max = 10)















# class FunnyStuff(ThreeDScene, MovingCameraScene):
# 	def construct(self):
# 		self.circle_diameters = [12.6, 14.0, 16.8, 25.2, 36.4, 42.0, 48.8]
# 		self.width_difference = 50
# 		self.overall_height = 0
# 		self.starting_place = -3
# 		self.the_scale = 0.1

# 		self.max_len = len(self.circle_diameters)

# 		axes = ThreeDAxes(x_max=100, y_max=100, z_max=100)
# 		#theta = side
# 		#phi = vertical
# 		# self.set_camera_orientation(phi=75*DEGREES, theta=60*DEGREES, distance = 100)
# 		self.set_camera_orientation(phi=75*DEGREES, theta=10*DEGREES, distance = 100)
# 		# self.set_camera_orientation(distance = 30)

# 		list_of_slopes = [[0.01353246785069448, 6.42164502], [0.2842597414270834, 4.165584406863426], [0.46880519687847233, 1.0898268160069424], [0.5486233796215276, -0.9056277525694405], [0.5051688350729164, 0.5428570657175982], [0.3198961086493062, 8.262554000034694]]


# 		list_of_lines = [self.return_a_vertical_line(self.max_len/(self.width_difference*self.the_scale)*index, item*self.the_scale/2, self.starting_place) for index, item in enumerate(self.circle_diameters)]
# 		list_of_circles = [self.return_a_circle(item*self.the_scale, self.max_len/(self.width_difference*self.the_scale)*index, self.overall_height, self.starting_place) for index, item in enumerate(self.circle_diameters)]
# 		circle_group = VGroup(*list_of_circles)
# 		line_group = VGroup(*list_of_lines)
# 		circle_group.generate_target()
# 		line_group.generate_target()

# 		circle_group.target.shift(3*DOWN)
# 		line_group.target.shift(3*DOWN)

# 		# mock_line = self.return_a_vertical_line(0, 2)
# 		# mock_line.generate_target()
# 		# mock_line.target.shift(2*DOWN)

# 		# mock_para_sur = ParametricSurface(lambda u, v: np.array([
# 		# 	3,
# 		# 	u,
# 		# 	0]),
# 		# u_max = 5)

# 		# self.add(mock_line)
# 		# self.play(MoveToTarget(mock_line))
# 		"""
# 		directions:
# 		axes drawing
# 		liens drawing
# 		lines spinning
# 		circles drawing
# 		lines disappear
# 		curve making solid
# 		circles disappear

# 		"""
# 		# the_damn_graph = self.return_the_solid_graph()
# 		# the_damn_graph.generate_target()
# 		# the_damn_graph.target.shift(100*DOWN)
# 		# self.add(axes, self.return_the_graph_from_slopes(list_of_slopes))
# 		# self.add(axes, self.return_the_slope(), line_group)
# 		self.add(axes, line_group, self.return_the_slope())

# 		self.wait()
# 		# self.play(MoveToTarget(the_damn_graph))
# 		# self.move_camera(phi=70*DEGREES, theta=80*DEGREES, distance = 1000)


# 		# self.play(Create(line_group))
# 		# self.play(Rotating(line_group, axis=np.array([0., 1., 0.]), run_time=0.7, radians=4*PI), Create(circle_group))
# 		# self.play(MoveToTarget(line_group), MoveToTarget(circle_group))
# 		# self.wait()
# 		# self.move_camera(phi=70*DEGREES, theta=80*DEGREES, distance = 100, frame_center = [2, 2 ,0])
# 		# self.wait()
# 	# def return_the_graph(self):
# 	# 	return FunctionGraph(lambda u: (-1.33527273e-06*u**4 - 1.40072727e-04*u**3 + 2.03945455e-02*u**2 - 1.45922078e-01*u + 6.42164502e+00)*self.the_scale, x_max = 50, y_max =50)

# 	def return_the_solid_graph(self):
# 		return ParametricSurface(lambda u, v: np.array([
# 			u*np.sin(v),
# 			u*np.cos(v),
# 			math.sqrt(u)]),
# 		u_min=0, u_max=5, v_max = 2*PI)

# 	def return_a_vertical_line(self, x_value, radius_, starting_place):
# 		# return FunctionGraph(lambda u: x_value + starting_place, x_min = -radius_, x_max = radius_)
# 		return ParametricSurface(lambda u, v: np.array([
# 			radius_,
# 			u,
# 			0]),
# 		u_max = 10
# 		)

# 	def return_a_circle(self, diameter, distance_between, overall_height, starting_place):
# 		return ParametricSurface(lambda u, v: np.array([
# 			diameter/2 * np.cos(v),
# 			distance_between + starting_place,
# 			diameter/2 * np.sin(v) + overall_height]),
# 		v_max = 2*PI, stroke_width = 3, fill_color = "#FF0000", stroke_color = "#FF0000")

# 	def return_the_slope(self):
# 		return ParametricSurface(lambda u, v: np.array([
# 			u*self.the_scale,
# 			(-1.33527273*10**-(6)*u**4 - 1.40072727*10**(-4)*u**3 + 2.03945455*10**(-2)*u**2 - 1.45922078*10**(-1)*u + 6.42164502)*self.the_scale,
# 			0]),
# 			u_max = 50)

# 	def return_the_graph_from_slopes(self, list_la: "list of slopes with b-value included"):
# 		bigger_group = []

# 		for index, item in enumerate(list_la):
# 			slope = ParametricSurface(lambda u, v: np.array([
# 				0,
# 				item[0]*u+item[1],
# 				u*self.the_scale]),
# 			u_max = 5
# 			)
# 			bigger_group.append(slope)

# 		return VGroup(*bigger_group)


# def aux_stuff(): 
# 	circle_diameters = [12.6, 14.0, 16.8, 25.2, 36.4, 42.0, 48.8]

# 	def find_slope(a: "coordinates as list", b):
# 		"""
# 		y = mx+b
# 		m = slope = rise/run = diff(y1, y2)/diff(x1, x2)
# 		b = y1 - m*x1
# 		"""
# 		rise = abs(a[1] - b[1])
# 		run = abs(a[0] - b[0])
# 		m = rise/run
# 		b = a[1] - m*a[0]
	
# 		return [m, b]
	
# 	def the_slope_itself():
# 			return lambda u: [u, -1.33527273*10**-(6)*u**4 - 1.40072727*10**(-4)*u**3 + 2.03945455*10**(-2)*u**2 - 1.45922078*10**(-1)*u + 6.42164502]
	
# 	graphs = [find_slope(the_slope_itself()(50/6*i), the_slope_itself()(50/6*(i+1))) for i in range(len(circle_diameters)-1)]
	# print(graphs)
	# list_of_slopes = [[0.01353246785069448, 6.42164502], [0.2842597414270834, 4.165584406863426], [0.46880519687847233, 1.0898268160069424], [0.5486233796215276, -0.9056277525694405], [0.5051688350729164, 0.5428570657175982], [0.3198961086493062, 8.262554000034694]]

	# for index, item in list_of_slopes:
		# print(index)

# aux_stuff()



























# print(find_slope([0,5], [-5/3, 0]))
# class CameraStuff(MovingCameraScene):
# 	def construct(self):
# 		self.play(self.camera_frame.set_width)
# 		self.wait()

"""
u = 1/2*math.sqrt((1.50442*10**-56*(66374099732508548114477252552207192984521377098785011542261760*u + 1042724643209576631358295931525134032750948619641404796736372736))/(9.22625*10**-85*math.sqrt(-1169649991522613296716866353541340846489394502286410512313491552963622677702526377538216993552919851327415518621032686306950354186147360653983918801513081128861483890875937404039374831616*u**3 + 385740774493021048318015042268854140470380922088085661830208359958878924022654906990671564163452211262449823112653866914120673419938906302136954280669366977324548222747845879052032899284992*u**2 - 10934681601929300370009569022559358062505660631826196562693310184584115581356793599484287588308533084890381333004929840794386166581586643820818871346916984722280143569224628202725807010873344*u + 52953282722417287632286265197720713997691782716178336465423716258603582943487340958848043585530474156339935438733076922864606217279858101645816623692973699443698467924685299493435228997812224) + 1.93722*10**10*u - 2.21215*10**11)**(1/3) + (9.22625*10**-85*math.sqrt(-1169649991522613296716866353541340846489394502286410512313491552963622677702526377538216993552919851327415518621032686306950354186147360653983918801513081128861483890875937404039374831616*u**3 + 385740774493021048318015042268854140470380922088085661830208359958878924022654906990671564163452211262449823112653866914120673419938906302136954280669366977324548222747845879052032899284992*u**2 - 10934681601929300370009569022559358062505660631826196562693310184584115581356793599484287588308533084890381333004929840794386166581586643820818871346916984722280143569224628202725807010873344*u + 52953282722417287632286265197720713997691782716178336465423716258603582943487340958848043585530474156339935438733076922864606217279858101645816623692973699443698467924685299493435228997812224) + 1.93722*10**10*u - 2.21215*10**11)**(1/3) + 12933.6) + 1/2*math.sqrt(-(1.50442*10**-56*(66374099732508548114477252552207192984521377098785011542261760*u + 1042724643209576631358295931525134032750948619641404796736372736))/(9.22625*10**-85*math.sqrt(-1169649991522613296716866353541340846489394502286410512313491552963622677702526377538216993552919851327415518621032686306950354186147360653983918801513081128861483890875937404039374831616*u**3 + 385740774493021048318015042268854140470380922088085661830208359958878924022654906990671564163452211262449823112653866914120673419938906302136954280669366977324548222747845879052032899284992*u**2 - 10934681601929300370009569022559358062505660631826196562693310184584115581356793599484287588308533084890381333004929840794386166581586643820818871346916984722280143569224628202725807010873344*u + 52953282722417287632286265197720713997691782716178336465423716258603582943487340958848043585530474156339935438733076922864606217279858101645816623692973699443698467924685299493435228997812224) + 1.93722*10**10*u - 2.21215*10**11)**(1/3) - (9.22625*10**-85*math.sqrt(-1169649991522613296716866353541340846489394502286410512313491552963622677702526377538216993552919851327415518621032686306950354186147360653983918801513081128861483890875937404039374831616*u**3 + 385740774493021048318015042268854140470380922088085661830208359958878924022654906990671564163452211262449823112653866914120673419938906302136954280669366977324548222747845879052032899284992*u**2 - 10934681601929300370009569022559358062505660631826196562693310184584115581356793599484287588308533084890381333004929840794386166581586643820818871346916984722280143569224628202725807010873344*u + 52953282722417287632286265197720713997691782716178336465423716258603582943487340958848043585530474156339935438733076922864606217279858101645816623692973699443698467924685299493435228997812224) + 1.93722*10**10*u - 2.21215*10**11)**(1/3) - (2.1094*10**6)*math.sqrt((1.50442*10**-56*(66374099732508548114477252552207192984521377098785011542261760*u + 1042724643209576631358295931525134032750948619641404796736372736))/(9.22625*10**-85*math.sqrt(-1169649991522613296716866353541340846489394502286410512313491552963622677702526377538216993552919851327415518621032686306950354186147360653983918801513081128861483890875937404039374831616*u**3 + 385740774493021048318015042268854140470380922088085661830208359958878924022654906990671564163452211262449823112653866914120673419938906302136954280669366977324548222747845879052032899284992*u**2 - 10934681601929300370009569022559358062505660631826196562693310184584115581356793599484287588308533084890381333004929840794386166581586643820818871346916984722280143569224628202725807010873344*u + 52953282722417287632286265197720713997691782716178336465423716258603582943487340958848043585530474156339935438733076922864606217279858101645816623692973699443698467924685299493435228997812224) + 1.93722*10**10*u - 2.21215*10**11)**(1/3) + (9.22625*10**-85*math.sqrt(-1169649991522613296716866353541340846489394502286410512313491552963622677702526377538216993552919851327415518621032686306950354186147360653983918801513081128861483890875937404039374831616*u**3 + 385740774493021048318015042268854140470380922088085661830208359958878924022654906990671564163452211262449823112653866914120673419938906302136954280669366977324548222747845879052032899284992*u**2 - 10934681601929300370009569022559358062505660631826196562693310184584115581356793599484287588308533084890381333004929840794386166581586643820818871346916984722280143569224628202725807010873344*u + 52953282722417287632286265197720713997691782716178336465423716258603582943487340958848043585530474156339935438733076922864606217279858101645816623692973699443698467924685299493435228997812224) + 1.93722*10**10*u - 2.21215*10**11)**(1/3) + 12933.6) + 25867.1) - 26.2255
"""
