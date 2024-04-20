from shapely import LineString, box
from shapely.ops import unary_union

import gameboxes
import walls
# This file will contain some predefined projects so they don't reside in tkGUI.py

from laserproject import LaserObject, LaserProject, LaserTextObject, distribute_polygons_around_circle
from shapely.geometry import Polygon
from walls import create_tabbed_wall, create_slotted_wall, single_slotted_wall, tabbed_wall, slotted_wall, one_tile_door, insert_tabbed_wall, double_door, single_door

import csv
import json

def base_room(points):

    laserProject = LaserProject()
    tile_size = 25

    laserObject = LaserObject(2500, 300, 1)
    laserObject.location = (50, 50)
    laserObject.priority = 10

    # Multiply the points by the tile size for x
    points = [[x * tile_size for x in point] for point in points]
    scaled_points = points.copy()
    original_points = points.copy()

    # Create a polygon from the scaled points
    original_polygon = Polygon(scaled_points)
    buffer_distance = 5
    buffered_polygon = original_polygon.buffer(buffer_distance, join_style=2)

    buffered_polygon_coords = list(buffered_polygon.exterior.coords)

    # remove the last point, so it's no longer closed
    buffered_polygon_coords.pop()

    # Create a LineString from the scaled points to represent the original polygon as a line
    line = LineString(buffered_polygon_coords)
    traced_line = line.buffer(5 / 2, cap_style=1, join_style=1)
    traced_line_coords = list(traced_line.exterior.coords)
    laserObject.add_polygon(traced_line_coords)

    laserObject.fill()

    new_polygon = Polygon(traced_line_coords)
    buffer_distance = 2.5
    buffered_polygon = new_polygon.buffer(buffer_distance, join_style=2)
    buffered_polygon = list(buffered_polygon.exterior.coords)

    new_lo = LaserObject(400, 600, 1)
    new_lo.location = (50, 50)

    # Close the original polygon
    original_points.append(original_points[0])
    new_lo.add_polygon(original_points)

    # Draw around the original polygon
    outline = Polygon(original_points).buffer(10, join_style=2)
    outline_coords = list(outline.exterior.coords)
    new_lo.add_polygon(outline_coords)

    laserProject.laser_objects.append(new_lo)

    laserProject.laser_objects.append(laserObject)

    return laserProject

def half_open_room():

    offset = 10

    points_left = [[0, 0], [0, 4], [1, 4], [1, 6]]
    points_right= [[3, 0], [3, 4], [2, 4], [2, 6]]

    laserProject = LaserProject()
    tile_size = 25

    # Multiply the points by the tile size for x
    points_left = [[x * tile_size for x in point] for point in points_left]
    points_right = [[x * tile_size for x in point] for point in points_right]

    laserObject = LaserObject(400, 600, 1)
    laserObject.location = (offset, offset)
    laserObject.priority = 10

    # Identify endpoints
    left_start, left_end = points_left[0], points_left[-1]
    right_start, right_end = points_right[0], points_right[-1]

    # Determine shortest connections (assuming straight lines for simplicity)
    # We calculate distances between each possible pair of endpoints and choose the shortest
    distances = {
        "left_start-right_start": (left_start, right_start),
        "left_start-right_end": (left_start, right_end),
        "left_end-right_start": (left_end, right_start),
        "left_end-right_end": (left_end, right_end)
    }

    # Calculate actual distances
    actual_distances = {key: ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5 for key, (p1, p2) in
                        distances.items()}

    # Find the shortest connection
    shortest_connection = min(actual_distances, key=actual_distances.get)

    # Depending on the shortest connection, order the points to form the polygon
    if shortest_connection == "left_start-right_start":
        polygon_points = points_left[::-1] + points_right
    elif shortest_connection == "left_start-right_end":
        polygon_points = points_left[::-1] + points_right[::-1]
    elif shortest_connection == "left_end-right_start":
        polygon_points = points_left + points_right
    else:  # "left_end-right_end"
        polygon_points = points_left + points_right[::-1]

    # Close the polygon by adding the first point at the end
    polygon_points.append(polygon_points[0])
