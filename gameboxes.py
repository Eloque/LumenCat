from laserproject import LaserObject, LaserProject, LaserTextObject
from shapely.geometry import Polygon

from predefined import finger_jointed_side, move, finger_jointed_lid, rotate, rotate_90

material_thickness = 4.1
slot_width = material_thickness
slot_height = 6

def cardbox():

    speed = 800
    power = 850
    passes = 20
    # Create a box, meant for storing cards
    # This box has one row of card
    # material_thickness = 4.1

    rows = 1
    columns = 2
    depth = 40 + 2 * material_thickness

    # Card size determines the size of the box
    card_width = 63
    card_height = 92

    # Card size determines the size of the box
    card_width = 48
    card_height = 70

    # the base place of the box should be material_thickness + card_width and depth + 2 * material_thickness
    base_width = columns * (card_width + material_thickness) + material_thickness

    baseplate = LaserObject(speed, power, passes)
    baseplate.add_polygon(finger_jointed_box(base_width, depth, 3, 2))

    # Cards for ease of reference.
    cards = LaserObject(speed, power, passes)
    # for each card, create a rectangle
    for i in range(columns):
        x = i * (card_width + material_thickness) + material_thickness
        card = [(x, 0), (x, card_height), (x+card_width, card_height), (x + card_width, 0), (x, 0)]
        cards.add_polygon(card)

    cards.location = (material_thickness, 20)

    # total card width is card_width * columns
    total_card_width = card_width * columns
    total_divider = material_thickness * (columns - 1)
    sides = material_thickness * 2

    calculated_width = total_card_width + total_divider + sides

    # Slots in the bottom box
    slots_across = columns - 1
    slots_space = slots_across * material_thickness
    space_left = base_width - slots_space - 2 * material_thickness
    space_between_tabs = space_left / (slots_across + 1)
    slot_height = 6

    for i in range(1, slots_across + 1):
        tab_start_x = space_between_tabs * i + material_thickness * (i)
        baseplate.add_rectangle(tab_start_x, depth/2 - slot_height/2 , 4, slot_height)

    # Side of the box
    # sides = finger_jointed_back(base_width, card_height, 3, 2)

    h =  card_height/2 - 2 - 5
    print("h", h)

    sides = finger_jointed_front(base_width, h, 3, 2)
    side = LaserObject(speed, power, passes)
    side.add_polygon(move(sides, 0 , material_thickness))

    # side.add_polygon([[0,0], [base_width, h]])
    # side.add_polygon([[0, h], [base_width, 0]])

    xb = base_width/2

    # side.add_polygon([[xb, 0], [xb, 30]])
    # side.add_polygon([[0, 0], [xb, 30]])
    # side.add_polygon([[0, 30], [xb, 0]])

    xb = xb/2

    # side.add_polygon([[xb, 20], [xb, -80]])

    center = card_width / 2 + material_thickness
    center = 50

    title = LaserTextObject("Items", "../fonts/Ugalt.ttf", 20, 600, 250, 1)
    title = title.convert_to_laser_object()

    title.location = (xb, 0)
    title.center()
    title.translate(0, 20)
    title.priority = 20

    xb += base_width/2

    # side.add_polygon([[base_width/2, 0], [base_width , 30]])
    # side.add_polygon([[base_width/2, 30], [base_width , 0]])

    # side.add_polygon([[xb, 20], [xb, -80]])

    title2 = LaserTextObject("Artifacts", "../fonts/Ugalt.ttf", 20, 600, 250, 1)
    title2 = title2.convert_to_laser_object()

    title2.location = (xb, 0)
    title2.center()
    title2.translate(0, 20)
    title2.priority = 20

        # Insert
    insert = card_insert_side(depth, card_height)
    #side.add_polygon(move(insert, material_thickness, material_thickness ))
    #side.add_polygon(move(insert, material_thickness, material_thickness))

    insert = card_insert(depth, card_height)
    #side.add_polygon((move(insert, material_thickness, material_thickness)))

    laser_project = LaserProject()
    # laser_project.laser_objects.append(baseplate)
    laser_project.laser_objects.append(side)
    laser_project.laser_objects.append(title)
    laser_project.laser_objects.append(title2)
    #laser_project.laser_objects.append(cards)

    return laser_project


def finger_jointed_bottom(width, height, slots_across, slots_tall):

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

