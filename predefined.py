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

