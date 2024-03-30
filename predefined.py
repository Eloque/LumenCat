from shapely import LineString

# This file will contain some predefined projects so they don't reside in tkGUI.py

from laserproject import LaserObject, LaserProject, LaserTextObject
from shapely.geometry import Polygon

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
    # text.location =(n*25,n*25)
    # increase text location by 25
    # text.location = (text.location[0] + 25, text.location[1] + 25)

    text.fill()

    laserproject.laser_objects.append(text)
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

def import_csv():

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

    speed = int(150 * 4 * 1.5)
    power = 950
    passes = int(4 * 3 * 1.5)

    speed = 100
    power = 950
    passes = 1

    speed = 600
    power = 850
    passes = 20

    # Now we have a list of edges, we need to convert these to a path, ie, a list of vertices
    polygons = [convert_into_vertices(polygon) for polygon in polygons]

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

    for polygon in polygons:
        laser_object = LaserObject(speed, power, passes)
        laser_object.priority = order
        laser_object.add_polygon(polygon)

        # laser_object.location = (64.5, 0)
        laser_project.laser_objects.append(laser_object)

        order -=1

    # laser_project.location = (64.5, 0)

    # We need to place the slots half a tile size from the edge
    slot_width = 4
    slot_height = 6
    corner_size = 5

    slot = LaserObject(speed, power, passes)
    slot.priority = 100
    tile_size = 25
    height = 30
    width = 125

    # Create a slot on the left side
    slot.add_rectangle(tile_size/2, corner_size, slot_width, slot_height)
    slot.add_rectangle(tile_size / 2, height-corner_size-slot_height, slot_width, slot_height)

    # create a slot on the right side
    slot.add_rectangle(width-tile_size/2-slot_width, corner_size, slot_width, slot_height)
    slot.add_rectangle(width-tile_size/2-slot_width, height-corner_size-slot_height, slot_width, slot_height)

    # laser_project.laser_objects.append(slot)

    return laser_project


def get_outlines_for_single_line(points):

    # Create a polygon from the scaled points
    original_polygon = Polygon(points)
    buffer_distance = 5
    buffered_polygon = original_polygon.buffer(buffer_distance, join_style=2)
    buffered_polygon_coords = list(buffered_polygon.exterior.coords)

    # remove the last point, so it's no longer closed
    buffered_polygon_coords.pop()

    # Create a LineString from the scaled points to represent the original polygon as a line
    line = LineString(buffered_polygon_coords)
    traced_line = line.buffer(5 / 2, cap_style=1, join_style=1)
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