def card_insert_side(width, height, slots_vertical = 2, slots_horizontal = 2):

    # The side are on the inside, so subtract 2 x material_thickness
    width -= 2 * material_thickness

    # But, it also has an overhanging tab, so add 1 x material_thickness
    width += material_thickness

    points = []

    # We start 0,0 and then go to 0,height
    # How many slots do we need to make, that is the space for the slots
    left = finger_joints_vertical(height, slots_vertical)
    points += left

    # Sloped Curve on the right
    sloped = sloped_curve(width, height)
    points += sloped

    # Tabs inside slope
    points += [
                [width, height/2 - slot_height - 5],
                [width - slot_width, height/2 - slot_height - 5],
    ]

    print("Side" , height / 2 - slot_height - 5)

    points += [[width - slot_width, 0]]

    # And the bottom
    bottom = finger_joints_horizontal(width + material_thickness, slots_horizontal)

    # Move all bottom point left by material_thickness
    bottom = move(bottom, -material_thickness, 0)

    # Remove the first point in bottom
    bottom = bottom[1:]

    # Replace the last point in bottom
    bottom[-1] = [0, 0]

    points += bottom

    return points


def card_insert(width, height):

    # The side are on the inside, so subtract 2 x material_thickness
    width -= 2 * material_thickness

    # But, it also has an overhanging tab, so add 1 x material_thickness
    width += material_thickness

    # Bottom first, it has one tab in the middle
    space_left = width - slot_height + material_thickness

    # Determine the space between the tabs
    space_between_tabs = space_left / 2

    # Determine the starting x position of the first tab
    tab_start_x = space_between_tabs

    # Now make the bottom
    points = [[width - slot_width, 0]]

    # Add the first slot
    points += [
        [width - tab_start_x, 0],
        [width - tab_start_x, - slot_width],
        [tab_start_x - material_thickness, - slot_width],
        [tab_start_x - material_thickness, 0]
    ]

    points += [[0, 0], [0, height - slot_height]]

    # Now a small tab in the top
    points += [
        [-slot_width, height - slot_height],
        [-slot_width, height],
        [0, height]
    ]

    # get some rounded corners now
    radius = 6
    num_points = 16

    points += [[0, height]]

    # we have 3 points, a start, a corner and an end
    start = [0, height]
    corner =  [ width/2, height]
    end = [ width, height/2]

    # find the point that is radius away from the corner towards start
    # find the point that is radius away from the corner towards end

    # Calculate the points along the curve
    # curve = quadratic_bezier(start, corner, end, num_points)

    # Find the corner points
    left_corner_point = point_on_line(corner, start, radius)
    right_corner_point = point_on_line(corner, end, radius)

    first_curve = quadratic_bezier(left_corner_point, corner, right_corner_point, num_points)

    # The second curve is between the next points
    start = [ width/2, height]
    corner = [ width, height/2]
    end = [width,0]

    # Find the corner points
    left_corner_point = point_on_line(corner, start, radius)
    right_corner_point = point_on_line(corner, end, radius)

    second_curve = quadratic_bezier(left_corner_point, corner, right_corner_point, num_points)

    points += first_curve
    points += second_curve

    # Add the arc to the points
    # Now add a final tab
    points += [
                [width, height/2 - slot_height - 5],
                [width - slot_width, height/2 - slot_height - 5],
                #[width - slot_width, height/2 - slot_height - slot_height],
                #[width, height / 2 - slot_height - slot_height],
    ]

    points += [[width - slot_width, 0]]


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


###
def finger_jointed_front(width, height, slots_across, slots_tall):

    slot_height = 4
    material_thickness = 4.1

    # We start 0,0 and then go to 0,height
    # How many slots do we need to make, that is the space for the slots
    slots_space = slots_tall * slot_height
    space_left = height - slots_space

    # We need to divide the space left by the number of slots + 1 (top and bottom)
    space_between_tabs = space_left / (slots_tall + 1)

    # Dynamic points calculation starting from bottom left, moving up and then down the right side
    # left = finger_joints_vertical(height, width, slots_vertical = 2, slots=True, side = "left")
    points = [[0, 0]]

    slots_space = slots_across * slot_height
    space_left = width - slots_space
    space_between_tabs = space_left / (slots_across + 1)

    points += [
        [0, height - slot_height],
        [material_thickness, height - slot_height],
        [material_thickness, height]
    ]

    # Instead of this, we need one vertical slot, in the center
    # Insert slots in the middle
    columns = 2
    number_of_slots = columns - 1
    material_thickness = 4.1

    # Determine how much space is left after the slots
    space_left = width - number_of_slots * material_thickness

    # Determine the space between the slots
    space_between_slots = space_left / (number_of_slots + 1)

    # Determine the width of the slot
    slot_width = material_thickness

    # Determine the starting x position of the first slot
    tab_start_x = space_between_slots

    # Determine the starting y position of the slot
    tab_start_y = height

    # Add the first slot
    points += [
        [tab_start_x, tab_start_y],
        [tab_start_x, tab_start_y - slot_height],
        [tab_start_x + slot_width, tab_start_y - slot_height],
        [tab_start_x + slot_width, tab_start_y],
    ]

    points += [
        [width - material_thickness, height],
        [width - material_thickness, height - slot_height],
        [width, height - slot_height],
        [width, 0]
    ]

    bottom = finger_joints_horizontal( width, slots_horizontal = 3, slots=False)
    points += bottom


    return points

