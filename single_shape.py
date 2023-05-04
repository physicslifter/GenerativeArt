from turtle import Turtle, Screen
import numpy as np
from math import asin, acos
from shapely.geometry import Polygon, Point

screen = Screen()
screen.setworldcoordinates(-50, -50, 50, 50)
screen.screensize()
screen.setup(width=1.0, height=1.0, startx=None, starty=None)
turtle = Turtle()
turtle.width(4)
turtle.speed(4)
turtle.ht() #hide turtle to speed up drawing



def find_distance_between_points(point1, point2):
    return (((point1[0] - point2[0])**2) + ((point1[1] - point2[1])**2))**0.5

size_scale = 30
#generate random control points
endpoint1 = (size_scale*2*(np.random.random()-0.5), size_scale*2*(np.random.random()-0.5))
endpoint2 = (size_scale*2*(np.random.random()-0.5), size_scale*2*(np.random.random()-0.5))

#endpoint1=(0, 0)
#endpoint2 = (10, 10)
dist_between_points = find_distance_between_points(endpoint1, endpoint2)

midpoint = (0.5*(endpoint1[0]+endpoint2[0]), 0.5*(endpoint1[1]+endpoint2[1]))
#red_point = (endpoint1[0]-midpoint[0])*0.7, ((endpoint1[1]-midpoint[1])*0.7)

red_x = endpoint1[0]+0.075*(endpoint2[0] - endpoint1[0])
red_y = endpoint1[1]+0.075*(endpoint2[1] - endpoint1[1])
red_point1 = (red_x,red_y)
red_point2 = (endpoint1[0]+0.925*(endpoint2[0] - endpoint1[0]), endpoint1[1]+0.925*(endpoint2[1] - endpoint1[1]))

shifted2 = (endpoint2[0]-endpoint1[0], endpoint2[0]-endpoint1[0])
shifted1 = (0,0)
if shifted2[0] > 0:
    if shifted2[1] > 0:
        #if we're in the first quadrant...
        #cos(theta) = x/hyp
        # sin(theta) = y/hyp
        theta = asin(shifted2[1]/dist_between_points)
    else:
        theta = asin(shifted2[1]/dist_between_points)
else:
    theta = acos(shifted2[0]/dist_between_points)

#red_point = (shifted2[0]*0.85+endpoint1[0], shifted2[1]*0.15+endpoint1[1])

#get slope of line perpindicular to line between endpoints
endpoint_line_slope = (endpoint2[1] - endpoint1[1])/(endpoint2[0] - endpoint1[0])
endpoint_line_intercept = endpoint2[1] - endpoint_line_slope*endpoint2[0]
perpindicular_slope = -(endpoint2[0] - endpoint1[0])/(endpoint2[1] - endpoint1[1])
#we know that the 1st bounding box intersects the endpoint line at the red points
#we can use this to get the intercept of the line we're trying to draw
perpindicular_line_intercept1 = red_point1[1] - perpindicular_slope*red_point1[0]
perpindicular_line_intercept2 = red_point2[1] - perpindicular_slope*red_point2[0]

parallel_line_intercept1 = endpoint_line_intercept + 2*dist_between_points*(1+endpoint_line_slope**2)**0.5
parallel_line_intercept2 = endpoint_line_intercept - 2*dist_between_points*(1+endpoint_line_slope**2)**0.5

corner1x = (parallel_line_intercept1-perpindicular_line_intercept1)/(perpindicular_slope - endpoint_line_slope)
corner1y = endpoint_line_slope*corner1x+parallel_line_intercept1
corner2x = (parallel_line_intercept2-perpindicular_line_intercept1)/(-endpoint_line_slope + perpindicular_slope)
corner2y = endpoint_line_slope*corner2x+parallel_line_intercept2
corner3x = (parallel_line_intercept1-perpindicular_line_intercept2)/(-endpoint_line_slope + perpindicular_slope)
corner3y = endpoint_line_slope*corner3x+parallel_line_intercept1
corner4x = (parallel_line_intercept2-perpindicular_line_intercept2)/(-endpoint_line_slope + perpindicular_slope)
corner4y = endpoint_line_slope*corner4x+parallel_line_intercept2
corner1 = (corner1x, corner1y)
corner2 = (corner2x, corner2y)
corner3 = (corner3x, corner3y)
corner4 = (corner4x, corner4y)


bounding_box = Polygon([corner1, corner2, corner3, corner4])
def random_points_within(poly, num_points):
    min_x, min_y, max_x, max_y = poly.bounds

    points = []

    while len(points) < num_points:
        random_point = Point([np.random.uniform(min_x, max_x), np.random.uniform(min_y, max_y)])
        if (random_point.within(poly)):
            points.append(random_point)

    return points

control_point = random_points_within(bounding_box, 1)[0]
control_point = tuple(control_point.coords)[0]
'''
Calculate points along Bezier curve
'''
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

bezier_points = calculate_bezier_points(endpoint1=endpoint1, endpoint2=endpoint2, control_point=control_point, granularity = 100)

