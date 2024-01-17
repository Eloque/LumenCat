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
        self.laser_objects = []
        self.shapes_as_points = None
        self.gcode = None
        self.gcode_header = None

        self.laser_mode = "M4" # M4 is constant power mode, M3 is PWM mode

    # Helper function, get a string representation of the SVG

    def load_from_svg_file(self, filename):

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

        gcode.append("; XY plane")
        gcode.append("; cutter compensation off")
        gcode.append("; coordinate system 1")
        gcode.append("; move 'unit'/min")

        gcode.append("G17 G40 G54 G94")

        gcode.append("; constant power mode, but turned off")
        gcode.append(f"{self.laser_mode} S0")

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


    def get_gcode(self):

        # Get all the shapes as
        self.get_all_shapes_as_points()
        # Account for the fact that the Y axis is inverted
        self.invert_points()

        header = self.get_gcode_header()
        gcode = []

        gcode.extend(header)

        # Go through the laser objects
        for shape in self.shapes_as_points:

            for point_list in shape["points"]:
                for points in point_list:

                    speed = f"F{shape["speed"]}"
                    power = f"S{shape["power"]}"

                    shape_gcode = convert_points_to_gcode(points)
                    start_gcode = shape_gcode.pop(0)

                    gcode.append("; Shape start")
                    gcode.append("; Turn laser off, go to start position")
                    gcode.append("M5")
                    gcode.append(start_gcode)

                    # Turn the laser on
                    gcode.append("; Turn laser on")
                    gcode.append(self.laser_mode)

                    # Set the speed and power
                    gcode.append("; Set speed and power")
                    gcode.append(speed)
                    gcode.append(power)

                    # Add the gcode to the list
                    gcode.extend(shape_gcode)

        # Add the footer
        gcode.append("; All done, turn laser off")
        gcode.append("M5 S0")

        # Got back home
        gcode.append("; Go back home")
        gcode.append("G0 X0 Y0")

        # Return the gcode
        return gcode

    # Do simple, crude inversion of the Y axis
    def invert_points(self):

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

        # Now we have the maximum y and we can invert the points
        for shape in self.shapes_as_points:
            for points in shape["points"]:
                for point_list in points:
                    for point in point_list:
                        point[1] = max_y - point[1]

        return self.shapes_as_points


# A LaserObject is an SVG object, that can be converted to GCode
# It is a path object, or needs conversion to a path object first
class LaserObject:

    def __init__(self, speed, power, svg_element = None):
        self.svg_element = svg_element
        self.speed = speed
        self.power = power
        self.path = None
        self.points = None

        self.shape_gcode = None

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
        # It will contain the speed, the power and the points as a list

        # Get the points
        self.convert_to_points()

        points_list = list()
        points_list.append(self.points)

        return { "speed": self.speed, "power": self.power, "points": points_list}

    def convert_to_gcode(self):

        self.shape_gcode = convert_points_to_gcode(self.points)

        return self.shape_gcode


# A derived class for Text objects, based on LaserObject
class LaserTextObject(LaserObject):

    # This class has a font size, text and font
    def __init__(self, text, font, font_size, speed, power):
        self.text = text
        self.font = font
        self.font_size = font_size

        # Call the parent constructor
        super().__init__(speed, power)


    # Override the get_shape_as_points method
    # This will represent the text as a list of points, but accounting for the fact
    # that a text object has multiple letters
    def get_shape_as_points(self):

        points_list = list()

        # Convert the text to a list of SVG paths
        letter_paths = text_to_svg_path(self.text, self.font, self.font_size)

        for letter_path in letter_paths:
            # Create a LaserObject
            letter_object = LaserObject(self.speed, self.power, letter_path)

            # Get the shape as points
            letter_shape_as_points = letter_object.get_shape_as_points()

            # Add it to the list, unpack that list i guess
            points_list.append(letter_shape_as_points["points"][0])

        return {"speed": self.speed, "power": self.power, "points": points_list}

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

            coordinates = re.split(r'[ ,]+', item[1:])
            control_coordinates = coordinates[0:2]
            end_coordinates = coordinates[2:4]

            # convert all the coordinates to floats
            current_coordinates = [float(i) for i in current_coordinates]
            control_coordinates = [float(i) for i in control_coordinates]
            end_coordinates = [float(i) for i in end_coordinates]

            bezier_points = quadratic_bezier(current_coordinates, control_coordinates, end_coordinates, 3)

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

