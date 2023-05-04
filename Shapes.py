from turtle import Turtle, Screen
import numpy as np
from math import asin, acos
from shapely.geometry import Polygon, Point, LinearRing, MultiPolygon
import shapely
import random
from scipy import interpolate
from scipy.interpolate import UnivariateSpline
from scipy.optimize import differential_evolution
import time

#=================================================
#useful functions
def find_distance_between_points(point1, point2):
    return (((point1[0] - point2[0])**2) + ((point1[1] - point2[1])**2))**0.5

def random_points_within(poly, num_points):
    min_x, min_y, max_x, max_y = poly.bounds
    points = []
    while len(points) < num_points:
        random_point = Point([np.random.uniform(min_x, max_x), np.random.uniform(min_y, max_y)])
        if (random_point.within(poly)):
            points.append(random_point)
    return points

def get_point_reflected_across_line(point:tuple, slope:float, intercept:float):
    p = point[0]
    q = point[1]
    a = 1
    b = -slope
    c = -intercept
    x = (p*(a**2-b**2) - 2*b*(a*q+c))/(a**2+b**2)
    y = (q*(b**2-a**2)-2*a*(b*p+c))/(a**2+b**2)
    return (x, y)

def calculate_bezier_points(endpoint1:tuple, endpoint2:tuple, control_point:tuple, granularity:int=100):
    x1 = endpoint1[0]
    x2 = endpoint2[0]
    xc = control_point[0]
    y1 = endpoint1[1]
    y2 = endpoint2[1]
    yc = control_point[1]
    points = []
    t_array = np.arange(granularity+(1/granularity))/granularity
    for t in t_array:
        x = (1-t)*(1-t)*(x1)+2*(1-t)*t*xc+t*t*x2
        y = (1-t)*(1-t)*(y1)+2*(1-t)*t*yc+t*t*y2
        points.append((x,y))
    return points

def explode_xy(xy):
    xl=[]
    yl=[]
    for i in range(len(xy)):
        xl.append(xy[i][0])
        yl.append(xy[i][1])
    return xl,yl

def shoelace_area(x_list,y_list):
    a1,a2=0,0
    x_list.append(x_list[0])
    y_list.append(y_list[0])
    for j in range(len(x_list)-1):
        a1 += x_list[j]*y_list[j+1]
        a2 += y_list[j]*x_list[j+1]
    l=abs(a1-a2)/2
    return l