def get_point_reflected_across_line(point:tuple, slope:float, intercept:float):
    p = point[0]
    q = point[1]
    a = 1
    b = -slope
    c = -intercept
    
    #Now get the reflected points
    x = (p*(a**2-b**2) - 2*b*(a*q+c))/(a**2+b**2)
    y = (q*(b**2-a**2)-2*b*(a*q+c))/(a**2+b**2)

    return (x, y)

reflected_control_point1 = get_point_reflected_across_line(control_point, endpoint_line_slope, endpoint_line_intercept)

#Get control point for second curve
control_point2 = tuple(random_points_within(Polygon([endpoint1, endpoint2, control_point]), 1)[0].coords)[0]
#switched endpoints in bezier points so it would go reverse of the first curve, and the fill works nicely 
bezier_points2 = calculate_bezier_points(endpoint1 = endpoint2, endpoint2 = endpoint1, control_point = control_point2)

area = 0
print(f"area: {np.abs(np.sum(bezier_points)-np.sum(bezier_points2))}")

writing_point = (control_point[0]+15, control_point[1]+15)
writing_point = (45, 45)

writer = Turtle()
writer.ht()
writer.pu()
writer.speed(100)
writer.setposition(writing_point)
writer.pd()
def change_writing(new_writing, writer, writing_point):
    #writer.clear()
    writer.pu()
    try:
        newy = writing_point[1] - 5
        writing_point = (writing_point[0], newy)
    except:
        writing_point = (45, 45)
    writer.setposition(writing_point)
    writer.pencolor("black")
    writer.setposition(writing_point)
    writer.write(new_writing, font=("Arial", 20, "bold"))
    return writing_point

writing_point = change_writing("1. Drawing Endpoints", writer, writing_point)

#print(theta)
turtle.pu()
turtle.goto(x = endpoint1[0], y = endpoint1[1])
turtle.dot(20, "orange")
#make green line thicker than the bounding boxes
turtle.width(10)
turtle.pencolor("green")
turtle.width(4)
turtle.pd()
turtle.goto(x = endpoint2[0], y = endpoint2[1])
turtle.dot(20, "orange")
turtle.pu()
#import pdb
#pdb.set_trace()
print(dist_between_points)
print(endpoint1, endpoint2)
print(red_point1)
print(corner1, corner2, corner3, corner4)
writing_point = change_writing("2. Drawing Bounding Box for 1st curve", writer, writing_point)
turtle.goto(red_point1)
turtle.dot(8, "red")
turtle.pu()
turtle.goto(red_point2)
turtle.dot(8, "red")
turtle.pu()
turtle.goto(corner1)
turtle.pencolor("brown")
turtle.pd()
turtle.goto(corner3)
turtle.goto(corner4)
turtle.goto(corner2)
turtle.goto(corner1)
turtle.pu()

writing_point = change_writing("3. Getting 1st control point", writer, writing_point)

turtle.speed(20)

turtle.goto(control_point)
turtle.dot(20, "blue")

turtle.speed(40)

writing_point = change_writing("4. Drawing 1st curve", writer, writing_point)

turtle.pu()
turtle.goto(bezier_points[0])
turtle.pd()
turtle.pencolor("cyan")
#import pdb
#pdb.set_trace()
for point in bezier_points:
    turtle.goto(point)

writing_point = change_writing("5. Drawing 2nd Bounding Box", writer, writing_point)

#draw the bounding box for the second control point
turtle.pu()s
turtle.pencolor("medium violet red")
turtle.pd()
turtle.goto(x = endpoint2[0], y = endpoint2[1])
turtle.goto(control_point)
turtle.goto(x = endpoint1[0], y = endpoint1[1])
#turtle.goto(reflected_control_point1)
turtle.goto(x = endpoint2[0], y = endpoint2[1])

writing_point = change_writing("6. Getting 2nd control point", writer, writing_point)

turtle.speed(10)
print("==================")
print(reflected_control_point1)
#draw 2nd control point
turtle.pu()
turtle.goto(control_point2)
turtle.dot(20, "lime")

turtle.speed(2)

writing_point = change_writing("7. Drawing the 2nd curve", writer, writing_point)

turtle.speed(4)
#draw the 2nd curve
turtle.pu()
turtle.goto(bezier_points2[0])
turtle.pd()
turtle.pencolor("cyan")
#import pdb
#pdb.set_trace()
for point in bezier_points2:
    turtle.goto(point)

writing_point = change_writing("8. Filling in the shape", writer, writing_point)

turtle.speed(100)
#Now fill in the shape
turtle.pu()
turtle.goto(bezier_points[0])
turtle.pd()
turtle.fillcolor("lime")
turtle.begin_fill()
turtle.pencolor("dark turquoise")
for point in bezier_points:
    turtle.goto(point)
for point in bezier_points2:
    turtle.goto(point)

turtle.end_fill()

writing_point = change_writing("9. Done", writer, writing_point)

#turtle.pencolor("black")
#turtle.write("All Done !")

screen.exitonclick()