def finger_jointed_back(width, height, slots_across, slots_tall):

    slot_width = 4.1
    slot_height = 6

    #print(height)

    # We start 0,0 and then go to 0,height
    # How many slots do we need to make, that is the space for the slots
    slots_space = slots_tall * slot_height
    space_left = height - slots_space

    # We need to divide the space left by the number of slots + 1 (top and bottom)
    space_between_tabs = space_left / (slots_tall + 1)


    # Dynamic points calculation starting from bottom left, moving up and then down the right side
    left = finger_joints_vertical(height, width, slots_vertical = 2, slots=True, side = "left")
    points = left

    slots_space = slots_across * slot_height
    space_left = width - slots_space
    space_between_tabs = space_left / (slots_across + 1)

    points += [[0, height]]

    # Instead of this, we need one vertical slot, in the center
    # Insert slots in the middle
    columns = 2
    number_of_slots = columns - 1
    material_thickness = 4.1

    # Determine how much space is left after the slots
    space_left = width - number_of_slots * material_thickness

    # Determine the space between the slots
    space_between_slots = space_left / (number_of_slots + 1)

    # Determine the height of the slot
    slot_height = 6

    # Determine the width of the slot
    slot_width = material_thickness

    # Determine the starting x position of the first slot
    tab_start_x = space_between_slots

    # Determine the starting y position of the slot
    tab_start_y = height

    # Add the first slot
    points += [
        [tab_start_x, tab_start_y],
        [tab_start_x, tab_start_y - slot_height],
        [tab_start_x + slot_width, tab_start_y - slot_height],
        [tab_start_x + slot_width, tab_start_y],
    ]



    # # Top Side Slots
    # for i in range(1, slots_across + 1):
    #     tab_start_x = space_between_tabs * i + slot_height * (i - 1)
    #     points += [
    #         [tab_start_x, height],
    #         [tab_start_x, height + slot_width],
    #         [tab_start_x + slot_height, height + slot_width],
    #         [tab_start_x + slot_height, height],
    #     ]

    # Right side
    right = finger_joints_vertical(height, width, slots_vertical = 2, slots=True, side = "right")
    points += right


    # Bottom Side Slots
    for i in range(1, slots_across + 1):
        # Calculate starting x position from the right, moving leftward
        tab_start_x =  width - (space_between_tabs * i + slot_height * (i - 1)  )
        points += [
            [tab_start_x, 0],
            [tab_start_x, -slot_width],  # Slot extends upwards
            [tab_start_x - slot_height, -slot_width],  # Right side of the slot
            [tab_start_x - slot_height, 0],  # Back to starting height
        ]

    points += [[0, 0]]

    # okay, we have, the left and top, now we need to do the right and bottom
    # we can just mirror that
    # take all the points, and mirror them so the box is complete
   # mirrored_points = [[width - x, height - y] for x, y in points]

   # points += mirrored_points

    # Now we create the right side

    return points


import numpy as np


def quadratic_bezier(p0, p1, p2, N=16):
    """
    Computes N points along a quadratic Bézier curve defined by three points.

    Parameters:
    - p0: Tuple (x, y), the starting point of the curve.
    - p1: Tuple (x, y), the control point of the curve.
    - p2: Tuple (x, y), the ending point of the curve.
    - N : Integer, the number of points on the curve to calculate.

    Returns:
    - List of tuples representing points (x, y) along the curve.
    """
    t_values = [i / (N - 1) for i in range(N)]
    curve_points = []
    for t in t_values:
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        curve_points.append((x, y))
    return curve_points



