# We will have a class that can be used to covert SVG paths to GCode
# Per path object, we can set the speed and power of the laser
# This means that the class is en essence a list of SVG objects with a speed and power

# That would mean that there should be a class for SVG objects
import xml.etree.ElementTree as elementTree
from text import text_to_svg_path
from curvetopoints import quadratic_bezier
import re

# LaserProject is a collection of LaserObjects
class LaserProject:
    def __init__(self):
        self.laser_objects = list()
        self.shapes_as_points = None
        self.gcode = None
        self.gcode_header = None

        self.laser_mode = "M3" # M3 is constant power mode, M4 is PWM mode

    # Helper function, get a string representation of the SVG
    @staticmethod
    def load_from_svg_file(filename):

        # Open the file
        with open(filename, "r") as file:
            # Read the file
            svg = file.read()

            # Now we have the svg, we can parse it
            print(svg)

        return svg

    def get_svg(self):

        # First the header
        print('<?xml version="1.0" encoding="UTF-8"?>')
        print('<svg width="100%" height="100%" version="1.1" xmlns="http://www.w3.org/2000/svg">')

        for laserObject in self.laser_objects:

            svg = laserObject.get_svg_element()

            if type(svg) is list:
                for item in svg:
                    print(item)

            else:
                print(svg)

        print("</svg>")

    def get_gcode_header(self):

        # Create empty gcode list
        gcode = list()

        # Add the header
        gcode.append("; gCode created by LumenCat")
        gcode.append("; setting up machine basics")

        gcode.append("; G17 - XY plane")
        gcode.append("; G40 - cutter compensation off")
        gcode.append("; G21 - unit to mm")
        gcode.append("; G54 - work coordinate system 1")
        gcode.append("; G90 - absolute coordinates")

        gcode.append("G17 G40 G21 G54 G90")
        gcode.append("; air assist on")
        gcode.append("M8")

        gcode.append("; laser turned off")
        gcode.append("M3 S0")

        self.gcode_header = gcode

        return self.gcode_header

    # Convert all the laser objects to points, prior to converting to gcode
    def get_all_shapes_as_points(self):

        # Create empty list
        self.shapes_as_points = []

        # Go through the laser objects
        for laser_object in self.laser_objects:

            # Get the points for the object
            object_points = laser_object.get_shape_as_points()

            # Add the points to the list
            self.shapes_as_points.append(object_points)

        # Return the list
        return self.shapes_as_points

    # This is the original of the function
    def get_all_shapes_as_cartesian_points(self):

        shapes_as_cartesian_points = []

        # Go through the laser objects
        for laser_object in self.laser_objects:

            speed = laser_object.speed
            power = laser_object.power
            passes = laser_object.passes

            point_lists = laser_object.get_cartesian_points_as_lists()
            shapes_as_cartesian_points.append({"speed": speed,
                                               "power": power,
                                               "passes": passes,
                                               "point_lists": point_lists})

        return shapes_as_cartesian_points


    def get_all_shapes_as_process_points(self):

        ## NOTE THIS IS STILL IN CARTESIAN COORDINATES
        ## Update it to use process points later

        # Create empty list
        shapes_as_process_points = []

        # Go through the laser objects
        for laser_object in self.laser_objects:

            # Get the points for the object
            object_points = laser_object.get_process_points()

            # Add the points to the list
            shapes_as_process_points.append(object_points)

        # Return the list
        return shapes_as_process_points

    def get_gcode(self):

        # Get all the shapes as

        # No need, we are all cartesian now
        #self.get_all_shapes_as_points()

        # Account for the fact that the Y axis is inverted
        # self.invert_points()

        header = self.get_gcode_header()
        gcode = []

        gcode.extend(header)

        # Get all the shapes as cartesian points
        shapes_as_cartesian_points = self.get_all_shapes_as_cartesian_points()

        # Go through the laser objects
        for shape in shapes_as_cartesian_points:

            for point_list in shape["point_lists"]:

                speed = f"F{shape['speed']}"
                power = f"S{shape['power']}"
                passes = shape["passes"]

                shape_gcode = convert_points_to_gcode(point_list)
                start_gcode = shape_gcode.pop(0)

                gcode.append("; Shape start")

                # We should iterate the passes here
                for i in range(passes):
                    gcode.append(f"; Pass {i+1} of {passes}")
                    gcode.append("; Turn laser off, go to start position")
                    gcode.append("S0")
                    gcode.append(start_gcode)

                    # Turn the laser on
                    gcode.append("; Turn laser on")
                    gcode.append("; constant power mode, but turned off")
                    gcode.append(self.laser_mode)

                    # Set the speed and power
                    gcode.append("; Set speed and power")
                    gcode.append(speed)
                    gcode.append(power)

                    # Add the gcode to the list
                    gcode.extend(shape_gcode)

        # Add the footer
        gcode.append("; All done, turn laser off")
        gcode.append("M5")

        # Got back home
        gcode.append("; Go back home")
        gcode.append("G0 X0 Y0")

        # Return the gcode
        return gcode

    # Do simple, crude inversion of the Y axis
    def invert_points(self):

        # Now we have the maximum y and we can invert the points
        for shape in self.shapes_as_points:
            for points in shape["points"]:
                for point_list in points:
                    for point in point_list:
                        point[1] = max_y - point[1]

        return self.shapes_as_points

    # Take some preconfigured paths and text, turn it
    def get_max_y(self):

        # Add all the points in all the shapes to a list
        all_points = []

        for shape in self.shapes_as_points:
            for point_list in shape["points"]:
                for points in point_list:
                    all_points.extend(points)

        # We now have all the points
        # Find the maximum y
        max_y = 0

        for point in all_points:
            if point[1] > max_y:
                max_y = point[1]

        return max_y

    def load_test_project(self):

        # Clear out the laser objects
        self.laser_objects = []

        # Lets create a settings list, items of speed, power, passes
        settings = [(600, 700, 10),
                    (200, 800, 4),
                    (400, 700, 8),
                    (1200, 400, 20)]
        n = 0
        for setting in settings:
            laser_objects = self.small_material_test(setting[0], setting[1], setting[2])

            laser_objects[0].translate(0, n * 20)
            laser_objects[1].translate(0, n * 20)

            self.laser_objects.append(laser_objects[0])
            self.laser_objects.append(laser_objects[1])

            n+=1

        pass

    # Create a small square, and some text
    def material_test(self, speed, power):

        # Add a simple rectangle
        laser_object = LaserObject(speed, power)
        laser_object.add_rectangle(2, 2, 21, 21)

        # Add a some text
        text = (f"Speed  {speed}\n"
                f"Power  {power}\n"
                "Passes 1")

        # Writing has default speed/power 600-250
        laser_text_object = LaserTextObject(text, "../fonts/UbuntuMono-Regular.ttf", 14, 600, 250)
        laser_text_object.location = (25, 6)

        return laser_object, laser_text_object

    def small_material_test(self, speed, power, passes):

        # Add a simple rectangle
        laser_object = LaserObject(speed, power, passes)
        # laser_object.add_rectangle(0, 0, 7, 7)
        laser_object.add_rounded_rectangle(10, 10, 10, 10)

        laser_object.add_circle(10, 10, 9)

        # Add a some text
        text = (f"{speed}\n{int(power/10)}.{passes}")

        # Writing has default speed/power 600-250
        laser_text_object = LaserTextObject(text, "../fonts/UbuntuMono-Regular.ttf", 9, 600, 250, 1)
        laser_text_object.location = (6, 7.5)

        return laser_object, laser_text_object