##
    # Create a polygon from the scaled points
    original_polygon = Polygon(polygon_points)
    buffer_distance = 5
    buffered_polygon = original_polygon.buffer(buffer_distance, join_style=2)

    buffered_polygon_coords = list(buffered_polygon.exterior.coords)

    laserObject.add_polygon(polygon_points)

    # Draw around the original polygon
    outline = Polygon(polygon_points).buffer(10, join_style=2)
    outline_coords = list(outline.exterior.coords)

    laserObject.add_polygon(outline_coords)

    # now from the buffered polygon, remove the lines that were closing the polygon
    buffered_polygon_coords.pop()

    # And split the polygon into two, right down the middle
    left_half = buffered_polygon_coords[:len(buffered_polygon_coords) // 2]
    right_half = buffered_polygon_coords[len(buffered_polygon_coords) // 2:]

    #laserObject.add_polygon(left_half)
    #laserObject.add_polygon(right_half)

    # And create LineString for both
    line = LineString(left_half)
    traced_line = line.buffer(5 / 2, cap_style=1, join_style=1)
    traced_line_coords = list(traced_line.exterior.coords)

    left_laserObject = LaserObject(2500, 300, 1)
    left_laserObject.add_polygon(traced_line_coords)
    left_laserObject.fill()
    left_laserObject.location = (offset, offset)
    left_laserObject.power_mode = "M4"
    laserProject.laser_objects.append(left_laserObject)

    # And the second half
    line = LineString(right_half)
    traced_line = line.buffer(5 / 2, cap_style=1, join_style=1)
    traced_line_coords = list(traced_line.exterior.coords)

    right_laserObject = LaserObject(2500, 300, 1)
    right_laserObject.add_polygon(traced_line_coords)
    right_laserObject.fill()
    right_laserObject.location = (offset, offset)
    left_laserObject.power_mode = "M4"
    laserProject.laser_objects.append(right_laserObject)

    laserProject.laser_objects.append(laserObject)

    return laserProject

def half_way():

    offset = 25

    points_left = [[0, 3], [6, 3]]
    points_right = [[1,0],[1, 1], [6, 1]]

    laserProject = LaserProject()
    tile_size = 25

    # Multiply the points by the tile size for x
    points_left = [[x * tile_size for x in point] for point in points_left]
    points_right = [[x * tile_size for x in point] for point in points_right]

    laserObject = LaserObject(400, 600, 1)
    laserObject.location = (offset, offset)
    laserObject.priority = 10

    # Identify endpoints
    left_start, left_end = points_left[0], points_left[-1]
    right_start, right_end = points_right[0], points_right[-1]

    # Determine shortest connections (assuming straight lines for simplicity)
    # We calculate distances between each possible pair of endpoints and choose the shortest
    distances = {
        "left_start-right_start": (left_start, right_start),
        "left_start-right_end": (left_start, right_end),
        "left_end-right_start": (left_end, right_start),
        "left_end-right_end": (left_end, right_end)
    }

    # Calculate actual distances
    actual_distances = {key: ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5 for key, (p1, p2) in
                        distances.items()}

    # Find the shortest connection
    shortest_connection = min(actual_distances, key=actual_distances.get)

    # Depending on the shortest connection, order the points to form the polygon
    if shortest_connection == "left_start-right_start":
        polygon_points = points_left[::-1] + points_right
    elif shortest_connection == "left_start-right_end":
        polygon_points = points_left[::-1] + points_right[::-1]
    elif shortest_connection == "left_end-right_start":
        polygon_points = points_left + points_right
    else:  # "left_end-right_end"
        polygon_points = points_left + points_right[::-1]

    # Close the polygon by adding the first point at the end
    polygon_points.append(polygon_points[0])
    # laserObject.add_polygon(polygon_points)
    # laserObject.add_polygon(polygon_points)

    laserObject.add_polygon(points_right)
    laserObject.add_polygon(points_left)
    laserObject.add_polygon(polygon_points)

    # Create a polygon from the scaled points
    original_polygon = Polygon(polygon_points)
    buffer_distance = 5
    buffered_polygon = original_polygon.buffer(buffer_distance, join_style=2)
    buffered_polygon_coords = list(buffered_polygon.exterior.coords)

    # Draw around the original polygon
    outline = Polygon(polygon_points).buffer(10, join_style=2)
    outline_coords = list(outline.exterior.coords)

    laserObject.add_polygon(original_polygon.exterior.coords)
    buffer_distance = 5
    buffered_polygon = original_polygon.buffer(buffer_distance, join_style=2)
    buffered_polygon_coords = list(buffered_polygon.exterior.coords)

    laserObject.add_polygon(buffered_polygon_coords)

    # Now this buffer contains 2 edges that were added to close the polygon
    # Remove those edges

    # laserObject.add_polygon(outline_coords)
    print(buffered_polygon_coords)
    # now from the buffered polygon, remove the lines that were closing the polygon
    # buffered_polygon_coords.pop()

    print(buffered_polygon_coords)
    # laserObject.add_polygon(buffered_polygon_coords.copy())
    # move all buffered_polygon_coords 150 px up and to the right
    buffered_polygon_coords = [[50,50],[100,50],[150,50],[50,40]] # [[x + 2150, y + 2150] for x, y in buffered_polygon_coords]

    laserObject.add_polygon(buffered_polygon_coords)

    laserProject.laser_objects.append(laserObject)

    return laserProject

    # And split the polygon into two, right down the middle
    # Got trough each point in points_left, find the closest point in buffered_polygon_coords
    # and add that point to the new list, removed it from buffered_polygon_coords
    left_half = []

    for point in points_left:
        closest_point = min(buffered_polygon_coords, key=lambda x: ((x[0] - point[0]) ** 2 + (x[1] - point[1]) ** 2) ** 0.5)
        left_half.append(closest_point)
        buffered_polygon_coords.remove(closest_point)

    # do the same for the right half
    right_half = []

    for point in points_right:
        closest_point = min(buffered_polygon_coords, key=lambda x: ((x[0] - point[0]) ** 2 + (x[1] - point[1]) ** 2) ** 0.5)
        right_half.append(closest_point)
        buffered_polygon_coords.remove(closest_point)

    #laserObject.add_polygon(left_half)
    #laserObject.add_polygon(right_half)

    # And create LineString for both
    line = LineString(left_half)
    traced_line = line.buffer(5 / 2, cap_style=1, join_style=1)
    traced_line_coords = list(traced_line.exterior.coords)

    left_laserObject = LaserObject(2500, 300, 1)
    left_laserObject.add_polygon(traced_line_coords)
    left_laserObject.fill()
    left_laserObject.location = (offset, offset)
    left_laserObject.power_mode = "M4"
#    laserProject.laser_objects.append(left_laserObject)

    # And the second half
    line = LineString(right_half)
    traced_line = line.buffer(5 / 2, cap_style=1, join_style=1)
    traced_line_coords = list(traced_line.exterior.coords)

    right_laserObject = LaserObject(2500, 300, 1)
    right_laserObject.add_polygon(traced_line_coords)
    right_laserObject.fill()
    right_laserObject.location = (offset, offset)
    left_laserObject.power_mode = "M4"
 #   laserProject.laser_objects.append(right_laserObject)

    laserProject.laser_objects.append(laserObject)

    return laserProject

def foldable():

    # Create a foldable box
    laser_project = LaserProject()

    boxoutline = LaserObject(400, 600, 1)
    foldline = LaserObject(400, 600, 1)
    foldline.color = "red"

    # boxoutline.add_rectangle(0, 0, 50, 50)

    # Lets think about this functionality wise.
    # we have the width, we have the height and lenght
    x_size = 50
    y_size = 30
    z_size = 20

    # The base box is width x length
    points = [[0, 0], [0, y_size], [x_size, y_size], [x_size, 0], [0, 0]]
    foldline.add_polygon(points)

    # The front flap
    points = [[0, 0], [0, -z_size]]
    foldline.add_polygon(points)
    points = [[x_size, 0], [x_size, -z_size]]
    foldline.add_polygon(points)

    points = [[0, -z_size], [x_size, -z_size]]
    boxoutline.add_polygon(points)

    # The side flap left
    points = [[0, y_size], [-z_size/2, y_size+5], [-z_size/2, y_size+z_size-5], [0, y_size+z_size]]
    boxoutline.add_polygon(points)

    # The side flap right
    points = [[x_size, y_size], [x_size+z_size/2, y_size+5], [x_size+z_size/2, y_size+z_size-5], [x_size, y_size+z_size]]
    boxoutline.add_polygon(points)

    # The side flap left
    points = [[0, 0], [-z_size/2, -5], [-z_size/2, -z_size+5], [0, -z_size]]
    boxoutline.add_polygon(points)

    # And right
    points = [[x_size, 0], [x_size+z_size/2, -5], [x_size+z_size/2, -z_size+5], [x_size, -z_size]]
    boxoutline.add_polygon(points)

    # The back flap
    points = [[0, y_size], [0, y_size+z_size],[x_size, y_size+z_size], [x_size, y_size]]
    foldline.add_polygon(points)

    # The top
    points = [[0, y_size+z_size], [0, y_size+z_size+y_size]]
    boxoutline.add_polygon(points)
    points = [[x_size, y_size+z_size], [x_size, y_size+z_size+y_size]]
    boxoutline.add_polygon(points)

    points = [[0, y_size+z_size+y_size], [x_size, y_size+z_size+y_size]]
    foldline.add_polygon(points)

    # The top lid
    points = [[0, y_size+z_size+y_size], [5, y_size+z_size+y_size+10], [x_size-5, y_size+z_size+y_size+10], [x_size, y_size+z_size+y_size]]
    boxoutline.add_polygon(points)

    # The left flap
    points = [[0, 0], [-z_size, 0], [-z_size, y_size], [0, y_size]]
    boxoutline.add_polygon(points)

    # The right flap
    points = [[x_size, 0], [x_size+z_size, 0], [x_size+z_size, y_size], [x_size, y_size]]
    boxoutline.add_polygon(points)

    foldline.location = (20,20)
    foldline.priority = -10
    boxoutline.location = (20,20)

    foldline.dot_the_lines()

    laser_project.laser_objects.append(foldline)
    laser_project.laser_objects.append(boxoutline)

    return laser_project

def aoe():

    # Create an area of effect ring
    laserproject = LaserProject()

    n = 0.75

    laserobject = LaserObject(400, 500, 2)
    laserobject.add_circle(n*25, n*25, 18.5/2)
    laserobject.add_circle(n*25, n*25, 18.5/2 + 4)
    laserobject.location = (0, 0)

    text = LaserTextObject("Stunned", "../Ubuntu-R.ttf", 9, 2500, 300, passes=1)

    aoa = text.convert_to_laser_object()
    distribute_groups_around_circle(aoa, 18.5/2 + 4, 8)

    # text.location =(n*25,n*25)
    # increase text location by 25
    # text.location = (text.location[0] + 25, text.location[1] + 25)

    text.fill()

    laserproject.laser_objects.append(aoa)
    laserproject.laser_objects.append(laserobject)

    return laserproject

def corner_room():

    # Create a corner room
    laser_project = LaserProject()

    laser_object = LaserObject(400, 600, 1)
    laser_object.priority = 10

    points= [[0,0],[0,5],[4,5],[4,1],[2,1],[2,4],[1,4],[1,0]]
    points = scale_to_tile_size(points, 25)

    laser_object.add_polygon(points)

    traced = get_outlines_for_single_line(points)

    traced_object = LaserObject(2500, 300, 1)
    traced_object.add_polygon(traced)
    traced_object.color = "red"

    laser_project.laser_objects.append(traced_object)

    outline_coords = get_cut_line_for_single_line(points)
    laser_object.add_polygon(outline_coords)

    laser_project.laser_objects.append(laser_object)

    return laser_project

def room():

    laser_project = LaserProject()
    laser_project.laser_objects +=  create_square_room(6)

    return laser_project

def create_square_room(width):
    # Initial setup
    speed = 600
    power = 850
    passes = 16
    m = 0
    z = 0

    # Create LaserObject instances
    walls = LaserObject(speed, power, passes)
    frame = LaserObject(speed, power, passes)
    door = LaserObject(speed, power, passes)
    drawings = LaserObject(1200, 200, 1)

    # Set priorities
    walls.priority = 0
    drawings.priority = 10
    door.priority = 5

    # First set of operations
    wall = tabbed_wall(width)
    walls.add_polygon(move(wall[0], m, z))
    items = wall[1]
    for item in items:
        drawings.add_polygon(move(item, m, z))

    # Adjust z and repeat for different wall types and positions
    z = 27
    wall = slotted_wall(width)
    walls.add_polygon(move(wall[0], m, z))
    items = wall[1]
    for item in items:
        drawings.add_polygon(move(item, m, z))

    z = 54
    wall = tabbed_wall(width)
    walls.add_polygon(move(wall[0], m, z))
    items = wall[1]
    for item in items:
        drawings.add_polygon(move(item, m, z))

    z = 81
    models = double_door(width, style="slotted", position=(width-2)/2)
    door_frame = [models[0], models[1]]
    frame.add_polygon(move(door_frame[0], m, z))
    door.add_polygon(move(door_frame[1], m, z))
    items = models[2]
    for item in items:
        drawings.add_polygon(move(item, m, z))

    # Return the LaserObject instances
    return walls, frame, door, drawings

def broom():

    speed = 600
    power = 850
    passes = 16

    m = 6
    z = 0

    walls = LaserObject(speed, power, passes)
    frame = LaserObject(speed, power, passes)
    door = LaserObject(speed, power, passes)
    drawings = LaserObject(1200, 200, 1)

    walls.priority = 0
    drawings.priority = 10
    door.priority = 5

    wall = tabbed_wall(3)
    walls.add_polygon(move(wall[0], m, z))
    items = wall[1]

    for item in items:
        drawings.add_polygon(move(item, m, z))

    z = 27

    wall = slotted_wall(3)
    walls.add_polygon(move(wall[0], m, z))
    items = wall[1]

    for item in items:
        drawings.add_polygon(move(item, m, z))

    z = 54

    wall = tabbed_wall(3)
    walls.add_polygon(move(wall[0], m, z))
    items = wall[1]

    for item in items:
        drawings.add_polygon(move(item, m, z))

    z = 81

    models = single_door(3, style="slotted", position = 1)

    door_frame = [models[0], models[1]]
    frame.add_polygon(move(door_frame[0],m,z))
    door.add_polygon(move(door_frame[1],m,z))

    items = models[2]

    for item in items:
        drawings.add_polygon(move(item, m,z))

    # second room

    m = 93
    z = 0

    wall = tabbed_wall(3)
    walls.add_polygon(move(wall[0], m, z))
    items = wall[1]

    for item in items:
        drawings.add_polygon(move(item, m, z))

    z = 27

    wall = slotted_wall(3)
    walls.add_polygon(move(wall[0], m, z))
    items = wall[1]

    for item in items:
        drawings.add_polygon(move(item, m, z))

    #walls.add_polygon( move(tabbed_wall(3), 25, y = 27))
    #walls.add_polygon( move(tabbed_wall(3), 25, y = 54))

    z = 54

    wall = tabbed_wall(3)
    walls.add_polygon(move(wall[0], m, z))
    items = wall[1]

    for item in items:
        drawings.add_polygon(move(item, m, z))

    z = 81

    models = single_door(3, style="slotted", position = 1)
    #
    # # door_frame = rotate_sublists_points_180([models[0], models[1]])
    door_frame = [models[0], models[1]]
    frame.add_polygon(move(door_frame[0],m,z))
    door.add_polygon(move(door_frame[1],m,z))

    items = models[2]

    for item in items:
        drawings.add_polygon(move(item, m,z))

    ##

    laser_project = LaserProject()
    laser_project.laser_objects.append(frame)
    laser_project.laser_objects.append(door)
    laser_project.laser_objects.append(drawings)
    laser_project.laser_objects.append(walls)

    return laser_project


def bigroom():

    speed = 600
    power = 850
    passes = 16

    walls = LaserObject(speed, power, passes)
    prio_walls = LaserObject(speed, power, passes)
    prio_walls.priority = 10

    walls.add_polygon( move(slotted_wall(4), 25))
    walls.add_polygon( move(tabbed_wall(5), 25, y = 27))
    walls.add_polygon( move(tabbed_wall(5), 25, y = 54))

    walls.add_polygon(move(slotted_wall(1, configuration="r"), 25, y=81))
    walls.add_polygon(move(slotted_wall(1, configuration="r"), 55, y=81))

    tb_wall = insert_tabbed_wall(0.75, configuration="-r")

    x = 86
    prio_walls.add_polygon(move(tb_wall[0], x, y=81))
    prio_walls.add_polygon(move(tb_wall[1], x, y=81))
    walls.add_polygon(move(tb_wall[2], x, y=81))

    x += 26
    prio_walls.add_polygon(move(tb_wall[0], x, y=81))
    prio_walls.add_polygon(move(tb_wall[1], x, y=81))
    walls.add_polygon(move(tb_wall[2], x, y=81))

    x += 26
    prio_walls.add_polygon(move(tb_wall[0], x, y=81))
    prio_walls.add_polygon(move(tb_wall[1], x, y=81))
    walls.add_polygon(move(tb_wall[2], x, y=81))

    prio_walls.add_polygon(move(tb_wall[0], 137))
    prio_walls.add_polygon(move(tb_wall[1], 137))
    walls.add_polygon(move(tb_wall[2], 137 ))

    #walls.add_polygon( move(slotted_wall(9), y=27))

    #walls.add_polygon(move(slotted_wall(2), y=54))
    #walls.add_polygon(move(slotted_wall(6), 56, y=54))
    #walls.add_polygon(move(single_slotted_wall(), 212, y=54))

    # Create a door
    # frame_door = one_tile_door()
    # frame = LaserObject(speed, power, passes)
    # frame.add_polygon(frame_door[0])
    # frame.location = (25, 0)
    #
    # door = LaserObject(speed, power, passes+4)
    # door.add_polygon(frame_door[1])
    # door.location = (25, 0)
    #
    # framet = LaserObject(speed, power, passes)
    # framet.add_polygon(frame_door[0])
    # framet.location = (36, 0)
    #
    # doort = LaserObject(speed, power, passes+4)
    # doort.add_polygon(frame_door[1])
    # doort.location = (36, 0)
    #
    # framet.priority = 12
    # frame.priority = 12
    #
    # # 3 x 3
    # # walls.add_polygon(tabbed_wall(1))
    # # walls.add_polygon(move(tabbed_wall(1),x=25+7))
    # # walls.location = (4, 0)
    # #
    # # walls.add_polygon(move(slotted_wall(3), x=30+30))
    #
    laser_project = LaserProject()
    #laser_project.laser_objects.append(walls)
    #laser_project.laser_objects.append(prio_walls)
    #laser_project.laser_objects.append(door)
    #laser_project.laser_objects.append(frame)
    #laser_project.laser_objects.append(doort)
    #laser_project.laser_objects.append(framet)

    drawings = LaserObject(1200, 200, 1)
    door = LaserObject(speed, power, passes)
    frame = LaserObject(speed, power, passes)

    drawings.priority = 10
    door.priority = 8
    frame.priority = 5

    m = 3
    z = 28

    # models = double_door(10, style="tabs", position = 2)
    # frame.add_polygon(move(models[1],m))
    #
    # door.add_polygon(move(models[0],m))
    #
    # for item in models[2]:
    #     drawings.add_polygon(move(item,m))

    m = 6
    z = 0
    models = double_door(6, style="slotted", position = 2)

    # door_frame = rotate_sublists_points_180([models[0], models[1]])
    door_frame = [models[0], models[1]]
    frame.add_polygon(move(door_frame[0],m,z))
    door.add_polygon(move(door_frame[1],m,z))

    # items = rotate_sublists_points_180(models[2])
    items = models[2]

    for item in items:
        drawings.add_polygon(move(item, m,z))

    laser_project.laser_objects.append(frame)
    laser_project.laser_objects.append(door)
    laser_project.laser_objects.append(drawings)

    return laser_project

def xroom():

    speed = 600
    power = 850
    passes = 20

    x_size = 3

    # Create a room with a door, first of all create the three normal walls
    back_wall = LaserObject(speed, power, passes)
    points = create_tabbed_wall(x_size, 25, 2, 25, 4, 0.25)

    back_wall.location = (4+0.25, 0)
    back_wall.add_polygon(points)

    # Side walls
    side_wall = LaserObject(speed, power, passes)
    points = create_slotted_wall(x_size, 25, 2, 25, 4, 0.25)

    side_wall.location = (4+0.25, 25+2)
    side_wall.add_polygon(points)

    # Not translate the points, move the Y up by 26 points
    points = [[x, y + 27] for x, y in points]
    side_wall.add_polygon(points)

    # Corridor walls
    corridor_wall = LaserObject(speed, power, passes)
    points = create_tabbed_wall(1, 25, 2, 25, 4, 0.25, inside=True)
    corridor_wall.add_polygon(points)
    points = [[x+38, y] for x, y in points]
    corridor_wall.add_polygon(points)
    corridor_wall.location = (4+.25,81)

    points = create_slotted_wall(1, 25, 2, 25, 4, 0.25, inside=True)
    points = [[x+74, y] for x, y in points]
    corridor_wall.add_polygon(points)
    points = [[x+8, y - 27] for x, y in points]
    corridor_wall.add_polygon(points)

    laser_project = LaserProject()
    laser_project.laser_objects.append(back_wall)
    laser_project.laser_objects.append(side_wall)
    laser_project.laser_objects.append(corridor_wall)

    # Create a door
    frame = LaserObject(speed, power, passes)
    points = [[0, 0], [0, 4.33], [-4.25, 4.33], [-4.25, 10.33], [0, 10.33], [0, 14.67], [-4.25, 14.67], [-4.25, 20.67], [0, 20.67], [0.0, 33.3], [0.1, 34.2], [0.2, 34.9], [0.3, 35.6], [0.5, 36.3], [0.6, 37.0], [0.8, 37.6], [1.1, 38.3], [1.4, 38.9], [1.6, 39.6], [2.0, 40.2], [2.3, 40.8], [2.7, 41.4], [3.1, 41.9], [3.5, 42.5], [3.9, 43.0], [4.4, 43.5], [4.8, 43.9], [5.3, 44.3], [5.8, 44.7], [6.4, 45.1], [6.9, 45.5], [7.5, 45.8], [8.0, 46.0], [8.6, 46.3], [9.2, 46.5], [9.8, 46.6], [10.4, 46.8], [11.1, 46.9], [11.7, 46.9], [12.5, 46.9], [13.3, 46.9], [13.9, 46.9], [14.6, 46.8], [15.2, 46.6], [15.8, 46.5], [16.4, 46.3], [17.0, 46.0], [17.5, 45.8], [18.1, 45.5], [18.6, 45.1], [19.2, 44.7], [19.7, 44.3], [20.2, 43.9], [20.6, 43.5], [21.1, 43.0], [21.5, 42.5], [21.9, 41.9], [22.3, 41.4], [22.7, 40.8], [23.0, 40.2], [23.4, 39.6], [23.6, 38.9], [23.9, 38.3], [24.2, 37.6], [24.4, 37.0], [24.5, 36.3], [24.7, 35.6], [24.8, 34.9], [24.9, 34.2], [25.0, 33.3], [25.0, 20.67], [29.25, 20.67], [29.25, 14.67], [25.0, 14.67], [25.0, 10.33], [29.25, 10.33], [29.25, 4.33], [25.0, 4.33], [25.0, 0.0], [0.0, 0.0]]
    frame.add_polygon(points)

    door = LaserObject(speed, power, passes)
    points = [[12.5, 44.4], [13.2, 44.4], [13.6, 44.3], [14.1, 44.3], [14.6, 44.2], [15.0, 44.0], [15.5, 43.9], [15.9, 43.7], [16.4, 43.5], [16.8, 43.3], [17.2, 43.0], [17.6, 42.7], [18.1, 42.4], [18.4, 42.0], [18.8, 41.7], [19.2, 41.3], [19.6, 40.9], [19.9, 40.4], [20.2, 40.0], [20.5, 39.5], [20.8, 39.0], [21.1, 38.5], [21.3, 37.9], [21.5, 37.4], [21.7, 36.8], [21.9, 36.2], [22.1, 35.7], [22.2, 35.1], [22.3, 34.5], [22.4, 33.9], [22.5, 33.2], [22.5, 32.4], [22.5, 2.1], [12.5, 2.1], [2.5, 2.1], [2.5, 32.4], [2.5, 33.2], [2.6, 33.9], [2.7, 34.5], [2.8, 35.1], [2.9, 35.7], [3.1, 36.2], [3.3, 36.8], [3.5, 37.4], [3.7, 37.9], [3.9, 38.5], [4.2, 39.0], [4.5, 39.5], [4.8, 40.0], [5.1, 40.4], [5.4, 40.9], [5.8, 41.3], [6.2, 41.7], [6.6, 42.0], [6.9, 42.4], [7.4, 42.7], [7.8, 43.0], [8.2, 43.3], [8.6, 43.5], [9.1, 43.7], [9.5, 43.9], [10.0, 44.0], [10.4, 44.2], [10.9, 44.3], [11.4, 44.3], [11.8, 44.4], [12.5, 44.4]]
    door.add_polygon(points)

    laser_project.laser_objects.append(door)
    laser_project.laser_objects.append(frame)
    frame.location = (94,0)
    door.location = (94,0)

    door.priority = 20

    return laser_project


def cut_wall():

    # Create a corner room
    laser_project = LaserProject()

    speed = 150 * 4
    power = 950
    passes = 4 * 3

    laser_object = LaserObject(speed, power, passes)
    laser_object.priority = -10

    width = 5
    height = 30
    tile_size = 25

    width *= tile_size
    corner_size = 5

    # Create a rectangle, with slanted edges on the side
    points = [[0, 0],
              [0, height-corner_size],
              [corner_size, height],
              [width-corner_size, height],
              [width, height-corner_size],
              [width, 0],
              [0, 0]]

    laser_object.add_polygon(points)

    # Now, consider we need slots to be able to set it up straight
    # We need to cut out a small part of the wall
    slot = LaserObject(speed, power, passes)

    # We need to place the slots half a tile size from the edge
    slot_width = 4
    slot_height = 6

    # Create a slot on the left side
    slot.add_rectangle(tile_size/2, corner_size, slot_width, slot_height)
    slot.add_rectangle(tile_size / 2, height-corner_size-slot_height, slot_width, slot_height)

    # create a slot on the right side
    slot.add_rectangle(width-tile_size/2-slot_width, corner_size, slot_width, slot_height)
    slot.add_rectangle(width-tile_size/2-slot_width, height-corner_size-slot_height, slot_width, slot_height)

    # create a slot in the middle
    slot.add_rectangle(width/2-(0.5*slot_width), corner_size, slot_width, slot_height)
    slot.add_rectangle(width/2-(0.5*slot_width), height-corner_size-slot_height, slot_width, slot_height)

    # Now create the supports
    support = LaserObject(speed, power, passes)
    support.location = (width+slot_width+2, 0)

    tab_width = slot_width + 0.5

    # A support is half a tile size wide and the same height as the wall
    points = [[0, 0],

              [0, corner_size],
              [-tab_width, corner_size],
              [-tab_width, corner_size+slot_height],
              [0, corner_size + slot_height],

              [0, height-corner_size-slot_height],
              [-tab_width, height-corner_size-slot_height],
              [-tab_width, height-corner_size],
              [0, height-corner_size],

              [0, height],
              [corner_size, height],
              [tile_size/2+corner_size, corner_size],
              [tile_size / 2 + corner_size, 0],
              [0, 0]]

    support.add_polygon(points)

    support_r = LaserObject(speed, power, passes)
    support_r.location = (width+slot_width+4+tile_size, height)

    points = [[0, 0],

              [0, -corner_size],
              [tab_width, -corner_size],  # Flipped both x and y
              [tab_width, -(corner_size + slot_height)],  # Flipped both x and y
              [0, -(corner_size + slot_height)],

              [0, -(height - corner_size - slot_height)],
              [tab_width, -(height - corner_size - slot_height)],  # Flipped both x and y
              [tab_width, -(height - corner_size)],  # Flipped both x and y
              [0, -(height - corner_size)],

              [0, -height],
              [-corner_size, -height],  # Flipped both x and y
              [-(tile_size / 2 + corner_size), -corner_size],  # Flipped both x and y
              [-(tile_size / 2 + corner_size), 0],  # Flipped both x and y
              [0, 0]]

    support_r.add_polygon(points)

    #laser_project.laser_objects.append(slot)
    #laser_project.laser_objects.append(laser_object)

    #laser_project.laser_objects.append(support)
    #laser_project.laser_objects.append(support_r)

    # Make some copies!
    for i in range(2):

        instance = LaserObject(speed, power, passes)
        instance.shapes = slot.shapes.copy()
        instance.location = (0, (height + 2) * i )

        laser_project.laser_objects.append(instance)

        instance = LaserObject(speed, power, passes)
        instance.shapes = laser_object.shapes.copy()
        instance.location = (0, (height + 2) * i )

        laser_project.laser_objects.append(instance)
        print(i)

    # Make some copies!
    row = 2
    for i in range(4):

        instance = LaserObject(speed, power, passes)
        instance.shapes = support.shapes.copy()
        instance.location = ((tab_width) + (i * (tile_size + tab_width + tab_width+ tab_width)), row * (height + 2 ))

        laser_project.laser_objects.append(instance)

        instance = LaserObject(speed, power, passes)
        instance.shapes = support_r.shapes.copy()
        instance.location = ((tile_size + tab_width + 2) + (i * ((tile_size + tab_width + tab_width + tab_width ))), height + row * (height + 2 ))

        laser_project.laser_objects.append(instance)

    laser_project.laser_objects.pop()

    return laser_project

def newbox():

    speed = 600
    power = 850
    passes = 16

    box = LaserObject(speed, power, passes)

    position_x = 0
    num_slots = 3
    slot = 4
    spacing = 5

    # Assuming a length that can fit 3 slots with intervals and slot width of 4mm
    box_length = 3 * (4 + 4) + 2 * 3.5  # 3 slots, 2 intervals of 4mm each, and 4mm clearance on each side
    box_width = 50  # No slots on this edge, so it's straight

    # Generate the cutout pattern
    slot_cutout_polygon = generate_box_with_slots(36, 3, 5, 5)

    # Convert the polygon points to a list
    box.add_polygon( slot_cutout_polygon[0])
    box.add_polygon(slot_cutout_polygon[1])

    #box.add_rectangle(0, 0, 46, 46)

    laser_project = LaserProject()
    laser_project.laser_objects.append(box)

    return laser_project

def  box():

    # This is try out half cutting
    speed = 600
    power = 850
    passes = 4

    # laser_project = LaserProject()
    # box = LaserObject(speed, power, passes)
    # box.add_rectangle(0,0,40,4)
    # box.fill()
    # laser_project.laser_objects.append(box)
    #
    # return laser_project

    speed = 600
    power = 850
    passes = 16

    # Create a box
    laser_project = LaserProject()

    base = 41
    divider = 4

    width = divider + base + base + base + divider + divider + divider
    height = divider + base + divider + base + divider + divider + divider

    box = LaserObject(speed, power, passes)
    # width = 140
    points = finger_jointed_box(width, height, 3, 2)

    # box.add_rectangle(0, 0, width, height)
    box.add_polygon(points)
    box.location = (0, 0)

    bases = LaserObject(speed, power, passes)
    bases.add_rectangle(divider+divider, divider+divider, base, base)
    bases.add_rectangle(divider+divider+base, divider+divider, base, base)
    bases.add_rectangle(divider+divider + base + base, divider+divider, base, base)

    bases.add_rectangle(divider+divider, base+divider+divider+divider, base, base)
    bases.add_rectangle(divider+divider+base, base+divider+divider+divider, base, base)
    bases.add_rectangle(divider+divider + base + base, base+divider+divider+divider, base, base)

    # Create a slot in the center
    slot = LaserObject(speed, power, passes)
    slot.priority = 20

    slots_across = 2
    slots_space = slots_across * 6
    space_left = width - slots_space
    space_between_tabs = space_left / (slots_across + 1)
    slot_height = 6

    for i in range(1, slots_across + 1):
        tab_start_x = space_between_tabs * i + slot_height * (i - 1)
        slot.add_rectangle(tab_start_x, height-8, 6, 4)
        slot.add_rectangle(tab_start_x, 4, 6, 4)

    slots_across = 3
    slots_space = slots_across * 6
    space_left = width - slots_space
    space_between_tabs = space_left / (slots_across + 1)
    slot_height = 6

    for i in range(1, slots_across + 1):
        tab_start_x = space_between_tabs * i + slot_height * (i - 1)
        slot.add_rectangle(tab_start_x, height/2-2, 6, 4)

  #   laser_project.laser_objects.append(box)
#    laser_project.laser_objects.append(bases)

    # Get a side
    side = finger_jointed_side(width, 10, 3, 2)
    sides = LaserObject(speed, power, passes)
    sides.add_polygon(side)

    side = finger_jointed_side(width, 10, 2, 2)
    sides.add_polygon(move(side, y=28))

    # rotate side points 180 degrees
    side = [[-x, -y] for x, y in side]

    sides.add_polygon(move(side, x=width, y=26))
    #sides.location = (0, 102)
    laser_project.laser_objects.append(sides)

    points = finger_jointed_lid(width, 90, 3, 2)
    backside = LaserObject(speed, power, passes)
    backside.add_polygon(points)
    backside.location = (0,110)

    points = finger_jointed_side_alt(height, 90, 2, 2)
    backside.add_polygon(move(points, width + 8))

    #laser_project.laser_objects.append(backside)

    return laser_project

def import_csv():

    from blender_import  import import_csv as ic

    polygons = ic()

    laser_project = LaserProject()

    speed = 600
    power = 850
    passes = 1

    laser_object = LaserObject(speed, power, passes)

    # These polygons have the wrong scale, multiply by 10
    polygons = [scale_to_tile_size(polygon, 10) for polygon in polygons]

    laser_project.laser_objects.append(laser_object)
    main = polygons.pop()

    for polygon in polygons:
        laser_object.add_polygon(move(polygon, 120))

    from gameboxes import finger_joints_vertical, finger_joints_horizontal

    slots = 3
    new = cut_top(main)

    # get the max x from main
    width = max([x for x, y in main])

    top = finger_joints_horizontal(width, 2, slots, direction="top")
    new = replace_top(new, top)

    side = finger_joints_vertical(110, 0, slots, slots=False, side="right")
    new = cut_side(new, "right", move_ends=True)
    new = replace_side(new, side, direction="right")

    side = finger_joints_vertical(110, 0, slots, slots=False, side="left")
    new = cut_side(new, "left", move_ends=True)
    new = replace_side(new, side, direction="left")

    laser_object.add_polygon(move(new, 120))

    # Okay, so the thing is done, save it I guess, lets make a file and store it
    filename = "towerside.json"

    laser_object.load_shapes(filename)


    return laser_project

def old_import_csv():

    filename = "/mnt/d/vertices.csv"

    # This a csv file, it has the format of an identifier and 2 coordinates on each line
    import csv

    # Open the CSV file for reading
    polygons = list()

    with open(filename, 'r') as csvfile:
        # Create a CSV reader object
        reader = csv.reader(csvfile)
        # Iterate over each row in the CSV
        polygon = None
        polygon_id = None

        for row in reader:
            current_id = int(row[0])
            if polygon_id != current_id:
                if polygon:
                    polygons.append(polygon)
                polygon = list()

                polygon_id = current_id

            edge = (float(row[1]), float(row[2]), float(row[3]), float(row[4]))

            polygon.append(edge)

        polygons.append(polygon)

    laser_project = LaserProject()

    speed = 600
    power = 850
    passes = 20

    # Now we have a list of edges, we need to convert these to a path, ie, a list of vertices
    polygons = [convert_into_vertices(polygon) for polygon in polygons]
    #polygons = [convert_into_lines(polygon) for polygon in polygons]

    # Flatten the list of polygons one step
    #polygons = [edge for polygon in polygons for edge in polygon]

    # back to what it was

    # Now, order the the polygons so that they are in the correct order, smallest to largest by length of path
    polygons = sorted(polygons, key=lambda x: len(x))

    # Now the coordinates are way over the grid, we need to find the lower left corner and move all the coordinates to account for that
    min_x = min([min([x[0] for x in polygon]) for polygon in polygons])
    min_y = min([min([x[1] for x in polygon]) for polygon in polygons])

    # Move all the coordinates to account for the lower left corner
    polygons = [[(x - min_x, y - min_y) for x, y in polygon] for polygon in polygons]

    # The coordinates are too small, multiply by 10
    polygons = [scale_to_tile_size(polygon, 10) for polygon in polygons]

    order = len(polygons)
    points = polygons[0]
    d = 0.5

    cutouts = []
    #
    # original_polygon = Polygon(points)
    # # Create the cutout 1 unit inside the original polygon
    # inner_cutout_polygon = original_polygon.buffer(-d)
    # # Get the exterior coordinates of the inner cutout
    # inner_cutout_points = list(inner_cutout_polygon.exterior.coords)
    #
    # cutouts.append(inner_cutout_points)
    # points = polygons[1]
    #
    # original_polygon = Polygon(points)
    # # Create the cutout 1 unit inside the original polygon
    # inner_cutout_polygon = original_polygon.buffer(d)
    # # Get the exterior coordinates of the inner cutout
    # inner_cutout_points = list(inner_cutout_polygon.exterior.coords)
    #
    # cutouts.append(inner_cutout_points)
    #
    # polygons = cutouts

    # Now the coordinates are way over the grid, we need to find the lower left corner and move all the coordinates to account for that
    min_x = min([min([x[0] for x in polygon]) for polygon in polygons])
    min_y = min([min([x[1] for x in polygon]) for polygon in polygons])

    # Move all the coordinates to account for the lower left corner
    polygons = [[(x - min_x, y - min_y) for x, y in polygon] for polygon in polygons]

    # Now find the center of the all the polygons and move them so that the center becomes x=25
    center_x = sum([sum([x[0] for x in polygon]) for polygon in polygons]) / sum([len(polygon) for polygon in polygons])
    polygons = [[(x - center_x + 25, y) for x, y in polygon] for polygon in polygons]

    # not raise the Y value of all these polyons by d
    polygons = [[(x, y+d) for x, y in polygon] for polygon in polygons]

    # And round all the values to 2 decimal places
    polygons = [[(round(x, 1), round(y, 1)) for x, y in polygon] for polygon in polygons]

    laser_object = LaserObject(speed, power, passes)
    for polygon in polygons:

        laser_object.add_polygon(polygon)
        print(polygon)

    print(polygons)

    laser_project.laser_objects.append(laser_object)

    print(laser_object.shapes)

    return laser_project


def get_outlines_for_single_line(points, distance=4):

    # Create a polygon from the scaled points
    original_polygon = Polygon(points)
    buffer_distance = distance
    buffered_polygon = original_polygon.buffer(buffer_distance, join_style=2)
    buffered_polygon_coords = list(buffered_polygon.exterior.coords)

    # remove the last point, so it's no longer closed
    buffered_polygon_coords.pop()

    # Create a LineString from the scaled points to represent the original polygon as a line
    line = LineString(buffered_polygon_coords)
    traced_line = line.buffer(distance / 2, cap_style=1, join_style=1)
    traced_line_coords = list(traced_line.exterior.coords)

    return traced_line_coords

def get_cut_line_for_single_line(points):

    # Close the original polygon
    points.append(points[0])

    # Draw around the original polygon
    outline = Polygon(points).buffer(12.5, join_style=2)
    outline_coords = list(outline.exterior.coords)

    return outline_coords

def scale_to_tile_size(points, tile_size):

    # Multiply the points by the tile size for x
    points = [[x * tile_size for x in point] for point in points]

    # Round them all to 3 decimal place
    points = [[round(x, 1) for x in point] for point in points]

    return points


def find_polygon(start_edge, edges):
    polygon = [start_edge]
    current_edge = start_edge

    while True:
        for edge in edges:
            if edge == current_edge:
                continue  # Skip the current edge itself

            # Check if the current edge connects to the next edge
            if current_edge[2:] == edge[:2]:
                polygon.append(edge)
                current_edge = edge
                break
            elif current_edge[2:] == edge[2:]:
                # If the edge is in the reverse direction
                polygon.append((edge[2], edge[3], edge[0], edge[1]))
                current_edge = (edge[2], edge[3], edge[0], edge[1])
                break
        else:
            # No more connected edges found
            break

        # Check if the polygon is closed
        if polygon[0][:2] == polygon[-1][2:]:
            return polygon

    return None


def convert_into_vertices(edges):
    if not edges:
        return []

    # Start with the first edge and add its starting vertex
    path = [edges[0][:2]]  # Add the starting point of the first edge
    current_point = edges[0][2:]  # The ending point of the first edge becomes the current point

    # Remove the first edge from the list
    remaining_edges = edges[1:]

    while remaining_edges:
        for i, edge in enumerate(remaining_edges):
            if edge[:2] == current_point:  # If the start of the edge connects
                path.append(edge[:2])
                current_point = edge[2:]
                del remaining_edges[i]
                break
            elif edge[2:] == current_point:  # If the end of the edge connects (but is in reverse)
                path.append(edge[2:])
                current_point = edge[:2]
                del remaining_edges[i]
                break
        else:
            # No more connecting edges found
            break

    # Add the last point
    path.append(current_point)

    return path


def convert_into_lines(edges):
    if not edges:
        return []

    # Each edge is a joined line, so we can just return the edges
    path = []
    for edge in edges:
        line = []
        line.append(edge[:2])
        line.append(edge[2:])

        path.append(line)

    return path


def separate_into_polygons(edges):
    polygons = []
    remaining_edges = edges[:]

    while remaining_edges:
        start_edge = remaining_edges.pop(0)
        polygon = find_polygon(start_edge, remaining_edges)

        if polygon:
            polygons.append(polygon)
            # Remove used edges from remaining_edges
            for edge in polygon:
                if edge in remaining_edges:
                    remaining_edges.remove(edge)
                # Also check for edge in reverse direction
                reverse_edge = (edge[2], edge[3], edge[0], edge[1])
                if reverse_edge in remaining_edges:
                    remaining_edges.remove(reverse_edge)

    return polygons


def calculate_perimeter(path):
    """Calculate the perimeter of a polygon given its path."""
    perimeter = 0
    for i in range(len(path)):
        # Calculate the distance between consecutive vertices, wrapping around to the start
        dx = path[i][0] - path[i-1][0]
        dy = path[i][1] - path[i-1][1]
        distance = (dx**2 + dy**2)**0.5
        perimeter += distance
    return perimeter

def move(points, x=0, y=0):

    n = x
    o = y

    points = [[x + n, y + o] for x, y in points]

    return points

def rotate(points):
    min_x = min(points, key=lambda point: point[0])[0]
    min_y = min(points, key=lambda point: point[1])[1]
    max_x = max(points, key=lambda point: point[0])[0]
    max_y = max(points, key=lambda point: point[1])[1]

    # Calculate the shift needed to keep the lower-left corner in place after rotation
    shift_x = max_x + min_x
    shift_y = max_y + min_y

    # Rotate points by 180 degrees around the origin, then translate to keep the lower-left corner the same
    rotated_translated_points = [(-(x - shift_x), -(y - shift_y)) for x, y in points]

    return rotated_translated_points

def rotate_90(points):
    # Find the bounding box of the original points
    min_x = min(points, key=lambda point: point[0])[0]
    min_y = min(points, key=lambda point: point[1])[1]
    max_x = max(points, key=lambda point: point[0])[0]
    max_y = max(points, key=lambda point: point[1])[1]

    # Rotate points 90 degrees counterclockwise around the origin
    rotated_points = [(-y, x) for x, y in points]

    # Find new bounds after rotation
    new_min_x = min(rotated_points, key=lambda point: point[0])[0]
    new_min_y = min(rotated_points, key=lambda point: point[1])[1]

    # Calculate the translation needed to align the new lower-left corner with the old one
    translate_x = min_x - new_min_x
    translate_y = min_y - new_min_y

    # Apply translation
    rotated_translated_points = [(x + translate_x, y + translate_y) for x, y in rotated_points]

    return rotated_translated_points

def rotate_sublists_points_180(points_lists):
    # Find the global lower-left corner across all sublists
    all_points = [point for sublist in points_lists for point in sublist]
    min_x = min(all_points, key=lambda point: point[0])[0]
    min_y = min(all_points, key=lambda point: point[1])[1]
    max_x = max(all_points, key=lambda point: point[0])[0]
    max_y = max(all_points, key=lambda point: point[1])[1]

    # Calculate the shift needed to keep the lower-left corner in place after rotation
    shift_x = max_x + min_x
    shift_y = max_y + min_y

    # Rotate and translate each sublist
    rotated_translated_lists = []
    for sublist in points_lists:
        rotated_translated_sublist = [(-(x - shift_x), -(y - shift_y)) for x, y in sublist]
        rotated_translated_lists.append(rotated_translated_sublist)

    return rotated_translated_lists

def generate_jointed_rectangle_points(width, height, slot_width, slot_height):
    # Assuming the width and height are divisible by slot_width * 2 for simplicity
    slots_across = width // (slot_width * 2)
    slots_tall = height // (slot_width * 2)

    points = []

    # Top edge
    for i in range(slots_across):
        points.extend([
            (i * 2 * slot_width, height),
            (i * 2 * slot_width + slot_width, height),
            (i * 2 * slot_width + slot_width, height - slot_height),
            ((i + 1) * 2 * slot_width, height - slot_height),
            ((i + 1) * 2 * slot_width, height),
        ])

    # Right edge
    for i in range(slots_tall):
        points.extend([
            (width, height - i * 2 * slot_width),
            (width, height - i * 2 * slot_width - slot_width),
            (width - slot_height, height - i * 2 * slot_width - slot_width),
            (width - slot_height, (height - (i + 1) * 2 * slot_width)),
            (width, (height - (i + 1) * 2 * slot_width)),
        ])

    # Bottom edge
    for i in range(slots_across):
        points.extend([
            (width - i * 2 * slot_width, 0),
            (width - i * 2 * slot_width - slot_width, 0),
            (width - i * 2 * slot_width - slot_width, slot_height),
            (width - (i + 1) * 2 * slot_width, slot_height),
            (width - (i + 1) * 2 * slot_width, 0),
        ])

    # Left edge
    for i in range(slots_tall):
        points.extend([
            (0, i * 2 * slot_width),
            (0, i * 2 * slot_width + slot_width),
            (slot_height, i * 2 * slot_width + slot_width),
            (slot_height, (i + 1) * 2 * slot_width),
            (0, (i + 1) * 2 * slot_width),
        ])

    return points


def finger_jointed_box(width, height, slots_across, slots_tall):

    slot_width = 4
    slot_height = 6

    # We start 0,0 and then go to 0,height
    # How many slots do we need to make, that is the space for the slots
    slots_space = slots_tall * slot_height
    space_left = height - slots_space

    # We need to divide the space left by the number of slots + 1 (top and bottom)
    space_between_tabs = space_left / (slots_tall + 1)

    # Dynamic points calculation starting from bottom left, moving up and then down the right side
    points = [[0, 0]]

    # Generating tab points dynamically on the left side
    for i in range(1, slots_tall + 1):
        tab_start_y = space_between_tabs * i + slot_height * (i - 1)
        points += [
            [0, tab_start_y],
            [slot_width , tab_start_y],  # Left side of the tab
            [slot_width , tab_start_y + slot_height],  # Bottom side of the tab
            [0, tab_start_y + slot_height],  # Right side of the tab
        ]

    # Add the top left corner

    slots_space = slots_across * slot_height
    space_left = width - slots_space
    space_between_tabs = space_left / (slots_across + 1)

    points += [[0, height]]

    for i in range(1, slots_across + 1):
        tab_start_x = space_between_tabs * i + slot_height * (i - 1)
        points += [
            [tab_start_x, height],
            [tab_start_x, height - slot_width],
            [tab_start_x + slot_height, height - slot_width],
            [tab_start_x + slot_height, height],
        ]

    points += [[width, height]]

    # okay, we have, the left and top, now we need to do the right and bottom
    # we can just mirror that
    # take all the points, and mirror them so the box is complete
    mirrored_points = [[width - x, height - y] for x, y in points]

    points += mirrored_points

    # Now we create the right side

    return points

def finger_jointed_side(width, height, slots_across, slots_tall):

    slot_width = 4
    slot_height = 6

    # We start 0,0 and then go to 0,height
    # How many slots do we need to make, that is the space for the slots
    slots_space = slots_tall * slot_height
    space_left = height - slots_space

    # We need to divide the space left by the number of slots + 1 (top and bottom)
    space_between_tabs = space_left / (slots_tall + 1)

    # Dynamic points calculation starting from bottom left, moving up and then down the right side
    slots_space = slots_across * slot_height
    space_left = width - slots_space
    space_between_tabs = space_left / (slots_across + 1)

    points = [[0, height]]

    for i in range(1, slots_across + 1):
        tab_start_x = space_between_tabs * i + slot_height * (i - 1)
        points += [
            [tab_start_x, height],
            [tab_start_x, height + slot_width],
            [tab_start_x + slot_height, height + slot_width],
            [tab_start_x + slot_height, height],
        ]

    points += [[width, height]]
    points += [[width, 0]]
    points += [[0, 0]]
    points += [[0, height]]

    # Now we create the right side

    return points

def finger_jointed_lid(width, height, slots_across, slots_tall):

    slot_width = 4
    slot_height = 6

    # We start 0,0 and then go to 0,height
    # How many slots do we need to make, that is the space for the slots
    slots_space = slots_tall * slot_height
    space_left = height - slots_space

    # We need to divide the space left by the number of slots + 1 (top and bottom)
    space_between_tabs = space_left / (slots_tall + 1)

    # Dynamic points calculation starting from bottom left, moving up and then down the right side
    points = [[0, 0]]

    # Generating tab points dynamically on the left side
    for i in range(1, slots_tall + 1):
        tab_start_y = space_between_tabs * i + slot_height * (i - 1)
        points += [
            [0, tab_start_y],
            [slot_width , tab_start_y],  # Left side of the tab
            [slot_width , tab_start_y + slot_height],  # Bottom side of the tab
            [0, tab_start_y + slot_height],  # Right side of the tab
        ]

    # Add the top left corner

    slots_space = slots_across * slot_height
    space_left = width - slots_space
    space_between_tabs = space_left / (slots_across + 1)

    points += [[0, height]]

    for i in range(1, slots_across + 1):
        tab_start_x = space_between_tabs * i + slot_height * (i - 1)
        points += [
            [tab_start_x, height],
            [tab_start_x, height + slot_width],
            [tab_start_x + slot_height, height + slot_width],
            [tab_start_x + slot_height, height],
        ]

    points += [[width, height]]

    # okay, we have, the left and top, now we need to do the right and bottom
    # we can just mirror that
    # take all the points, and mirror them so the box is complete
    mirrored_points = [[width - x, height - y] for x, y in points]

    points += mirrored_points

    # Now we create the right side

    return points

def finger_jointed_side_alt(width, height, slots_across, slots_tall):

    slot_width = 4
    slot_height = 6

    # We start 0,0 and then go to 0,height
    # How many slots do we need to make, that is the space for the slots
    slots_space = slots_tall * slot_height
    space_left = height - slots_space

    # We need to divide the space left by the number of slots + 1 (top and bottom)
    space_between_tabs = space_left / (slots_tall + 1)

    # Dynamic points calculation starting from bottom left, moving up and then down the right side
    points = [[0, 0]]
    bottom = []

    # Generating tab points dynamically on the left side
    for i in range(1, slots_tall + 1):
        tab_start_y = space_between_tabs * i + slot_height * (i - 1)
        points += [
            [0, tab_start_y],
            [-slot_width , tab_start_y],  # Left side of the tab
            [-slot_width , tab_start_y + slot_height],  # Bottom side of the tab
            [0, tab_start_y + slot_height],  # Right side of the tab
        ]

    # Add the top left corner

    slots_space = slots_across * slot_height
    space_left = width - slots_space
    space_between_tabs = space_left / (slots_across + 1)

    points += [[0, height]]

    for i in range(1, slots_across + 1):
        tab_start_x = space_between_tabs * i + slot_height * (i - 1)
        points += [
            [tab_start_x, height],
            [tab_start_x, height - slot_width],
            [tab_start_x + slot_height, height - slot_width],
            [tab_start_x + slot_height, height],
        ]

    points += [[width, height]]

    # okay, we have, the left and top, now we need to do the right and bottom
    # The right is a straight line
    points += [[width, 0]]

    # reverse bottom
    bottom = []

    for i in range(1, slots_across + 1):
        tab_start_x = space_between_tabs * i + slot_height * (i - 1)
        bottom += [
            [tab_start_x, 0],
            [tab_start_x, 0 - slot_width],
            [tab_start_x + slot_height, 0 - slot_width],
            [tab_start_x + slot_height, 0],
        ]

    # reverse bottom
    bottom = [[width - x, y] for x, y in bottom]

    # Make room for the inserts


    points += bottom
    points += [[0, 0]]

    return points


def generate_box_with_slots(width, num_slots, spacing, slot_width):
    # Initialize the list of points
    points = []
    indent = 2
    border = 4

    # Calculate the starting x position for the first slot
    start_x = 0

    # First point
    points += [
                [start_x - spacing/2, (width / 2) - indent],
                [start_x - spacing/2, 0],
                [start_x, 0]
                ]

    # Bottom edge slots
    for i in range(num_slots):
        # go down by the indent
        points += [
            [start_x, -indent],
            [start_x + slot_width, -indent],
            [start_x + slot_width, 0],
            [start_x + slot_width + spacing, 0]
            ]

        print(start_x + slot_width + spacing)
        start_x += slot_width + spacing
        print(start_x)

    start_x -= spacing / 2

    # The last point, need to replaced
    points.pop()

    # And the top left corner added
    points += [
        [start_x, 0],
        [start_x, (width/2)-indent],
    ]

    # Take all the points, mirror the y to complete
    mirrored_points = [[x, -y] for x, y in points]

    # And the move all the mirrored points up by width/2
    mirrored_points = [[x, y + width - indent] for x, y in mirrored_points]

    # Invert mirrored points
    mirrored_points = mirrored_points[::-1]
    mirrored_points.pop()

    # and the first point of points to the mirrored points
    mirrored_points.append(points[0])

    # Add to the points
    points += mirrored_points

    # Now the coordinates are way over the grid, we need to find the lower left corner and move all the coordinates to account for that
    min_x = min([x[0] for x in points])
    min_y = min([x[1] for x in points])

    # Move all the coordinates to account for the lower left corner
    points = [[x - min_x, y - min_y] for x, y in points]

    # Now get the max x and y
    max_x = max([x[0] for x in points])
    max_y = max([x[1] for x in points])

    # Move all the points by border
    points = [[x + border, y + border] for x, y in points]

    # And create 5 points around all this, the square around it
    square = [[0, 0], [max_x + 2 * border, 0], [max_x + 2 * border, max_y + 2 * border], [0, max_y + 2 * border], [0, 0]]

    return points, square

def cut_top(points, move_ends=False):

    # Check if the polygon is closed or not
    if points[0] == points[-1]:
        # Remove the last point, so it's no longer closed
        points.pop()

    # Search for the max-y value
    goal_y = max([x[1] for x in points])

    for i, point in enumerate(points):
        if point[1] == goal_y:
            # check if the next point is the same
            if points[i+1][1] == goal_y:
                # We've found the two points
                break

    # Anything up to point i is one side
    side_one = points[:i+1]

    # everything after i is the other side
    side_two = points[i+1:]

    # Start at side_two and add side_one
    points = side_two + side_one

    return points

def cut_side(points, direction="left", move_ends=False):

    # Check if the polygon is closed or not
    if points[0] == points[-1]:
        # Remove the last point, so it's no longer closed
        points.pop()

    if direction == "left":
        # Search for the min-x value
        goal_x = min([x[0] for x in points])

    if direction == "right":
        # Search for the min-x value
        goal_x = max([x[0] for x in points])

    for i, point in enumerate(points):
        if point[0] == goal_x:
            # check if the next point is the same
            if points[i+1][0] == goal_x:
                # We've found the two points
                break

    # Anything up to point i is one side
    side_one = points[:i+1]

    # everything after i is the other side
    side_two = points[i+1:]

    # Start at side_two and add side_one
    points = side_two + side_one

    if move_ends:

        if direction == "right":
            move_x = -gameboxes.material_thickness
        else:
            move_x = gameboxes.material_thickness

        points[0] = [points[0][0] + move_x, points[0][1]]
        points[-1] = [points[-1][0] + move_x, points[-1][1]]

        # if direction == "right":
        #     move_x = gameboxes.material_thickness * -1
        # else:
        #     move_x = gameboxes.material_thickness
        #
        # # move the first point by move_x
        # points[0] = [points[0][0] + move_x, points[0][1]]
        #
        # # move the last point by 5
        # points[-1] = [points[-1][0] - move_x, points[-1][1]]

    return points

def replace_side(main, side, direction="right"):

    # Take the first point of the main polygon, get the X-coordinate, that is the difference
    diff = main[0][0]

    # move the side polygon by diff
    side = [[x + diff, y] for x, y in side]

    # Check the direction
    if main[0][1] > main[-1][1]:
        main = main[::-1]

    if side[0][1] < side[-1][1]:
        side = side[::-1]

    main += side

    # Close the polygon if it is not closed
    if main[0] != main[-1]:
        main.append(main[0])

    return main

def replace_top(main, top):

    # Take the first point of the main polygon, get the Y-coordinate, that is the difference
    diff = main[0][1]

    # move the side polygon by diff
    top = [[x, y + diff] for x, y in top]

    # Check the direction
    if main[0][0] > main[-1][0]:
        main = main[::-1]

    top.pop(0)

    main.extend(top)

    return main






















