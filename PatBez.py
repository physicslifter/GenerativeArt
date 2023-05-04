import numpy as np
from scipy import interpolate

class EndPoint:
    def __init__(self):
        self.x = np.random.randomsample(-10, 10)
        self.y = np.random.randomsample(-10, 10)
    def set_point(self, x, y):
        self.x = x
        self.y = y

class ControlPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y      

class QuadraticPoints:
    def __init__(self, first_end_point:EndPoint, second_end_point:EndPoint, control_point:ControlPoint):
        self.first_end = first_end_point
        self.second_end = second_end_point
        self.control = control_point

class TwoSidedConcave:
    def __init__(self, points:QuadraticPoints, granularity:int = 100):
        self.initial_points = points
        self.granularity = granularity

    def calc_x(self, t):
        return (np.square((1 - t)))*self.initial_points.first_end.x + np.multiply((2*t*self.initial_points.control.x), (1-t)) + self.initial_points.second_end.x*np.square(t)

    def calc_t_from_x(self, x): 
        t1x = self.initial_points.control.x/(self.initial_points.second_end.x - 2*self.initial_points.first_end.x) + (self.initial_points.control.x**2 - (self.initial_points.first_end.x - x)*(self.initial_points.second_end.x - 2*self.initial_points.control.x - self.initial_points.first_end.x))**2
        t2x = self.initial_points.control.x/(self.initial_points.second_end.x - 2*self.initial_points.first_end.x) - (self.initial_points.control.x**2 + (self.initial_points.first_end.x - x)*(self.initial_points.second_end.x - 2*self.initial_points.control.x - self.initial_points.first_end.x))**2
        return t1x, t2x

    def calc_y(self, t):
        return (np.square((1 - t)))*self.initial_points.first_end.y + np.multiply((2*t*self.initial_points.control.y), (1-t)) + self.initial_points.second_end.y*np.square(t)

    def calc_t_from_y(self, y): 
        t1y = self.initial_points.control.y/(self.initial_points.second_end.y - 2*self.initial_points.first_end.y) + (self.initial_points.control.y**2 - (self.initial_points.first_end.y - y)*(self.initial_points.second_end.y - 2*self.initial_points.control.y - self.initial_points.first_end.y))**2
        t2y = self.initial_points.control.y/(self.initial_points.second_end.y - 2*self.initial_points.first_end.y) - (self.initial_points.control.y**2 + (self.initial_points.first_end.y - y)*(self.initial_points.second_end.y - 2*self.initial_points.control.y - self.initial_points.first_end.y))**2
        return t1y, t2y

    def calc_initial_curve(self):
        t = np.arange(self.granularity)
        self.x1 = self.calc_x(t)
        self.y1 = self.calc_y(t)

    def generate_point_in_bounding_box(self):
        '''
        the end points should be the same
        the control point should be in the area between the initial curve and a straight line 
        '''
        #get min/max x and y to create a bounding box of possible points
        max_x = max(
            max(self.x1),
            max(self.initial_points.first_end.x, self.initial_points.second_end.x)
        )
        min_x = min(
            min(self.x1),
            min(self.initial_points.first_end.x, self.initial_points.second_end.x)
        )
        max_y = max(
            max(self.y1),
            max(self.initial_points.first_end.y, self.initial_points.second_end.y)
        )
        min_y = min(
            min(self.y1),
            min(self.initial_points.first_end.y, self.initial_points.second_end.y)
        )
        new_x = np.random.random_sample(min_x, max_x)
        new_y = np.random.random_sample(min_y, max_y)
        new_point = (new_x, new_y)
        return new_point

    def endpoint_line_y_from_x(self, x):
        slope = (self.initial_points.second_end.y - self.initial_points.first_end.y)/(self.initial_points.second_end.y - self.initial_points.first_end.y)
        b_intercept = (self.initial_points.first_end.x*self.initial_points.second_end.y - self.initial_points.second_end.x*self.initial_points.first_end.y)/(self.first_end.x - self.second_end.x)
        return slope*x + b_intercept

    def endpoint_line_x_from_y(self, y):
        slope = (self.initial_points.second_end.y - self.initial_points.first_end.y)/(self.initial_points.second_end.y - self.initial_points.first_end.y)
        b_intercept = (self.initial_points.first_end.x*self.initial_points.second_end.y - self.initial_points.second_end.x*self.initial_points.first_end.y)/(self.first_end.x - self.second_end.x)
        return (y - b_intercept)/slope

    def test_point_in_bounding_box(self, point:tuple):
        #Test whether point is inside of the desired area
        #returns Boolean
        y_bounds = []
        x_bounds = []

        #Get x & y points that are on the curve associated with the x & y positions of the test point
        t_from_x = self.calc_t_from_x(point[0])
        t_from_y = self.calc_t_from_y(point[1])
        for t in t_from_x:
            if t > 0:
                y_bounds.append(self.calc_y(t))
        for t in t_from_y:
            if t > 0:
                x_bounds.append(self.calc_x(t))

        y_bounds.append(self.endpoint_line_y_from_x(point[0]))
        x_bounds.append(self.endpoint_line_x_from_y(point[1]))

        min_x = min(x_bounds)
        max_x = max(x_bounds)
        min_y = min(y_bounds)
        max_y = max(y_bounds)
        
        f=interpolate.interp1d(self.x1,self.y1, bounds_error=False, fill_value='extrapolate')
        interpolated_data=f(point[0])

    def ray_cast_test(self, point:tuple):
        #returns true if inside
        #cast a straight ray from this point
        #The max/min of any of these points is +/-10, so a ray of length 20 should suffice
        #okay, now cast a ray from the point:
        ray_y_values = np.ones(self.granularity)*point[1]
        ray_x_values = np.arange(0, 20+20/100, 100*3) #use higher granularity to ensure I don't miss a hit
        hit_shape = False
        num_hits = 0
        for c, x in enumerate(ray_x_values):
            if c != 0:
                prev_less_than = less_than
                if x < self.x1[c]:
                    less_than = True
                else:
                    less_than = False
                if prev_less_than != less_than:
                    num_hits += 1
            else:
                #if c is 0
                if x < self.x1[c]:
                    less_than = True
                else:
                    less_than = False
        return num_hits%2 == 1 #return true if odd, false if even

    def get_new_control_point(self):
        point = self.generate_point_in_bounding_box()
        