def point_on_line(a, b, n):
    """
    Calculates a point C that is N distance away from point A along the line AB.

    Parameters:
    - a: Tuple (x, y), the coordinates of point A.
    - b: Tuple (x, y), the coordinates of point B.
    - n: Float, the distance from point A to point C.

    Returns:
    - Tuple (x, y) representing the coordinates of point C.
    """
    # Calculate the vector from A to B
    vector_ab = (b[0] - a[0], b[1] - a[1])
    # Calculate the distance from A to B
    length_ab = (vector_ab[0]**2 + vector_ab[1]**2)**0.5
    # Normalize the vector
    unit_vector_ab = (vector_ab[0] / length_ab, vector_ab[1] / length_ab)
    # Calculate point C as A + n * unit_vector
    c = (a[0] + n * unit_vector_ab[0], a[1] + n * unit_vector_ab[1])
    return c


def finger_joints_vertical(height, width=0, slots_vertical = 2, slots=False, side = "left"):

    slots_space = slots_vertical * slot_height
    space_left = height - slots_space

    # We need to divide the space left by the number of slots + 1 (top and bottom)
    space_between_tabs = space_left / (slots_vertical + 1)

    # Create points
    points = []

    if slots:
        modifier = -1
    else:
        modifier = 1

    if side == "left":

        points = [[0, 0]]

        # Generating tab points dynamically on the left side
        for i in range(1, slots_vertical + 1):
            tab_start_y = space_between_tabs * i + slot_height * (i - 1)
            points += [
                [0, tab_start_y],
                [-slot_width * modifier , tab_start_y],  # Left side of the tab
                [-slot_width * modifier, tab_start_y + slot_height],  # Bottom side of the tab
                [0, tab_start_y + slot_height],  # Right side of the tab
            ]

        points += [[0, height]]

    if side == "right":

        points = [[width, height]]

        for i in range(1, slots_vertical + 1):
            # Calculate starting y position from the top, moving downward
            tab_start_y = height - (space_between_tabs * i + slot_height * (i - 1))
            points += [
                [width, tab_start_y],
                [width - (slot_width * - modifier), tab_start_y],  # Left side of the tab
                [width - (slot_width * - modifier), tab_start_y - slot_height],  # Bottom side of the tab
                [width, tab_start_y - slot_height],  # Right side of the tab
            ]

        points += [[width, 0]]

    return points

def finger_joints_horizontal(width, slots_horizontal = 2, slots=False, direction= "bottom"):

    # We start 0,0 and then go to 0,height
    # How many slots do we need to make, that is the space for the slots
    slots_space = slots_horizontal * slot_height
    space_left = width - slots_space

    # We need to divide the space left by the number of slots + 1 (top and bottom)
    space_between_tabs = space_left / (slots_horizontal + 1)

    points = [[width, 0]]

    if direction == "bottom":
        multiplier = 1
    else:
        multiplier = -1

    # Bottom Side Slots
    for i in range(1, slots_horizontal + 1):
        # Calculate starting x position from the right, moving leftward
        tab_start_x =  width - (space_between_tabs * i + slot_height * (i - 1)  )
        points += [
            [tab_start_x, 0],
            [tab_start_x, -slot_width * multiplier],  # Slot extends upwards
            [tab_start_x - slot_height, -slot_width  * multiplier],  # Right side of the slot
            [tab_start_x - slot_height, 0],  # Back to starting height
        ]

    points += [[0, 0]]

    return points

def sloped_curve(width, height):

    # Below this, is the sloped side
    # get some rounded corners now
    radius = 6
    num_points = 16

    # we have 3 points, a start, a corner and an end
    start = [0, height]
    corner =  [ width/2, height]
    end = [ width, height/2]

    # find the point that is radius away from the corner towards start
    # find the point that is radius away from the corner towards end
    left_corner_point = point_on_line(corner, start, radius)
    right_corner_point = point_on_line(corner, end, radius)

    first_curve = quadratic_bezier(left_corner_point, corner, right_corner_point, num_points)

    # The second curve is between the next points
    start = [ width/2, height]
    corner = [ width, height/2]
    end = [width,0]

    # Find the corner points
    left_corner_point = point_on_line(corner, start, radius)
    right_corner_point = point_on_line(corner, end, radius)

    second_curve = quadratic_bezier(left_corner_point, corner, right_corner_point, num_points)

    points = []

    points += first_curve
    points += second_curve

    return points