# A LaserObject is an SVG object, that can be converted to GCode
# It is a path object, or needs conversion to a path object first
class LaserObject:

    def __init__(self, speed, power, passes, svg_element = None):
        self.svg_element = svg_element
        self.speed = speed
        self.power = power
        self.passes = passes
        self.path = None
        self.points = None

        self.shape_gcode = None

        # These are a list of points, that are in cartesian coordinates
        # All other data is derived from this
        # An object can have multiple points lists
        self.shapes = list()

        # This is the origin of the laser object, all other cartesian points are relative to this
        self.location = (0, 0)

        # This is the bounding box of the object, used to display the item when it is selected
        self.bounding_box = (0,0,0,0)

    def translate(self, x, y ):

        x = self.location[0] + x
        y = self.location[1] + y

        self.location = (x, y)

    def get_cartesian_points_as_lists(self):

        # This will return a copy of the list, so multiple point lists can be in the same shape
        # And it can be mutated without affecting the original
        point_lists = list()

        for shape in self.shapes:

            cartesian_points = list()

            for point in shape:
                x = point[0] + self.location[0]
                y = point[1] + self.location[1]

                cartesian_points.append((x, y))

            point_lists.append(cartesian_points)

        return point_lists

    # This is a helper function, that will return the points in a proces point format
    # Currently without regard for max_y
    def get_process_points(self):

        ## NOTE THIS IS STILL IN CARTESIAN COORDINATES
        ## Update it to use process points later?
        ## Or just use cartesian points, and to this somewhere else

        # Create empty list
        process_points = list()

        # Go through the shapes
        for shape in self.shapes:

            shape_points = []

            for point in shape:

                # Add the points to the list
                x = point[0] + self.location[0]
                y = point[1] + self.location[1]

                result = []
                result.append(x)
                result.append(y)

                shape_points.append(result)

            # Hack, hacky code, hacky code
            # This will flip it !
            for points in shape_points:
                # Flip it around the Y axis
                points[1] = 400 - points[1]

            process_points.append(shape_points)

        return process_points



    def convert_process_to_cartesian(self, process_points):
        raise NotImplementedError
        # # These points are now upside down, flip them
        # # Now we have the maximum y and we can invert the points
        # max_y = 0
        # for list_of_points in process_points:
        #     for point in list_of_points:
        #         if point[1] > max_y:
        #             max_y = point[1]
        #
        # # Now we have the maximum y and we can invert the points
        # for list_of_points in process_points:
        #     for point in list_of_points:
        #         point[1] = max_y - point[1]
        #
        # # They are now cartesian points, we need to convert them to process points
        # self.cartesian_points = process_points


    def get_path(self):
        # We have an SVG element, it is already unpacked
        # So the root should contain the data

        root = elementTree.fromstring(self.svg_element)
        try:

            path = root.attrib["d"]
            return path

        except elementTree.ParseError:
            # Raise an error maybe
            pass

    def get_svg_element(self):

        return self.svg_element

    def convert_to_points(self):

        # The whole shape is a list of points
        # Each point is tuple of 2 elements, x and y
        self.path = self.get_path()
        self.points = convert_path_to_points(self.path)

        return self.points

    def get_shape_as_points(self):

        # This will return a list

        # Get the points
        self.convert_to_points()

        points_list = list()
        points_list.extend(self.points)

        return points_list

    def convert_to_gcode(self):

        self.shape_gcode = convert_points_to_gcode(self.points)

        return self.shape_gcode

    # These are functino that add shapes to the laser object
    # Considering making separate classes for each shape, but for now they are all just paths

    # The rectangle is defined by the bottom left corner, and the width and height
    def add_rectangle(self, x, y, width, height):

        # Create a list of points
        points = list()

        # Bottom left corner
        points.append((x, y))

        # Top left corner
        points.append((x, y + height))

        # Top right corner
        points.append((x + width, y + height))

        # Bottom right corner
        points.append((x + width, y))

        # And close the shape
        points.append((x, y))

        # Add this rectangle to the list of shapes
        self.shapes.append(points)

        return

    def add_rounded_rectangle(self, x_center, y_center, width, height, radius=3):

        import numpy as np
        """
        Generate points on the boundary of a rounded rectangle.

        Parameters:
        x_center (float): The x-coordinate of the center of the rectangle.
        y_center (float): The y-coordinate of the center of the rectangle.
        width (float): The width of the rectangle.
        height (float): The height of the rectangle.
        radius (float): The radius of the corners.
        points_per_corner (int): Number of points to generate on each corner.

        Returns:
        list of tuples: List of (x, y) coordinates of the points on the boundary.
        """
        points_per_corner = 16

        # Calculate corner centers
        half_width, half_height = width / 2, height / 2
        corner_centers = [
            (x_center - half_width + radius, y_center - half_height + radius),  # top-left
            (x_center + half_width - radius, y_center - half_height + radius),  # top-right
            (x_center + half_width - radius, y_center + half_height - radius),  # bottom-right
            (x_center - half_width + radius, y_center + half_height - radius),  # bottom-left
        ]

        # Generate points for each corner
        points = []
        for (cx, cy), start_angle in zip(corner_centers, [np.pi, 1.5 * np.pi, 0, 0.5 * np.pi]):
            angles = np.linspace(start_angle, start_angle + np.pi / 2, points_per_corner, endpoint=False)
            x_points = cx + radius * np.cos(angles)
            y_points = cy + radius * np.sin(angles)
            points.extend(list(zip(x_points, y_points)))

        # Take the last point, and add it to the beginning
        points.append(points[0])

        # Add this rectangle to the list of shapes
        self.shapes.append(points)

        return

    def add_polygon(self, points):

        # Add this polygon to the list of shapes
        self.shapes.append(points)

        return

    def add_circle(self, x_center, y_center, radius):

        import numpy as np

        """
        Generate points on the circumference of a circle.

        Parameters:
        x_center (float): The x-coordinate of the center of the circle.
        y_center (float): The y-coordinate of the center of the circle.
        radius (float): The radius of the circle.
        num_points (int): Number of points to generate on the circumference.

        Returns:
        list of tuples: List of (x, y) coordinates of the points on the circumference.
        """
        num_points = 128
        angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
        x_points = x_center + radius * np.cos(angles)
        y_points = y_center + radius * np.sin(angles)

        points = list(zip(x_points, y_points))

        # Take the last point, and add it to the beginning
        points.append(points[0])

        # Add this circle to the list of shapes
        self.shapes.append(points)

        return

    # Fill the shapes with ilnes
    def fill(self):

        # Initialize the list to store start and end coordinates of lines
        lines = []

        # Get all the points
        for shape in self.shapes:
            polygon = shape.copy()
            polygon.pop()

        ###
            # Extracting the ymin and ymax values from the polygon vertices
            y_values = [point[1] for point in polygon]
            ymin, ymax = min(y_values), max(y_values)

            # Iterate through each y value from ymin to ymax
            for y in range(ymin, ymax + 1):
                intersections = []

                # Find intersections with the polygon edges
                for i in range(len(polygon)):
                    start, end = polygon[i], polygon[(i + 1) % len(polygon)]

                    # Skip horizontal edges
                    if start[1] == end[1]:
                        continue

                    # Ensure that the scanline intersects the edge vertically
                    if (y >= start[1] and y < end[1]) or (y >= end[1] and y < start[1]):
                        # Calculate the x value of the intersection using linear interpolation
                        x = start[0] + (y - start[1]) * (end[0] - start[0]) / (end[1] - start[1])
                        intersections.append(x)

                # Sort the intersections to ensure correct filling
                intersections.sort()

                # Fill between each pair of intersections
                for i in range(0, len(intersections), 2):
                    if i + 1 < len(intersections):  # Ensure there's a pair
                        print(f"Drawing line from ({intersections[i]}, {y}) to ({intersections[i + 1]}, {y})")
                        start = (intersections[i], y)
                        stop = (intersections[i + 1], y)
                        lines.append([start, stop])

        # Add the lines to the shapes
        self.shapes.extend(lines)

        return