#==================================================
class TwoSided:
    
    def __init__(self, concave:bool=None, endpoints:tuple=None, control_point1:tuple=None, box_length:int = 100, drawer_speed:int=10, granularity:int=100, fillcolor = "lime", edge_color = "dark turquoise"):
        #passing in initialization args
        self.fill_color, self.edge_color = fillcolor, edge_color
        self.granularity = granularity
        self.drawer_speed = drawer_speed
        self.concave = concave
        self.box_length = box_length
        self.size_scale = box_length*0.3
        self.calculated = False
        if control_point1 == None:
            self.has_control_points = False
            self.has_control1 = False
        else:
            self.has_control_points = False
            self.has_control1 = True
            self.control_point1 = control_point1
        self.has_adjacent = False
        self.turtle_setup = False
        self.has_outer_boundary = False
        self.found_bounding_box = False
        self.screen_up = True
        if endpoints != None:
            self.endpoints = endpoints
        else:
            self.endpoints = (self.generate_random_point(), self.generate_random_point())

    def setup_turtle(self):
        #create screen
        self.turtle_setup = True
        self.screen = Screen()
        self.screen.setworldcoordinates(-self.box_length/2, -self.box_length/2, self.box_length/2, self.box_length/2)
        self.screen.screensize()
        self.screen.setup(width=1.0, height=1.0, startx=None, starty=None)
        #create drawer
        self.t = Turtle()
        self.t.width(4)
        self.t.speed(self.drawer_speed)
        self.t.ht() #hide turtle to speed up drawing

    def get_bounding_box(self):
        self.found_bounding_box = True
        self.dist_between_points = find_distance_between_points(self.endpoints[1], self.endpoints[0])
        self.endpoint_line_slope = (self.endpoints[1][1] - self.endpoints[0][1])/(self.endpoints[1][0] - self.endpoints[0][0])
        self.endpoint_line_intercept = self.endpoints[1][1] - self.endpoint_line_slope*self.endpoints[1][0]
        perpindicular_slope = -(self.endpoints[1][0] - self.endpoints[0][0])/(self.endpoints[1][1] - self.endpoints[0][1])
        perpindicular_line_intercept1 = self.endpoints[0][1] - perpindicular_slope*self.endpoints[0][0]
        perpindicular_line_intercept2 = self.endpoints[1][1] - perpindicular_slope*self.endpoints[1][0]
        parallel_line_intercept1 = self.endpoint_line_intercept + 2*self.dist_between_points*(1+self.endpoint_line_slope**2)**0.5
        parallel_line_intercept2 = self.endpoint_line_intercept - 2*self.dist_between_points*(1+self.endpoint_line_slope**2)**0.5
        #get corners of the bounding box
        corner1x = (parallel_line_intercept1-perpindicular_line_intercept1)/(perpindicular_slope - self.endpoint_line_slope)
        corner1y = self.endpoint_line_slope*corner1x+parallel_line_intercept1
        corner2x = (parallel_line_intercept2-perpindicular_line_intercept1)/(-self.endpoint_line_slope + perpindicular_slope)
        corner2y = self.endpoint_line_slope*corner2x+parallel_line_intercept2
        corner3x = (parallel_line_intercept1-perpindicular_line_intercept2)/(-self.endpoint_line_slope + perpindicular_slope)
        corner3y = self.endpoint_line_slope*corner3x+parallel_line_intercept1
        corner4x = (parallel_line_intercept2-perpindicular_line_intercept2)/(-self.endpoint_line_slope + perpindicular_slope)
        corner4y = self.endpoint_line_slope*corner4x+parallel_line_intercept2
        self.corner1 = (corner1x, corner1y)
        self.corner2 = (corner2x, corner2y)
        self.corner3 = (corner3x, corner3y)
        self.corner4 = (corner4x, corner4y)
        self.bounding_box = Polygon([self.corner1, self.corner2, self.corner3, self.corner4])

    def generate_control_points(self):
        if self.found_bounding_box == False:
            self.get_bounding_box()
        self.has_control_points = True
        if self.has_control1 == False:
            self.control_point1 = tuple(random_points_within(self.bounding_box, 1)[0].coords)[0]
        reflected_control_point1 = get_point_reflected_across_line(self.control_point1, slope = self.endpoint_line_slope, intercept = self.endpoint_line_intercept)
        self.reflected_control_point1 = reflected_control_point1
        if self.concave == None: #if shape can be either concave of convex
            self.control_point2 = tuple(random_points_within(Polygon([self.endpoints[0], self.endpoints[1], self.control_point1, reflected_control_point1]), 1)[0].coords)[0] 
        elif self.concave == True:
            self.control_point2 = tuple(random_points_within(Polygon([self.endpoints[0], self.endpoints[1], self.control_point1]), 1)[0].coords)[0] 
        elif self.concave == False:
            self.control_point2 = tuple(random_points_within(Polygon([self.endpoints[0], self.endpoints[1], reflected_control_point1]), 1)[0].coords)[0] 
        else:
            raise Exception ("concave must be Boolean or None")
    
    def generate_random_point(self):
        return (self.size_scale*2*(np.random.random()-0.5), self.size_scale*2*(np.random.random()-0.5))

    def calculate_curve_points(self):
        if self.has_control_points == False:
            self.generate_control_points()
        self.calculated = True
        self.curve1 = calculate_bezier_points(endpoint1 = self.endpoints[0], endpoint2 = self.endpoints[1], control_point = self.control_point1, granularity = self.granularity)
        self.curve2 = calculate_bezier_points(endpoint1 = self.endpoints[1], endpoint2 = self.endpoints[0], control_point = self.control_point2, granularity = self.granularity)
        self.points = self.curve1 + self.curve2

    def get_area(self):
        xy_e = explode_xy(self.points)
        area = shoelace_area(xy_e[0], xy_e[1])
        print(area)
        return area

    def draw_shape(self):
        self.t.pu()
        self.t.goto(self.curve1[0])
        self.t.pd()
        self.t.fillcolor(self.fill_color)
        self.t.begin_fill()
        self.t.pencolor(self.edge_color)
        '''for point in self.curve1:
            self.t.goto(point)
        for point in self.curve2:
            self.t.goto(point)'''
        for point in self.points:
            self.t.goto(point)
        self.t.end_fill()

    def clear_canvas(self):
        self.t.clear()

    def go(self):
        self.setup_turtle()
        self.get_bounding_box()
        self.generate_control_points()
        self.calculate_curve_points()
        while self.get_area() < 0.01*(self.box_length**2):
            self.setup_turtle()
            self.get_bounding_box()
            self.generate_control_points()
            self.calculate_curve_points()
        self.draw_shape()
        self.screen.exitonclick()

    def calc(self):
        if self.found_bounding_box == False:
            self.get_bounding_box()
        if self.has_control_points == False:
            self.generate_control_points()
        self.calculate_curve_points()
        total_tries = 0
        num_tries = 0
        while self.get_area() < 0.000001*(self.box_length**2):
            self.get_bounding_box()
            self.generate_control_points()
            self.calculate_curve_points()
            if num_tries > 100:
                self.__init__()
                num_tries = 0
            if total_tries > 1000:
                break
            total_tries+=1
            num_tries+=1

    def get_outer_boundary(self):
        self.has_outer_boundary = True
        if self.calculated == False:
            self.calculate_curve_points()
        shape_poly = Polygon(self.points)
        self.outer_boundary = shape_poly.buffer(distance = 2, resolution = 10)
        #self.outer_boundary = shapely.buffer(shape_poly, distance = 2, quad_segs = 32)
        self.outer_boundary_points = list(self.outer_boundary.exterior.coords)
        self.tight_boundary = shape_poly.buffer(distance = 1.5, resolution = 100)
        self.tight_points = list(self.tight_boundary.exterior.coords)

    def get_boundary(self, offset_distance:int=1):
        '''
        gets a border of small length, d around the shape
        '''
        self.has_outer_boundary = True
        if self.calculated == False:
            self.calculate_curve_points()
        #Getting the offset
        x1 = self.endpoints[0][0]
        x2 = self.endpoints[1][0]
        xc = self.control_point1[0]
        y1 = self.endpoints[0][1]
        y2 = self.endpoints[1][1]
        yc = self.control_point1[1]
        xc2 = self.control_point2[0]
        yc2 = self.control_point2[1]
        points1 = []
        points2 = []
        t_array = np.arange(self.granularity+(1/self.granularity))/self.granularity
        for t in t_array:
            curve1_x = (1-t)*(1-t)*(x1)+2*(1-t)*t*xc+t*t*x2
            curve1_y = (1-t)*(1-t)*(y1)+2*(1-t)*t*yc+t*t*y2
            curve2_x = (1-t)*(1-t)*(x1)+2*(1-t)*t*xc2+t*t*x2
            curve2_y = (1-t)*(1-t)*(y1)+2*(1-t)*t*yc2+t*t*y2
            curve1_x_prime = -2*x1*t+2*xc-4*xc*t+2*t*x2
            curve1_y_prime = -2*y1*t+2*yc-4*yc*t+2*t*y2
            curve2_x_prime = -2*x1*t+2*xc2-4*xc2*t+2*t*x2
            curve2_y_prime = -2*y1*t+2*yc2-4*yc2*t+2*t*y2
            boundary1_x = curve1_x + offset_distance*curve1_y_prime*(curve1_x_prime**2+curve1_y_prime**2)**-0.5
            boundary1_y = curve1_y + offset_distance*curve1_x_prime*(curve1_x_prime**2+curve1_y_prime**2)**-0.5
            boundary2_x = curve2_x + offset_distance*curve2_y_prime*(curve2_x_prime**2+curve2_y_prime**2)**-0.5
            boundary2_y = curve2_y + offset_distance*curve2_x_prime*(curve2_x_prime**2+curve2_y_prime**2)**-0.5
            points1.append((boundary1_x,boundary1_y))
            points2.append((boundary2_x,boundary2_y))
            
        points2.reverse()
        self.boundary_points = points1 + points2

    def draw_outer_boundary(self):
        self.outer_boundary_points = list(self.outer_boundary.exterior.coords)
        self.t.pu()
        self.t.goto(self.outer_boundary_points[0])
        self.t.pd()
        self.t.pencolor("medium purple")
        for point in self.outer_boundary_points:
            self.t.goto(point)
        
    def draw_adjacent(self):
        if self.has_adjacent == False:
            self.get_adjacent_shape()
        self.t.pu()
        self.t.goto(self.adjacent_bezier[0])
        self.t.pd()
        self.t.pencolor("medium violet red")
        for point in self.adjacent_bezier:
            self.t.goto(point)
        self.t.pu()
        self.t.goto(self.adjacent_endpoint1)
        self.t.dot(20, "blue")
        self.t.write("endpoint 1")
        self.t.pu()
        self.t.goto(self.adjacent_endpoint2)
        self.t.dot(20, "blue")
        self.t.write("endpoint 2")
        self.t.pu()
        self.t.goto(self.adjacent_control_point)
        self.t.dot(20, "green")
        self.t.write("control point")
        self.t.pu()
        self.t.goto(self.adjacent_ref_1)
        self.t.dot(20, "light sea green")
        self.t.write("point 1")
        self.t.pu()
        self.t.goto(self.adjacent_ref_2)
        self.t.dot(20, "light sea green")
        self.t.write("point 2")

    def draw_adjacent2(self):
        if self.has_adjacent == False:
            self.get_adjacent2()
        self.t.pu()
        self.t.goto(self.adjacent_curve_points[0])
        self.t.pd()
        self.t.pencolor("black")
        for point in self.adjacent_curve_points:
            self.t.goto(point)

    def draw_adjacent_bezier(self):
        self.t.pu()
        self.t.goto(self.adjacent_bezier[0])
        self.t.pd()
        self.t.dot(20, "dark green")
        self.t.pu()
        self.t.goto(self.adjacent_bezier[-1])
        self.t.pd()
        self.t.dot(20, "dark green")
        self.t.pu()
        self.t.goto(self.adjacent_control_point)
        self.t.dot(20, "dark red")
        self.t.pu()
        self.t.goto(self.adjacent_bezier[0])
        self.t.pencolor("red")
        self.t.pd()
        for point in self.adjacent_bezier:
            self.t.goto(point)

    def draw_w_boundary(self):
        self.setup_turtle()
        self.calc()
        self.draw_shape()
        if self.has_outer_boundary == False:
            self.get_outer_boundary()
        self.draw_outer_boundary()
        self.screen.exitonclick()

    def draw_w_adjacent(self):
        if self.turtle_setup == False:
            self.setup_turtle()
        self.calc()
        self.draw_shape()
        if self.has_outer_boundary == False:
            self.get_outer_boundary()
        #self.draw_outer_boundary()
        self.get_adjacent2()
        self.draw_adjacent2()
        #self.get_adjacent_shape()
        #self.draw_adjacent()
        self.get_adjacent_bezier()
        self.draw_adjacent_bezier()
        if self.screen_up == False:
            self.screen.exitonclick()
            self.screen_up = True

    def get_adjacent_shape(self):
        self.has_adjacent = True
        #should be 3 for endpoint1, point1, and point2
        unique_indices = False
        while unique_indices == False:
            indices = [np.random.randint(len(self.points)),
                        np.random.randint(len(self.points)),
                        np.random.randint(len(self.points))]
            unique_indices = indices[0] != indices[1] and indices[0] != indices[2] and indices[1] != indices[2]
        #make sure all of the indices are different
        endpoint1_index = min(indices)
        point2_index = max(indices)
        for index in indices:
            if index != endpoint1_index and index != point2_index:
                point1_index = index
        endpoint1 = self.points[endpoint1_index]
        point1 = self.points[point1_index]
        point2 = self.points[point2_index]
        self.point1_index = point1_index
        self.point2_index =point2_index
        self.endpoint1_index = endpoint1_index
        ts = np.arange(self.granularity+(1/self.granularity))/self.granularity
        point1_t = np.random.uniform()
        point2_t = np.random.uniform()

        for c, t in enumerate(ts):
            diff1 = np.abs(t - point1_t)
            diff2 = np.abs(t - point2_t)
            if c==0:
                min_diff1 = diff1
                min_t1 = t
                min_diff2 = diff2
                min_t2 = t
            else:
                if diff1 < min_diff1:
                    min_diff1 = diff1
                    min_t1 = t
                if diff2 < min_diff2:
                    min_diff2 = diff2
                    min_t2 = t

        point1_t = min_t1
        point2_t = min_t2
        if point1_t > point2_t:
            point1_t = min_t2
            point2_t = min_t1

        point1_t = 0.33
        point2_t = 0.66

        #Calculate endpoint2
        A_x = (point2[0] - (1-point2_t**2)*endpoint1[0])/(2*point2_t*(1-point2_t)) - ((point1[0] - (1-point1_t**2)*endpoint1[0])/(2*point1_t*(1-point1_t)))
        A_y = (point2[1] - (1-point2_t**2)*endpoint1[1])/(2*point2_t*(1-point2_t)) - ((point1[1] - (1-point1_t**2)*endpoint1[1])/(2*point1_t*(1-point1_t)))
        B = ((-point1_t**2)/(2*point1_t*(1-point1_t))) + (((-point2_t**2)/(2*point2_t*(1-point2_t))))
        
        #technique 2
        x_numerator_term1 = -point1[0]*((1-point2_t)*point2_t)
        x_numerator_term2 = endpoint1[0]*((1+point2_t)*(1-point2_t)*point1_t*(1-point1_t) - (1+point1_t)*(1-point1_t)*(point2_t)*(1-point2_t))
        x_numerator_term3 = point2[0]*((1 - point1_t)*point1_t)
        y_numerator_term1 = -point1[1]*((1-point2_t)*point2_t)
        y_numerator_term2 = endpoint1[1]*((1+point2_t)*(1-point2_t)*point1_t*(1-point1_t) - (1+point1_t)*(1-point1_t)*(point2_t)*(1-point2_t))
        y_numerator_term3 = point2[1]*((1 - point1_t)*point1_t)
        x_numerator = x_numerator_term1+x_numerator_term2+x_numerator_term3
        y_numerator = y_numerator_term1+y_numerator_term2+y_numerator_term3
        denominator = 2*point1_t*point2_t*(1-point1_t)*(1-point2_t)
        endpoint2 = ((x_numerator/denominator), (y_numerator/denominator))

        #endpoint2 = ((A_x/B),(A_y/B))
        control_point_x = (point1[0] - (1-point1_t**2)*endpoint1[0]-point1_t**2*endpoint2[0])/(2*point1_t*(1-point1_t))
        control_point_y = (point1[1] - (1-point1_t**2)*endpoint1[1]-point1_t**2*endpoint2[1])/(2*point1_t*(1-point1_t))
        control_point = (control_point_x, control_point_y)
        self.adjacent_endpoint1 = endpoint1
        self.adjacent_endpoint2 = endpoint2
        self.adjacent_control_point = control_point
        self.adjacent_bezier = calculate_bezier_points(endpoint1, endpoint2, control_point)
        self.adjacent_ref_1 = point1
        self.adjacent_ref_2 = point2
        self.point1_t = point1_t
        self.point2_t = point2_t


        '''
        technique 2:
            get three points from boundary an interpolate/draw a curve that goes through these three points
        '''
    def get_adjacent2(self):
        self.has_adjacent = True
        point_inside = True #set to true to start the while loop
        while point_inside == True:
            index1 = np.random.randint(len(self.outer_boundary_points))
            index2 = np.random.randint(len(self.outer_boundary_points))
            curve_points = self.outer_boundary_points[index1:index2] #get random segment of curve to draw along
            while len(curve_points) < (len(self.outer_boundary_points)/10) or len(curve_points) > (len(self.outer_boundary_points)/2):
                index1 = np.random.randint(len(self.outer_boundary_points))
                index2 = np.random.randint(len(self.outer_boundary_points))
                curve_points = self.outer_boundary_points[index1:index2]
                if len(curve_points) == 0:
                    curve_points = self.outer_boundary_points[index2:index1]

            exploded = explode_xy(curve_points)
            x, y = exploded[0], exploded[1]
            t_progress = np.random.uniform() #controls how much of the adjacent curve is along the existing boundary
            while t_progress < 0.5:
                t_progress = np.random.uniform()
            t_progress = 0.25
            num_points = len(curve_points)

            t_array = np.arange(0, t_progress, t_progress/num_points)
            #import pdb
            #pdb.set_trace()
            print(len(t_array), len(x))
            full_t_array = np.arange(0, 1, t_progress/num_points)
            x_extrapolator = UnivariateSpline(t_array, x, k=2)
            y_extrapolator = UnivariateSpline(t_array, y, k=2)
            self.adjacent_curve_points = []
            for t in full_t_array:
                #print(t)
                point = (x_extrapolator(t).item(), y_extrapolator(t).item())
                formal_point = Point([point[0],point[1]])
                tight_boundary_polygon = Polygon(self.tight_points)
                if formal_point.distance(tight_boundary_polygon) < (self.size_scale/2):
                    self.adjacent_curve_points.append(point)
            point_inside = False
            for point in self.adjacent_curve_points:
                formal_point = Point([point[0],point[1]])
                formal_boundary = Polygon(self.tight_points)
                if (formal_point.within(formal_boundary)):
                    point_inside = True
        self.full_t_array = full_t_array
        self.x_extrapolator = x_extrapolator
        self.y_extrapolator = y_extrapolator

    def get_adjacent_bezier(self):
        endpoint1 = self.adjacent_curve_points[0]
        endpoint2 = self.adjacent_curve_points[-1]
        def optimizable_func(params):
            x, y = params
            control_point = (x,y)
            bezier = calculate_bezier_points(endpoint1, endpoint2, control_point, granularity=len(self.adjacent_curve_points))
            least_squares = 0
            for c, point in enumerate(self.adjacent_curve_points):
                least_squares += ((point[0] - bezier[c][0])**2+(point[1] - bezier[c][1])**2)**0.5
            return least_squares
        my_bounds = ((-self.box_length*10,self.box_length*10),(-self.box_length*10, self.box_length*10))
        diffEV = differential_evolution(optimizable_func, bounds = my_bounds, popsize=100)
        self.solution = diffEV
        control_point = (diffEV.x[0], diffEV.x[1])
        self.adjacent_control_point = control_point
        self.adjacent_bezier = calculate_bezier_points(endpoint1, endpoint2, control_point)
        return control_point, endpoint1, endpoint2

