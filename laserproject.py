# We will have a class that can be used to covert SVG paths to GCode
# Per path object, we can set the speed and power of the laser
# This means that the class is en essence a list of SVG objects with a speed and power

# That would mean that there should be a class for SVG objects

import xml.etree.ElementTree as elementTree

# LaserProject is a collection of LaserObjects
class LaserProject:
    def __init__(self):
        self.laser_objects = []

    def get_gcode(self):

        # Create empty gcode list
        gcode = []

        # Add the header
        gcode.append("; gCode created by LumenCat")
        gcode.append("; setting up machine basics")

        gcode.append("; XY plane")
        gcode.append("; cutter compensation off")
        gcode.append("; coordinate system 1")
        gcode.append("; move 'unit'/min")

        gcode.append("G17 G40 G54 G94")

        gcode.append("; constant power mode, but turned off")
        gcode.append("M4 S0")

        # Go through the laser objects
        for laser_object in self.laser_objects:

            # Get the gcode for the laser object
            object_gcode = laser_object.get_gcode()

            # Add the gcode to the list
            gcode.extend(object_gcode)

        # Add the footer
        gcode.append("; All done, turn laser off")
        gcode.append("M5 S0")

        # Got back home
        gcode.append("; Go back home")
        gcode.append("G0 X0 Y0")

        # Return the gcode
        return gcode

# A LaserObject is an SVG object, that can be converted to GCode
class LaserObject:

    def __init__(self, svg_element, speed, power):
        self.svg_element = svg_element
        self.speed = speed
        self.power = power
        self.path = None

    def extract_path(self):
        # We have an SVG element, it is already unpacked
        # So the root should contain the data

        root = elementTree.fromstring(self.svg_element)

        try:

            path = root.attrib["d"]

            # The gcode for the shape is
            shape_gcode = convert_path_to_gcode(path)

            # And return it
            return shape_gcode

        except elementTree.ParseError:
            # Raise an error maybe
            pass

    def get_gcode(self):

        # Create empty gcode list
        gcode = []

        # Get the settings
        speed = f"F{self.speed}"
        power = f"S{self.power}"

        # Get the gcode
        shape_gcode = self.extract_path()

        # Get the first item from the list, that is the start of the shape
        # Remove that item from the list as well
        start_gcode = shape_gcode.pop(0)

        gcode.append("; Shape start")
        gcode.append("; Turn laser off, go to start position")
        gcode.append("M5")
        gcode.append(start_gcode)

        # Set the speed and power
        gcode.append("; Set speed and power")
        gcode.append(speed)
        gcode.append(power)

        # Go through the shape gcode
        while shape_gcode:
            # Get the next gcode
            next_gcode = shape_gcode.pop(0)

            # Add it to the list
            gcode.append(next_gcode)

        # Return the list

        return gcode

        
# function to convert SVG path to GCode
def convert_path_to_gcode(path):

    # split the path into its components
    components = path.split(" ")

    # create gcode list
    gcode = []

    # go through each component
    for item in components:

        # we will check what type of component it is
        if item[0] == "M":
            # this is a move command, G0
            # get the coordinates
            coordinates = item[1:].split(",")

            gcode.append("G0 " + "X" + coordinates[0] + " Y" + coordinates[1])

        if item[0] == "H":
            # this is a horizontal line command, G1
            # get the x coordinate
            x = item[1:]

            gcode.append("G1 " + "X" + x)

        if item[0] == "V":
            # this is a vertical line command, G1
            # get the y coordinate
            y = item[1:]

            gcode.append("G1 " + "Y" + y)

        if item[0] == "L":
            # this is a line command, G1
            # get the coordinates
            coordinates = item[1:].split(",")

            gcode.append("G1 " + "X" + coordinates[0] + " Y" + coordinates[1])

    return gcode