# A derived class for Text objects, based on LaserObject
class LaserTextObject(LaserObject):

    # This class has a font size, text and font
    def __init__(self, text, font, font_size, speed, power, passes):
        self.text = str(text)
        self.font = font
        self.font_size = font_size

        # Call the parent constructor
        super().__init__(speed, power, passes)


    # Override the get_shape_as_points method
    # This will represent the text as a list of points, but accounting for the fact
    # that a text object has multiple letters
    def get_shape_as_points(self):

        # probably not need
        raise NotImplementedError

        # Convert the text to a list of SVG paths
        letter_paths = text_to_svg_path(self.text, self.font, self.font_size)

        for letter_path in letter_paths:
            print(letter_path)

            # Convert that path to points
            letter_points = convert_path_to_points(letter_path)

            return letter_points


    # This is the laser TextObject of the function
    def get_cartesian_points_as_lists(self):

        # Convert the text to a list of SVG paths
        letter_paths = text_to_svg_path(self.text, self.font, self.font_size)

        # Make empty process points list
        process_points = list()

        letter_objects = list()
        letter_process_points_list = list()

        # Get all the lettesr
        for letter_path in letter_paths:

            # Create a LaserObject
            letter_object = LaserObject(self.speed, self.power, self.passes, letter_path)
            letter_object.location = self.location

            # Convert the paths to points
            letter_process_points = letter_object.get_shape_as_points()

            letter_process_points_list.append(letter_process_points)
            letter_objects.append(letter_object)

        # Get the max_y over all the letters
        max_y = 0
        for shape in letter_process_points_list:
            for list_of_points in shape:
                for point in list_of_points:
                    if point[1] > max_y:
                        max_y = point[1]

        # A this point, we have cartesian points for each letter, as LaserObjects

        # Convert all the letters to cartesian points
        for letter_object in letter_objects:

            # Get the process points for the letter
            letter_process_points = letter_object.get_shape_as_points()

            # These are process points, we need to convert them to cartesian points
            letter_process_points = convert_process_to_cartesian(letter_process_points, max_y = max_y)

            # Add those points to the shapes list
            letter_object.shapes.extend(letter_process_points)

            # And for all those points, fix location
            for shape in letter_process_points:
                point_list = list()

                for point in shape:
                    x = point[0] + self.location[0]
                    y = point[1] + self.location[1]

                    point_list.append((x, y))

                process_points.append(point_list)

        return process_points

    # This overloaded function takes into account that the text is converted to SVG glyphs first
    # Then those pats, are converted to process points
    # And finally those process points are converted to cartesian points
    def get_process_points(self):

        # Convert the text to a list of SVG paths
        letter_paths = text_to_svg_path(self.text, self.font, self.font_size)

        # Make empty process points list
        process_points = list()

        letter_objects = list()
        letter_process_points_list = list()

        # Get all the lettesr
        for letter_path in letter_paths:

            # Create a LaserObject
            letter_object = LaserObject(self.speed, self.power, self.passes, letter_path)
            letter_object.location = self.location

            # Convert the paths to points
            letter_process_points = letter_object.get_shape_as_points()

            letter_process_points_list.append(letter_process_points)
            letter_objects.append(letter_object)

        # Get the max_y over all the letters
        max_y = 0
        for shape in letter_process_points_list:
            for list_of_points in shape:
                for point in list_of_points:
                    if point[1] > max_y:
                        max_y = point[1]

        # Convert all the letters to cartesian points
        for letter_object in letter_objects:

            # Get the process points for the letter
            letter_process_points = letter_object.get_shape_as_points()

            # Really confused here!
            # These are process points, we need to convert them to cartesian points
            letter_process_points = convert_process_to_cartesian(letter_process_points, max_y = max_y)

            # Add those points to the shapes list
            letter_object.shapes.extend(letter_process_points)

            # And then get the process points for those
            shape_points = letter_object.get_process_points()

            # And extend the process points list
            process_points.extend(shape_points)

        return process_points

    def get_svg_element(self):

        letter_paths = text_to_svg_path(self.text, self.font, self.font_size)
        return letter_paths


