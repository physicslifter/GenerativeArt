from turtle import Turtle, Screen
from math import pi, sin as sine
from Bezier import QuadBezier
import pdb

screen = Screen()
screen.setworldcoordinates(0, 0, 100, 100)
turtle = Turtle()
turtle.width(4)

def draw_sine(drawer:Turtle, screen:Screen):
    angle = 0
    while angle < 2 * pi:
        drawer.goto(angle, sine(angle))
        angle += 0.1

def draw_initial_bezier(drawer:Turtle, screen:Screen):
    my_curve = QuadBezier(0, 0, 1, 2, 3, 0)
    my_curve.random(max = 100)
    my_curve.max_k(granuality=25)
    points = my_curve.calc_curve()
    drawer.pu()
    drawer.goto(points[0][0], points[1][0])
    drawer.pd()
    #pdb.set_trace()
    for c, point in enumerate(points[0]):
        drawer.goto(point, points[1][c])
    #pdb.set_trace()
    return points, my_curve

def draw_second_bezier(drawer:Turtle, first_curve:QuadBezier, points):
    my_curve = QuadBezier()
    my_curve.random()
    my_curve.p0 = first_curve.p0
    my_curve.p2 = first_curve.p2
    for c, point in enumerate(points[0]):
        if c == 0 or c == (len(points[0])+1):
            pass
        else:
            my_curve.add_obstacle(points[1][c])
    my_curve.p2 = first_curve.p2
    points2 = my_curve.calc_curve()
    drawer.pu()
    drawer.goto(points2[0][0], points2[1][0])
    drawer.pd()
    for c, point in enumerate(points2[0]):
        drawer.goto(point, points2[1][c])

#draw_sine(turtle, screen)
initial_curve = draw_initial_bezier(turtle, screen)
second_curve = draw_second_bezier(turtle, initial_curve[1], initial_curve[0])

screen.exitonclick()