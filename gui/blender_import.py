# This a csv file, it has the format of an identifier and 2 coordinates on each line
import csv
from shapely import Polygon

def import_csv():

    filename = "/mnt/d/vertices.csv"

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

    # Now we have a list of edges, we need to convert these to a path, ie, a list of vertices
    polygons = [convert_into_vertices(polygon) for polygon in polygons]

    # Now, order the the polygons so that they are in the correct order, smallest to largest by length of path
    polygons = sorted(polygons, key=lambda x: len(x))

    # Now the coordinates are way over the grid, we need to find the lower left corner and move all the coordinates to account for that
    min_x = min([min([x[0] for x in polygon]) for polygon in polygons])
    min_y = min([min([x[1] for x in polygon]) for polygon in polygons])

    print (min_x, min_y)

    # Move all the coordinates to account for the lower left corner, maintain 2 decimal places
    polygons = [[(round(x[0] - min_x, 2), round(x[1] - min_y, 2)) for x in polygon] for polygon in polygons]

    # Now sort it so, that the smallest polygon is first
    polygons = sorted(polygons, key=lambda x: len(x))

    return polygons

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

polygons = import_csv()

# # draw these polygons using import matplotlib.pyplot as plt
# import matplotlib.pyplot as plt
#
# print(polygons)
#
# list_of_polygons = polygons
#
# # Plotting with matplotlib
# plt.figure()
# for polygon_points in list_of_polygons:
#     plt.plot(*zip(*polygon_points), marker='o')  # Unzip the list of tuples into x and y coordinates
#
# # Set the aspect of the plot to be equal
# plt.gca().set_aspect('equal', adjustable='box')
#
# # Optionally create Shapely Polygons and work with them
# # For example, you can check the area or any other geometric properties
# polygons = [Polygon(points) for points in list_of_polygons]
# # Example of accessing properties: print(polygons[0].area)
#
# # Display the plot
# plt.show()