def convert_path_to_points(path):
    # Regex pattern to match path commands and their parameters
    pattern = r'([MLCQAZHVmlcqazhv][^MLCQAZHVmlcqazhv]*)'
    components = re.findall(pattern, path)

    # create point list
    points = []

    # Return list
    return_list = []

    # We need the start coordinates, so we can go back to them
    # We will get them from the first component
    # We will remove the first component from the list as well
    first_command = components[0]
    start_coordinates = re.split(r'[ ,]+', first_command[1:])

    start_coordinates = start_coordinates[:2]
    current_coordinates = start_coordinates

    # go through each component
    for item in components:

        # we will check what type of component it is
        if item[0] == "M":
            # this is a move command, and the first command
            # get the coordinates
            coordinates = re.split(r'[ ,]+', item[1:])

            # Track the current coordinates
            current_coordinates = coordinates[:2]

            # Also, the start coordinates
            start_coordinates = coordinates[:2]

            # Add the coordinates to the list
            points.append(list(current_coordinates))

        if item[0] == "H":
            # this is a horizontal line command
            # get the x coordinate
            x = item[1:]

            # Track the current coordinates, only update X
            current_coordinates[0] = x

            points.append(list(current_coordinates))

        if item[0] == "V":
            # this is a vertical line command
            # get the y coordinate
            y = item[1:]

            # Track the current coordinates, only update Y
            current_coordinates[1] = y
            points.append(list(current_coordinates))

        if item[0] == "L":
            # this is a line command
            # get the coordinates
            coordinates = re.split(r'[ ,]+', item[1:])

            # Track the current coordinates
            current_coordinates = coordinates[:2]

            points.append(list(current_coordinates))

        if item[0] == "C":
            # This is a circle command
            # get the coordinates
            coordinates = re.split(r'[ ,]+', item[1:])

            # Track the current coordinates
            current_coordinates = coordinates[4:6]


        if item[0] == "Q":

            # This is a quadratic bezier curve c
            coordinates = re.split(r'[ ,]+', item[1:])
            control_coordinates = coordinates[0:2]
            end_coordinates = coordinates[2:4]

            # convert all the coordinates to floats
            current_coordinates = [float(i) for i in current_coordinates]
            control_coordinates = [float(i) for i in control_coordinates]
            end_coordinates = [float(i) for i in end_coordinates]

            bezier_points = quadratic_bezier(current_coordinates, control_coordinates, end_coordinates)

            for bezier_point in bezier_points:
                points.append(list(bezier_point))

            current_coordinates = end_coordinates

        if item[0] == "Z":

            # We are at end for this path, maybe we should do something return for debug
            points.append(list(start_coordinates))

            # convert all the points to floats
            points = [[float(i) for i in point] for point in points]

            # add the points to the return list
            return_list.append(points)

            # clear the points list
            points = []

    return return_list

# function to convert SVG path to GCode
def convert_points_to_gcode(points):

    # create gcode list
    gcode = []

    # Get the first item from the list, that is the start of the shape
    # Remove that item from the list as well
    start_coordinates = points.pop(0)
    gcode.append(f"G0 X{start_coordinates[0]} Y{start_coordinates[1]}")

    # We need to make sure that all the items in points, are strings
    points = [[str(i) for i in point] for point in points]

    # go through each component
    # At this point, we only have to deal with lines
    for item in points:

        # get the coordinates
        gcode.append("G1 " + "X" + item[0] + " Y" + item[1])

    return gcode

# Helper function to covert a set of process points to cartesian points
def convert_process_to_cartesian(points, max_y = 0):

    # These points are now upside down, flip them
    # Now we have the maximum y and we can invert the points
    # Check if we have the max_y, or we need to find it
    if max_y == 0:
        for list_of_points in points:
            for point in list_of_points:
                if point[1] > max_y:
                    max_y = point[1]

    # Now we have the maximum y and we can invert the points
    for list_of_points in points:
        for point in list_of_points:
            point[1] = max_y - point[1]

    # They are now cartesian points, we need to convert them to process points
    return points