from Shapes import World

while 1:
    w = World(drawer_speed=100)
    w.create_initial_shape()
    w.create_second_shape()
    w.get_group_boundary(draw = True)