class World:
    def __init__(self, drawer_speed=10, box_length:int = 100):
        self.box_length = box_length
        self.shapes = []
        self.boundary = []
        self.turtle_setup = False
        self.box_length = 100
        self.drawer_speed = drawer_speed
        self.size_scale = box_length*0.1

    def setup_turtle(self):
        #create screen
        self.turtle_setup = True
        self.screen = Screen()
        self.screen.setworldcoordinates(-self.box_length/2, -self.box_length/2, self.box_length/2, self.box_length/2)
        self.screen.screensize()
        self.screen.setup(width=1.0, height=1.0, startx=None, starty=None)
        #create drawer
        self.t = Turtle()
        self.t.width(4)
        self.t.speed(self.drawer_speed)
        self.t.ht() #hide turtle to speed up drawing

    def add_shape(self, shape:TwoSided):
        self.shapes.append(shape)

    def create_initial_shape(self):
        shape = TwoSided(concave = None)
        shape.calc()
        shape.get_outer_boundary()
        self.boundary = Polygon(shape.tight_points)
        process_worked = False
        while process_worked == False:
            try:
                shape.get_adjacent2()
                process_worked = True
            except:
                process_worked = False
        self.second_shape_params = shape.get_adjacent_bezier()
        self.add_shape(shape)

    def create_new_shape(self):
        self.get_group_boundary()
        self.get_adjacent()
        new_shape_params = self.get_adjacent_bezier()
        endpoints = (new_shape_params[1], new_shape_params[2])
        control_point1 = new_shape_params[0]
        new_shape = TwoSided(control_point1 = control_point1, endpoints = endpoints)
        new_shape.get_bounding_box()
        valid_curve = False
        curve_tries = []
        while valid_curve == False:
            new_shape.control_point2 = tuple(random_points_within(new_shape.bounding_box, 1)[0].coords)[0]
            new_shape.has_control_points = True
            new_shape.calc()
            valid_curve = True
            curve_tries.append(new_shape.curve2)
            #Test for each point in the curve whether it crosses into the first shape
            for point in new_shape.points:
                formal_point = Point(point)
                for shape in self.shapes:
                    if formal_point.within(shape.tight_boundary):
                        valid_curve = False
            #Test whether the second shape fully envelopes the first shape
            test_point = Point(self.shapes[0].points[int(self.shapes[0].granularity/3)])
            new_shape_poly = Polygon(new_shape.points)
            if test_point.within(new_shape_poly):
                valid_curve = False
        new_shape.has_control_points = True
        new_shape.calc()
        new_shape.get_outer_boundary()
        self.shape2_curve_tries = curve_tries
        self.add_shape(new_shape)


    def create_second_shape(self):
        endpoints = (self.second_shape_params[1], self.second_shape_params[2])
        control_point1 = self.second_shape_params[0]
        new_shape = TwoSided(control_point1=control_point1, endpoints=endpoints)
        new_shape.get_bounding_box()
        #illegal_polygons = []
        #polygon_holes = []
        #for shape in self.shapes:
        #    illegal_polygons.append(shape.tight_points)
        #    for point in shape.tight_points:
        #        polygon_holes.append(point)
        #polygon_holes = [LinearRing(polygon_holes)]
        #box_for_control_point2 = Polygon([shape.corner1, shape.corner2, shape.corner2, shape.corner4], holes = polygon_holes)
        valid_curve = False
        curve_tries = []

        while valid_curve == False:
            new_shape.control_point2 = tuple(random_points_within(new_shape.bounding_box, 1)[0].coords)[0]
            new_shape.has_control_points = True
            new_shape.calc()
            valid_curve = True
            curve_tries.append(new_shape.curve2)
            #Test for each point in the curve whether it crosses into the first shape
            for point in new_shape.points:
                formal_point = Point(point)
                for shape in self.shapes:
                    if formal_point.within(shape.tight_boundary):
                        valid_curve = False
            #Test whether the second shape fully envelopes the first shape
            test_point = Point(self.shapes[0].points[int(self.shapes[0].granularity/3)])
            new_shape_poly = Polygon(new_shape.points)
            if test_point.within(new_shape_poly):
                valid_curve = False

        new_shape.has_control_points = True
        new_shape.calc()
        new_shape.get_outer_boundary()
        self.shape2_curve_tries = curve_tries
        self.add_shape(new_shape)

    def get_group_boundary(self, draw = False):
        group_polygon_list = []
        for shape in self.shapes:
            group_polygon_list.append(Polygon(shape.points))
        self.group_polygon = MultiPolygon(group_polygon_list)
        self.group_boundary = self.group_polygon.buffer(distance = 2)
        self.outer_boundary_points = list(self.group_boundary.exterior.coords)
        self.tight_boundary = self.group_polygon.buffer(distance = 1.5, resolution = 10)
        self.tight_points = list(self.tight_boundary.exterior.coords)
        if draw == True:
            self.draw_shapes()
            self.t.pu()
            self.t.goto(self.outer_boundary_points[0])
            self.t.pd()
            self.t.pencolor("red")
            for point in self.outer_boundary_points:
                self.t.goto(point)
            self.t.pu()

    def get_adjacent(self):
        self.has_adjacent = True
        point_inside = True #set to true to start the while loop
        while point_inside == True:
            index1 = np.random.randint(len(self.outer_boundary_points))
            index2 = np.random.randint(len(self.outer_boundary_points))
            curve_points = self.outer_boundary_points[index1:index2] #get random segment of curve to draw along
            while len(curve_points) < (len(self.outer_boundary_points)/10) or len(curve_points) > (len(self.outer_boundary_points)/2):
                index1 = np.random.randint(len(self.outer_boundary_points))
                index2 = np.random.randint(len(self.outer_boundary_points))
                curve_points = self.outer_boundary_points[index1:index2]
                if len(curve_points) == 0:
                    curve_points = self.outer_boundary_points[index2:index1]

            exploded = explode_xy(curve_points)
            x, y = exploded[0], exploded[1]
            t_progress = np.random.uniform() #controls how much of the adjacent curve is along the existing boundary
            while t_progress < 0.5:
                t_progress = np.random.uniform()
            t_progress = 0.9
            num_points = len(curve_points)

            t_array = np.arange(0, t_progress, t_progress/num_points)
            #import pdb
            #pdb.set_trace()
            print(len(t_array), len(x))
            full_t_array = np.arange(0, 1, t_progress/num_points)
            x_extrapolator = UnivariateSpline(t_array, x, k=2)
            y_extrapolator = UnivariateSpline(t_array, y, k=2)
            self.adjacent_curve_points = []
            for t in full_t_array:
                #print(t)
                point = (x_extrapolator(t).item(), y_extrapolator(t).item())
                formal_point = Point([point[0],point[1]])
                tight_boundary_polygon = Polygon(self.tight_points)
                if formal_point.distance(tight_boundary_polygon) < (self.size_scale/2):
                    self.adjacent_curve_points.append(point)
            point_inside = False
            for point in self.adjacent_curve_points:
                formal_point = Point([point[0],point[1]])
                formal_boundary = Polygon(self.tight_points)
                if (formal_point.within(formal_boundary)):
                    point_inside = True
        self.full_t_array = full_t_array
        self.x_extrapolator = x_extrapolator
        self.y_extrapolator = y_extrapolator
        
    def get_adjacent_bezier(self):
        endpoint1 = self.adjacent_curve_points[0]
        endpoint2 = self.adjacent_curve_points[-1]
        def optimizable_func(params):
            x, y = params
            control_point = (x,y)
            bezier = calculate_bezier_points(endpoint1, endpoint2, control_point, granularity=len(self.adjacent_curve_points))
            least_squares = 0
            for c, point in enumerate(self.adjacent_curve_points):
                least_squares += ((point[0] - bezier[c][0])**2+(point[1] - bezier[c][1])**2)**0.5
            return least_squares
        my_bounds = ((-self.box_length*10,self.box_length*10),(-self.box_length*10, self.box_length*10))
        diffEV = differential_evolution(optimizable_func, bounds = my_bounds, popsize=10, maxiter = 10)
        self.solution = diffEV
        control_point = (diffEV.x[0], diffEV.x[1])
        self.adjacent_control_point = control_point
        self.adjacent_bezier = calculate_bezier_points(endpoint1, endpoint2, control_point)
        return control_point, endpoint1, endpoint2

    def generate_shapes(self, n:int = 10):
        self.shapes = []
        self.create_initial_shape()
        num_shapes = 0
        while num_shapes < n:
            try:
                self.create_new_shape()
                num_shapes+=1
            except: 
                pass

    def clear(self):
        self.shapes = []

    def draw_shapes(self, annotate = False):
        
        self.get_group_boundary()
        colors = ["dark red", "blue", "purple", "teal", "lime", "dark turquoise", "orange red"]
        if self.turtle_setup == False:
            self.setup_turtle()
        self.t.clear()
        if annotate == False:
            for c, shape in enumerate(self.shapes):
                self.t.pu()
                self.t.goto(shape.points[0])
                self.t.pd()
                self.t.fillcolor(random.choice(colors))
                self.t.begin_fill()
                self.t.pencolor(random.choice(colors))
                for point in shape.points:
                    self.t.goto(point)
                self.t.pu()
                self.t.end_fill()
            self.t.goto(self.tight_points[0])
            self.t.pencolor("red")
            self.t.pd()
            for point in self.tight_points:
                self.t.goto(point)
        else:
            #pass turtle parent to all shapes so that they can run their drawing functions on the currently open canvas (the same canavs)
            for shape in self.shapes:
                shape.t = self.t
            self.t.pu()
            writing_point = (45, 45)
            writer = Turtle()
            writer.ht()
            writer.pu()
            writer.setposition(writing_point)
            writer.speed(100)
            def write(string):
                writer.write(string, font=("Arial", 20, "bold"))
                writer.pu()
                loc = writer.position()
                new_loc = (loc[0], loc[1]-5)
                writer.goto(new_loc)
            write("1. Getting random endpoints for 1st")
            write("   shape")
            annotator = Turtle()
            annotator.ht()
            annotator.width(4)
            annotator.speed(self.drawer_speed)
            annotator.pu()
            annotator.goto(self.shapes[0].endpoints[0])
            annotator.pd()
            annotator.dot(20, "orange")
            annotator.pu()
            annotator.goto(self.shapes[0].endpoints[1])
            annotator.dot(20, "orange")
            write("2. Getting Bounding Box for 1st ")
            write("   control point")
            annotator.pu()
            annotator.goto(self.shapes[0].corner1)
            annotator.pd()
            annotator.pencolor("brown")
            annotator.goto(self.shapes[0].corner3)
            annotator.goto(self.shapes[0].corner4)
            annotator.goto(self.shapes[0].corner2)
            annotator.goto(self.shapes[0].corner1)
            annotator.pu()
            write("3. Getting 1st control point")
            annotator.goto(self.shapes[0].control_point1)
            annotator.pd()
            annotator.dot(20, "blue")
            write("4. Drawing 1st curve")
            annotator.pu()
            annotator.goto(self.shapes[0].curve1[0])
            annotator.pencolor("cyan")
            annotator.pd()
            for point in self.shapes[0].curve1:
                annotator.goto(point)
            annotator.pu()
            write("5. Getting Bounding Box for")
            write("   2nd endpoint")
            annotator.pencolor("medium violet red")
            annotator.goto(self.shapes[0].endpoints[0])
            annotator.pd()
            annotator.goto(self.shapes[0].control_point1)
            annotator.goto(self.shapes[0].endpoints[1])
            annotator.goto(self.shapes[0].reflected_control_point1)
            annotator.goto(self.shapes[0].endpoints[0])
            annotator.pu()
            write("6. Getting 2nd control point")
            annotator.pu()
            annotator.goto(self.shapes[0].control_point2)
            annotator.pd()
            annotator.dot(20,"lime")
            write("7. Drawing 2nd curve")
            annotator.pu()
            annotator.goto(self.shapes[0].curve2[0])
            annotator.pencolor("teal")
            annotator.pd()
            for point in self.shapes[0].curve2:
                annotator.goto(point)
            annotator.pu()
            write("8. Fill in shape")
            self.shapes[0].draw_shape()
            write("9. Find boundary surrounding shape")
            self.t.speed(4)
            self.shapes[0].draw_outer_boundary()
            self.t.speed(self.drawer_speed)
            write("10. Interpolate line along segment of")
            write("    boundary, and extrapolate to get ")
            write("    an adjacent offset curve.")
            self.shapes[0].draw_adjacent2()
            write("11. Optimize Bezier to fit adjacent")
            write("    interpolated curve")
            self.shapes[0].draw_adjacent_bezier()
            write("12. Draw 1st curve of new Bezier")
            annotator.pu()
            annotator.goto(self.shapes[1].curve1[0])
            annotator.pd()
            annotator.pencolor("teal")
            for point in self.shapes[1].curve1:
                annotator.goto(point)
            write("13. try 2nd curves until finding one that")
            write("    does not intersect shape 1")
            curve_turtle = Turtle()
            for c, curve in enumerate(self.shape2_curve_tries):
                curve_turtle.pu()
                curve_turtle.speed(self.drawer_speed)
                curve_turtle.goto(curve[0])
                curve_turtle.pd()
                curve_turtle.pencolor("blue")
                curve_turtle.width(4)
                curve_turtle.speed(self.drawer_speed)
                for point in curve:
                    curve_turtle.goto(point)
                if c == (len(self.shape2_curve_tries)-1):
                    curve_turtle.pencolor("green")
                    curve_turtle.write("PASSED", font=("Arial", 40, "bold"))
                    time.sleep(1)
                else:
                    curve_turtle.pencolor("dark red")
                    curve_turtle.write("FAILED", font=("Arial", 40, "bold"))
                    time.sleep(1)
                    curve_turtle.clear()
            write("14. draw 2nd shape")
            self.shapes[1].draw_shape()
            '''
            clear everything
            '''
            write("All together now!")
            time.sleep(1)
            curve_turtle.clear()
            annotator.clear()
            writer.clear()
            self.t.clear()
            while new_shapes == False:
                self.t.clear()
                for c, shape in enumerate(self.shapes):
                    self.t.pu()
                    self.t.speed(100)
                    self.t.goto(shape.points[0])
                    self.t.pd()
                    self.t.fillcolor(random.choice(colors))
                    self.t.begin_fill()
                    self.t.pencolor(random.choice(colors))
                    for point in shape.points:
                        self.t.goto(point)
                    self.t.pu()
                    self.t.end_fill()
                new_shapes = False
                while new_shapes == False:
                    try:
                        #self.create_initial_shape()
                        #self.shapes = [self.shapes[0]]
                        #self.create_second_shape()
                        new_shapes = True
                    except:
                        new_shapes = False
                #time.sleep(2)
                #self.t.clear()




                


            
            






        


    
        
