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

    ##
    # Create a polygon from the scaled points
    original_polygon = Polygon(polygon_points)
    buffer_distance = 5
    buffered_polygon = original_polygon.buffer(buffer_distance, join_style=2)

    buffered_polygon_coords = list(buffered_polygon.exterior.coords)

    # laserObject.add_polygon(polygon_points)

    # Draw around the original polygon
    outline = Polygon(polygon_points).buffer(10, join_style=2)
    outline_coords = list(outline.exterior.coords)

    #laserObject.add_polygon(buffered_polygon_coords)

    # Now this buffer contains 2 edges that were added to close the polygon
    # Remove those edges


    # laserObject.add_polygon(outline_coords)
    print(buffered_polygon_coords)
    # now from the buffered polygon, remove the lines that were closing the polygon
    # buffered_polygon_coords.pop()

    print(buffered_polygon_coords)

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

def foldable():

    # Create a foldable box
    laserproject = LaserProject()

    laserobject = LaserObject(600, 250, 1)

    laserobject.add_rectangle(0, 20, 20, 2)
    laserobject.priority = 10
    laserobject.fill()
    laserproject.laser_objects.append(laserobject)

    boxoutline = LaserObject(400, 600, 1)
    boxoutline.add_rectangle(0, 0, 20, 40)

    laserproject.laser_objects.append(boxoutline)

    return laserproject

