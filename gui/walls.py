SLOT_HEIGHT = 6

from shapely.geometry import Polygon
from shapely.ops import unary_union

def create_tabbed_wall(x_size, height, total_tabs, tile_size, material_thickness, offset, rim=1, inside=False, configuration="", bricks=False):

    slot_height = SLOT_HEIGHT
    slot_width = material_thickness

    right_side = True

    if not inside:
        width = x_size * tile_size + rim * 2
    else:
        width = x_size * tile_size - 0.5 * material_thickness

    # check if configuration contains -r
    if "-r" in configuration:
        width -= ( offset + rim + material_thickness )
        right_side = False

    # Calculating total space needed for all tabs
    total_tab_height = total_tabs * slot_height

    # Remaining space after subtracting the space needed for tabs
    remaining_space = height - total_tab_height

    # Space between the top of the shape and the first tab, and between tabs
    space_between_tabs = remaining_space / (total_tabs + 1)

    # Dynamic points calculation starting from bottom left, moving up and then down the right side
    points = [[0, 0]]

    # Generating tab points dynamically on the left side
    for i in range(1, total_tabs + 1):
        tab_start_y = space_between_tabs * i + slot_height * (i - 1)
        points += [
            [0, tab_start_y],
            [-slot_width - offset, tab_start_y],  # Left side of the tab
            [-slot_width - offset, tab_start_y + slot_height],  # Bottom side of the tab
            [0, tab_start_y + slot_height],  # Right side of the tab
        ]

    # Add top left corner
    points += [
        [0, height],
        [width, height],
    ]

    if right_side:
        # Generating tab points dynamically on the right side, in reverse order to keep the polygon continuous
        for i in range(total_tabs, 0, -1):
            tab_start_y = space_between_tabs * i + slot_height * (i - 1)
            points += [
                [width, tab_start_y + slot_height],
                [width + slot_width + offset, tab_start_y + slot_height],  # Right side of the tab
                [width + slot_width + offset, tab_start_y],  # Bottom side of the tab
                [width, tab_start_y],  # Left side of the tab
            ]
    else:
            points += [ [width + slot_width + offset, height], [width + slot_width + offset, 0] ]

    # Closing the shape by returning to the starting point
    points += [
        [width, 0],
        [0, 0]
    ]

    # And move all the points to left by the rim
    for i in range(len(points)):
        points[i][0] -= rim

    if bricks:

        area = 25 - 1
        bricklines = []
        brick_size = 25

        # We want 5 rows of bricks, that means 7 lines
        number_of_lines = 6

        # The space between the lines
        space = area / (number_of_lines - 1)
        v_space = space

        # Create the lines, start at x + 0.5, and at half
        for i in range(number_of_lines):
            bricklines.append([(0, i * space + 0.5), (x_size*tile_size, i * space + 0.5)])

        number_of_brick = x_size
        number_of_brick += 1

        half_brick = False

        for j in range(number_of_lines - 1):
            brickline = []
            for i in range(int(number_of_brick)):
                brickline.append([(i * brick_size, j * v_space + 0.5), (i * brick_size, (j + 1) * v_space + 0.5)])

            if half_brick:
                # move all the lines to left by 12.5
                for i in range(len(brickline)):
                    brickline[i][0] = (brickline[i][0][0] - 12.5, brickline[i][0][1])
                    brickline[i][1] = (brickline[i][1][0] - 12.5, brickline[i][1][1])

                brickline[0][0] = (0, brickline[0][0][1])
                brickline[0][1] = (0, brickline[0][1][1])

                brickline.append([(x_size*tile_size, j * v_space + 0.5), (x_size*tile_size, (j + 1) * v_space + 0.5)])

            half_brick = not half_brick
            bricklines.extend(brickline)
##
        bricks = bricklines

    return points, bricks

def create_slots(x_size, height, total_tabs, tile_size, material_thickness, offset, rim=1, inside=False, configuration=""):

    slot_height = SLOT_HEIGHT
    slot_width = material_thickness

    width = x_size * tile_size + rim * 2
    x_point = width / 2

    # Calculating total space needed for all tabs
    total_tab_height = total_tabs * slot_height

    # Remaining space after subtracting the space needed for tabs
    remaining_space = height - total_tab_height

    # Space between the top of the shape and the first tab, and between tabs
    space_between_tabs = remaining_space / (total_tabs + 1)

    # Dynamic points calculation starting from bottom left, moving up and then down the right side
    points = list()

    # Generating tab points dynamically on the left side
    for i in range(1, total_tabs + 1):

        slot = []

        tab_start_y = space_between_tabs * i + slot_height * (i - 1)
        slot += [
            [x_point, tab_start_y],
            [x_point + slot_width + offset, tab_start_y],  # Left side of the tab
            [x_point + slot_width + offset, tab_start_y + slot_height],  # Bottom side of the tab
            [x_point,  tab_start_y + slot_height],
            [x_point, tab_start_y]
        ]

        points.append(slot)

    return points


def create_slotted_wall(x_size, height, total_tabs, tile_size, material_thickness, offset, rim=1, inside=False, configuration="", bricks=False):

    slot_height = SLOT_HEIGHT
    slot_width = material_thickness

    if not inside:
        width = x_size * tile_size + 2 * material_thickness + 2 * offset + rim * 2
    else:
        width = x_size * tile_size

    # check if configuration contains low case r
    if "r" in configuration:
        width -= ( offset + rim * 2 + material_thickness )


    # Calculating total space needed for all tabs
    total_tab_height = total_tabs * slot_height

    # Remaining space after subtracting the space needed for tabs
    remaining_space = height - total_tab_height

    # Space between the top of the shape and the first tab, and between tabs
    space_between_tabs = remaining_space / (total_tabs + 1)

    # Dynamic points calculation starting from bottom left, moving up and then down the right side
    points = [[0, 0]]

    # Generating recessed tab points dynamically on the left side
    for i in range(1, total_tabs + 1):
        tab_start_y = space_between_tabs * i + slot_height * (i - 1)
        points += [
            [0, tab_start_y],
            [slot_width + offset, tab_start_y],  # Inward from the left side
            [slot_width + offset, tab_start_y + slot_height],  # Bottom side of the recess
            [0, tab_start_y + slot_height],  # Back to the edge
        ]

    # Add top left corner
    points += [
        [0, height],
        [width, height],
    ]

    # Generating recessed tab points dynamically on the right side, in reverse order
    for i in range(total_tabs, 0, -1):
        tab_start_y = space_between_tabs * i + slot_height * (i - 1)
        points += [
            [width, tab_start_y + slot_height],
            [width - (slot_width + offset), tab_start_y + slot_height],  # Inward from the right side
            [width - (slot_width + offset), tab_start_y],  # Bottom side of the recess
            [width, tab_start_y],  # Back to the edge
        ]

    # Closing the shape by returning to the starting point
    points += [
        [width, 0],
        [0, 0]
    ]

    # And move all the points to left by the material thickness
    for i in range(len(points)):
        points[i][0] -= ( material_thickness + offset + rim )

    if bricks:

        area = 25 - 1
        bricklines = []
        brick_size = 25

        # We want 5 rows of bricks, that means 7 lines
        number_of_lines = 6

        # The space between the lines
        space = area / (number_of_lines - 1)
        v_space = space

        # Create the lines, start at x + 0.5, and at half
        for i in range(number_of_lines):
            bricklines.append([(0, i * space + 0.5), (x_size * tile_size, i * space + 0.5)])

        number_of_brick = x_size
        number_of_brick += 1

        half_brick = False

        for j in range(number_of_lines - 1):
            brickline = []
            for i in range(int(number_of_brick)):
                brickline.append([(i * brick_size, j * v_space + 0.5), (i * brick_size, (j + 1) * v_space + 0.5)])

            if half_brick:
                # move all the lines to left by 12.5
                for i in range(len(brickline)):
                    brickline[i][0] = (brickline[i][0][0] - 12.5, brickline[i][0][1])
                    brickline[i][1] = (brickline[i][1][0] - 12.5, brickline[i][1][1])

                brickline[0][0] = (0, brickline[0][0][1])
                brickline[0][1] = (0, brickline[0][1][1])

                brickline.append(
                    [(x_size * tile_size, j * v_space + 0.5), (x_size * tile_size, (j + 1) * v_space + 0.5)])

            half_brick = not half_brick
            bricklines.extend(brickline)
        ##
        bricks = bricklines

    return points, bricks

# predefined wall pieces
def single_slotted_wall(inside=True):

    points = create_slotted_wall(1, 25, 2, 25, 4, 0.25, inside=inside)
    return points

def tabbed_wall(size=1, inside=False, configuration=""):

    points = create_tabbed_wall(size, 25, 2, 25, 4, 0.25, inside=inside, configuration=configuration, bricks=True)

    if points[1]:
        return points
    else:
        return points[0]

def insert_tabbed_wall(size=1, inside=False, configuration=""):

    points = create_tabbed_wall(size, 25, 2, 25, 4, 0.25, inside=inside, configuration=configuration)
    slots = create_slots(size, 25, 2, 25, 4, 0.25, inside=inside, configuration=configuration)

    slots.append(points)

    return slots


def slotted_wall(size=1, inside=False, configuration=""):

    points = create_slotted_wall(size, 25, 2, 25, 4, 0, inside=inside, configuration=configuration, bricks=True)
    return points

def one_tile_door(inside=False):

    points_door = [[0, 0], [0, 4.33], [-4.25, 4.33], [-4.25, 10.33], [0, 10.33], [0, 14.67], [-4.25, 14.67], [-4.25, 20.67], [0, 20.67], [0.0, 33.5], [0.1, 34.2], [0.1, 34.9], [0.3, 35.6], [0.4, 36.3], [0.5, 37.0], [0.7, 37.6], [0.9, 38.3], [1.1, 38.9], [1.4, 39.6], [1.6, 40.2], [1.9, 40.8], [2.2, 41.4], [2.6, 41.9], [2.9, 42.5], [3.3, 43.0], [3.7, 43.5], [4.1, 43.9], [4.5, 44.3], [4.9, 44.7], [5.4, 45.1], [5.8, 45.5], [6.3, 45.8], [6.8, 46.0], [7.2, 46.3], [7.7, 46.5], [8.3, 46.6], [8.8, 46.8], [9.3, 46.9], [9.8, 46.9], [10.5, 46.9], [11.2, 46.9], [11.7, 46.9], [12.2, 46.8], [12.7, 46.6], [13.3, 46.5], [13.8, 46.3], [14.2, 46.0], [14.7, 45.8], [15.2, 45.5], [15.6, 45.1], [16.1, 44.7], [16.5, 44.3], [16.9, 43.9], [17.3, 43.5], [17.7, 43.0], [18.1, 42.5], [18.4, 41.9], [18.8, 41.4], [19.1, 40.8], [19.4, 40.2], [19.6, 39.6], [19.9, 38.9], [20.1, 38.3], [20.3, 37.6], [20.5, 37.0], [20.6, 36.3], [20.7, 35.6], [20.9, 34.9], [20.9, 34.2], [21.0, 33.5], [21.0, 20.67], [25.25, 20.67], [25.25, 14.67], [21.0, 14.67], [21.0, 10.33], [25.25, 10.33], [25.25, 4.33], [21.0, 4.33], [21.0, 0.0], [0.0, 0.0]]
    points_frame = [[10.5, 44.4], [11.1, 44.4], [11.5, 44.3], [11.8, 44.3], [12.2, 44.2], [12.6, 44.0], [13.0, 43.9], [13.4, 43.7], [13.7, 43.5], [14.1, 43.3], [14.5, 43.0], [14.8, 42.7], [15.2, 42.4], [15.5, 42.0], [15.8, 41.7], [16.1, 41.3], [16.4, 40.9], [16.7, 40.4], [17.0, 40.0], [17.2, 39.5], [17.5, 39.0], [17.7, 38.5], [17.9, 37.9], [18.1, 37.4], [18.3, 36.8], [18.4, 36.2], [18.5, 35.7], [18.7, 35.1], [18.7, 34.5], [18.8, 33.9], [18.9, 33.2], [18.9, 2.0], [2.1, 2.0], [2.1, 33.2], [2.2, 33.9], [2.3, 34.5], [2.3, 35.1], [2.5, 35.7], [2.6, 36.2], [2.7, 36.8], [2.9, 37.4], [3.1, 37.9], [3.3, 38.5], [3.5, 39.0], [3.8, 39.5], [4.0, 40.0], [4.3, 40.4], [4.6, 40.9], [4.9, 41.3], [5.2, 41.7], [5.5, 42.0], [5.8, 42.4], [6.2, 42.7], [6.5, 43.0], [6.9, 43.3], [7.3, 43.5], [7.6, 43.7], [8.0, 43.9], [8.4, 44.0], [8.8, 44.2], [9.2, 44.3], [9.5, 44.3], [9.9, 44.4], [10.5, 44.4]]

    return points_door, points_frame

def double_door(width=2, style="tabs", position = 1):

    tile_size = 25
    material_thickness = 4
    offset = 0.25

    points_frame = [(19.849249672179763, 48.684171110747634), (19.87224816348115, 48.71545344963746), (19.90480971620229, 48.75172970182263), (19.940748998152777, 48.784662803727834), (19.97972441059956, 48.81393973001489), (20.021365496739143, 48.83928220687352), (20.065276462846786, 48.86044935698183), (20.111039940250244, 48.87723998901751), (23.311039940250247, 49.87723998901751), (23.359900501356226, 49.88984133779659), (23.409782342306425, 49.89745385157735), (23.46017743681822, 49.9), (26.66017743681822, 49.9), (26.710572531330016, 49.89745385157735), (26.760454372280215, 49.88984133779659), (26.809314933386194, 49.87723998901751), (30.009314933386193, 48.87723998901751), (30.05507841078965, 48.86044935698183), (30.098989376897293, 48.83928220687352), (30.140630463036878, 48.81393973001489), (30.17960587548366, 48.784662803727834), (30.215545157434146, 48.75172970182263), (30.248106710155287, 48.71545344963746), (30.271105201456674, 48.684171110747634), (32.8283456353173, 47.77087095579741), (32.87755196973381, 47.75027581818229), (35.77755196973381, 46.35027581818229), (35.826584071661294, 46.323116420044876), (38.52658407166129, 44.62311642004488), (38.574345990362026, 44.588970590101866), (41.17434599036203, 42.488970590101864), (41.20250536529651, 42.46443324407052), (41.22875450691859, 42.43786231425867), (43.428754506918594, 40.037862314258675), (43.4739153240141, 39.98075070916863), (45.3739153240141, 37.18075070916863), (45.40739103231818, 37.12360679774998), (47.00739103231818, 33.92360679774998), (47.0331504097912, 33.862162162162164), (48.23315040979119, 30.36216216216216), (48.25146255966675, 30.292945834052425), (48.95146255966675, 26.592945834052426), (48.958844298614004, 26.536487819155788), (49.258844298614, 22.436487819155786), (49.26017743681822, 22.4), (49.26017743681822, 0.5), (49.257769800154314, 0.45099142983521967), (49.25057007701983, 0.4024548389919359), (49.238647604684324, 0.35485766137276886), (49.222117203073864, 0.3086582838174551), (49.20113806899239, 0.26430163158700115), (49.17591224296949, 0.2222148834901989), (49.14668266349959, 0.18280335791817726), (49.113730827411494, 0.14644660940672627), (49.07737407890004, 0.1134947733186315), (49.03796255332802, 0.08426519384872738), (48.995875805231215, 0.05903936782582253), (48.95151915300076, 0.03806023374435663), (48.90531977544545, 0.021529832133895532), (48.85772259782628, 0.009607359798384785), (48.809186006983, 0.002407636663901591), (48.76017743681822, 0.0), (1.3601774368182191, 0.0), (1.3111688666534391, 0.0024076366639015356), (1.2626322758101551, 0.00960735979838484), (1.215035098190988, 0.021529832133895588), (1.1688357206356734, 0.03806023374435674), (1.124479068405222, 0.05903936782582253), (1.0823923203084185, 0.08426519384872738), (1.0429807947363976, 0.11349477331863167), (1.006624046224946, 0.14644660940672627), (0.9736722101368507, 0.18280335791817737), (0.9444426306669449, 0.22221488349019902), (0.9192168046440408, 0.26430163158700115), (0.8982376705625761, 0.3086582838174552), (0.8817072689521162, 0.354857661372769), (0.869784796616603, 0.4024548389919358), (0.8625850734821192, 0.4509914298352197), (0.8601774368182191, 0.5), (0.8601774368182191, 22.4), (0.8615105750224359, 22.436487819155786), (1.1615105750224366, 26.536487819155788), (1.1688923139696854, 26.592945834052426), (1.8688923139696847, 30.292945834052425), (1.8872044638452472, 30.36216216216216), (3.0872044638452465, 33.862162162162164), (3.112963841318262, 33.92360679774998), (4.71296384131826, 37.12360679774998), (4.746439549622341, 37.18075070916863), (6.64643954962234, 39.98075070916863), (6.69160036671785, 40.037862314258675), (8.89160036671785, 42.43786231425867), (8.91784950833993, 42.46443324407052), (8.94600888327441, 42.488970590101864), (11.546008883274409, 44.588970590101866), (11.59377080197515, 44.62311642004488), (14.29377080197515, 46.323116420044876), (14.342802903902632, 46.35027581818229), (17.242802903902636, 47.75027581818229), (17.292009238319142, 47.77087095579741), (19.849249672179763, 48.684171110747634)]
    points_door = [(21.485199425996132, 43.16959470588059), (21.51528851521862, 43.13798945905144), (21.552195292133394, 43.106112962189236), (21.592031867753445, 43.07798346739621), (21.63441928131858, 43.053868567319675), (21.678954306240744, 43.033997664229354), (23.478954306240745, 42.33399766422935), (23.5228799463665, 42.319220009655496), (23.567985159173407, 42.30857291085791), (23.61388242937164, 42.302147840935156), (23.66017743681822, 42.3), (26.46017743681822, 42.3), (26.5064724442648, 42.302147840935156), (26.552369714463033, 42.30857291085791), (26.59747492726994, 42.319220009655496), (26.641400567395696, 42.33399766422935), (28.441400567395693, 43.033997664229354), (28.48593559231786, 43.053868567319675), (28.528323005882992, 43.07798346739621), (28.568159581503043, 43.106112962189236), (28.605066358417815, 43.13798945905144), (28.635155447640305, 43.16959470588059), (30.670998734665243, 42.436691122551615), (33.020673370478235, 41.35975691447066), (35.167713275870376, 39.99345879285748), (37.21491870490038, 38.33619725507129), (38.96759575259465, 36.388778313188766), (40.52679287820268, 34.14743244512722), (41.696911175966, 31.709685991453615), (42.67599093580791, 28.870354687912087), (43.26290728783136, 25.837953535790923), (43.46017743681822, 22.385725928520927), (43.46017743681822, 3.0), (6.66017743681822, 3.0), (6.66017743681822, 22.38572592852094), (6.857447585805076, 25.83795353579093), (7.444363937828527, 28.870354687912094), (8.423443697670418, 31.709685991453576), (9.593561995433777, 34.147432445127244), (11.152759121041777, 36.38877831318875), (12.905436168736061, 38.33619725507129), (14.952641597766082, 39.99345879285749), (17.099681503158195, 41.35975691447065), (19.449356138971194, 42.436691122551615), (21.485199425996132, 43.16959470588059)]

    drawings = [[(43.9, 0.5), (43.9, 22.4)], [(43.9, 22.4), (48.7, 22.4)], [(48.7, 22.4), (48.7, 0.5)], [(48.7, 0.5), (43.9, 0.5)], [(48.7, 22.4), (48.4, 26.5)], [(48.4, 26.5), (47.7, 30.2)], [(47.7, 30.2), (46.5, 33.7)], [(46.5, 33.7), (44.9, 36.9)], [(44.9, 36.9), (43.0, 39.7)], [(43.0, 39.7), (40.8, 42.1)], [(40.8, 42.1), (38.2, 44.2)], [(38.2, 44.2), (35.5, 45.9)], [(35.5, 45.9), (32.6, 47.3)], [(32.6, 47.3), (29.8, 48.3)], [(43.9, 22.4), (43.7, 25.9)], [(43.7, 25.9), (43.1, 29.0)], [(43.1, 29.0), (42.1, 31.9)], [(42.1, 31.9), (40.9, 34.4)], [(40.9, 34.4), (39.3, 36.7)], [(39.3, 36.7), (37.5, 38.7)], [(37.5, 38.7), (35.4, 40.4)], [(35.4, 40.4), (33.2, 41.8)], [(33.2, 41.8), (30.8, 42.9)], [(30.8, 42.9), (28.3, 43.8)], [(32.6, 47.3), (30.8, 42.9)], [(35.5, 45.9), (33.2, 41.8)], [(38.2, 44.2), (35.4, 40.4)], [(40.8, 42.1), (37.5, 38.7)], [(43.0, 39.7), (39.3, 36.7)], [(44.9, 36.9), (40.9, 34.4)], [(46.5, 33.7), (42.1, 31.9)], [(47.7, 30.2), (43.1, 29.0)], [(48.4, 26.5), (43.7, 25.9)], [(29.8, 48.4), (26.6, 49.4)], [(29.8, 48.4), (28.2, 43.5)], [(28.2, 43.5), (26.4, 42.8)], [(26.6, 49.4), (26.4, 42.8)], [(26.4, 42.8), (25.0, 42.8)], [(23.6, 42.8), (25.0, 42.8)], [(21.8, 43.5), (23.6, 42.8)], [(23.4, 49.4), (23.6, 42.8)], [(20.2, 48.4), (23.4, 49.4)], [(23.4, 49.4), (25.0, 49.4)], [(26.6, 49.4), (25.0, 49.4)], [(20.2, 48.4), (21.8, 43.5)], [(6.1, 0.5), (6.1, 22.4)], [(1.3, 0.5), (6.1, 0.5)], [(1.3, 22.4), (1.3, 0.5)], [(6.1, 22.4), (1.3, 22.4)], [(1.3, 22.4), (1.6, 26.5)], [(1.6, 26.5), (2.3, 30.2)], [(1.6, 26.5), (6.3, 25.9)], [(6.1, 22.4), (6.3, 25.9)], [(6.3, 25.9), (6.9, 29.0)], [(6.9, 29.0), (7.9, 31.9)], [(2.3, 30.2), (6.9, 29.0)], [(7.9, 31.9), (9.1, 34.4)], [(3.5, 33.7), (7.9, 31.9)], [(2.3, 30.2), (3.5, 33.7)], [(3.5, 33.7), (5.1, 36.9)], [(5.1, 36.9), (7.0, 39.7)], [(5.1, 36.9), (9.1, 34.4)], [(7.0, 39.7), (9.2, 42.1)], [(7.0, 39.7), (10.7, 36.7)], [(9.1, 34.4), (10.7, 36.7)], [(10.7, 36.7), (12.5, 38.7)], [(12.5, 38.7), (14.6, 40.4)], [(9.2, 42.1), (12.5, 38.7)], [(14.6, 40.4), (16.8, 41.8)], [(11.8, 44.2), (14.6, 40.4)], [(9.2, 42.1), (11.8, 44.2)], [(11.8, 44.2), (14.5, 45.9)], [(14.5, 45.9), (17.4, 47.3)], [(14.5, 45.9), (16.8, 41.8)], [(17.4, 47.3), (20.2, 48.3)], [(17.4, 47.3), (19.2, 42.9)], [(16.8, 41.8), (19.2, 42.9)], [(19.2, 42.9), (21.7, 43.8)]]

    # first, we need to calculate the width of the whole wall
    # width = width * tile_size - 0.5 * material_thickness

    if style == "tabs":
        wall = create_tabbed_wall(width, 25, 2, 25, 4, 0.25)
    else:
        wall = create_slotted_wall(width, 25, 2, 25, 4, 0.25)

    wall = wall[0]

    # The door is at tile 1 as the middle
    # Move it so it is a at half the width
    half = tile_size * position

    # move all the x coordinates by half
    for i in range(len(points_door)):
        points_door[i] = [points_door[i][0] + half, points_door[i][1]]

    for i in range(len(points_frame)):
        points_frame[i] = [points_frame[i][0] + half, points_frame[i][1]]

    for i in range(len(drawings)):
        for j in range(len(drawings[i])):
            drawings[i][j] = (drawings[i][j][0] + half, drawings[i][j][1])

    # We are going to make some brick lines, first the horizontal lines
    # The height is 25, we wee need a half on each side for offset
    area = 25 - 1
    bricklines = []

    # We want 5 rows of bricks, that means 7 lines
    number_of_lines = 6

    # The space between the lines
    space = area / ( number_of_lines - 1 )
    v_space = space

    # Create the lines, start at x + 0.5, and at half
    for i in range(number_of_lines):
        bricklines.append([(0, i * space + 0.5), (half, i * space + 0.5 )])

    # Create the lines, start at x + 0.5, and at half
    for i in range(number_of_lines):
        bricklines.append([(half + 2 * tile_size, i * space + 0.5), (width * tile_size, i * space + 0.5 )])

    # See how much space we have
    # On the left its half * tilesize
    space = half

    brick_size = 25

    number_of_brick = space / brick_size
    number_of_brick += 1

    half_brick = False

    for j in range(number_of_lines-1):
        brickline = []
        for i in range(int(number_of_brick)):
            brickline.append([(i * brick_size, j * v_space + 0.5), (i * brick_size, (j +  1) * v_space + 0.5)])

        if half_brick:
            # move all the lines to left by 12.5
            for i in range(len(brickline)):
                brickline[i][0] = (brickline[i][0][0] - 12.5, brickline[i][0][1])
                brickline[i][1] = (brickline[i][1][0] - 12.5, brickline[i][1][1])

            brickline[0][0] = (0, brickline[0][0][1])
            brickline[0][1] = (0, brickline[0][1][1])

            brickline.append([(half, j * v_space + 0.5), (space, (j + 1) * v_space + 0.5)])

        half_brick = not half_brick
        bricklines.extend(brickline)

    # See how much space we have
    # On the right its width * tilesize - half * tilesize
    space = width * tile_size - ( 2 * tile_size) - half
    offset = half + (2 * tile_size )

    number_of_brick = space / brick_size
    number_of_brick += 1

    half_brick = False

    for j in range(number_of_lines-1):
        brickline = []
        for i in range(int(number_of_brick)):
            brickline.append([(i * brick_size + offset, j * v_space + 0.5), (i * brick_size + offset, (j +  1) * v_space + 0.5)])

        if half_brick:
            # move all the lines to left by 12.5
            for i in range(len(brickline)):
                brickline[i][0] = (brickline[i][0][0] - 12.5, brickline[i][0][1])
                brickline[i][1] = (brickline[i][1][0] - 12.5, brickline[i][1][1])

            brickline[0][0] = (offset, brickline[0][0][1])
            brickline[0][1] = (offset, brickline[0][1][1])

            brickline.append([(space+offset, j * v_space + 0.5), (space + offset, (j + 1) * v_space + 0.5)])

        half_brick = not half_brick
        bricklines.extend(brickline)

#####

    drawings += bricklines

    polygon1 = Polygon(wall)
    polygon2 = Polygon(points_frame)

    # Combine the two polygons into one
    combined_polygon = unary_union([polygon1, polygon2])
    # If you need the combined outline as a list of points
    combined_outline_points = list(combined_polygon.exterior.coords)

    return points_door, combined_outline_points, drawings

def single_door(width=2, style="tabs", position = 1):

    tile_size = 25
    material_thickness = 4
    offset = 0.25

    points_frame = [[0, 0], [0, 20.67], [0.0, 33.5], [0.1, 34.2], [0.1, 34.9], [0.3, 35.6], [0.4, 36.3], [0.5, 37.0], [0.7, 37.6], [0.9, 38.3], [1.1, 38.9], [1.4, 39.6], [1.6, 40.2], [1.9, 40.8], [2.2, 41.4], [2.6, 41.9], [2.9, 42.5], [3.3, 43.0], [3.7, 43.5], [4.1, 43.9], [4.5, 44.3], [4.9, 44.7], [5.4, 45.1], [5.8, 45.5], [6.3, 45.8], [6.8, 46.0], [7.2, 46.3], [7.7, 46.5], [8.3, 46.6], [8.8, 46.8], [9.3, 46.9], [9.8, 46.9], [10.5, 46.9], [11.2, 46.9], [11.7, 46.9], [12.2, 46.8], [12.7, 46.6], [13.3, 46.5], [13.8, 46.3], [14.2, 46.0], [14.7, 45.8], [15.2, 45.5], [15.6, 45.1], [16.1, 44.7], [16.5, 44.3], [16.9, 43.9], [17.3, 43.5], [17.7, 43.0], [18.1, 42.5], [18.4, 41.9], [18.8, 41.4], [19.1, 40.8], [19.4, 40.2], [19.6, 39.6], [19.9, 38.9], [20.1, 38.3], [20.3, 37.6], [20.5, 37.0], [20.6, 36.3], [20.7, 35.6], [20.9, 34.9], [20.9, 34.2], [21.0, 33.5], [21.0, 20.67], [21.0, 0.0], [0.0, 0.0]]
    points_door = [[10.5, 44.4], [11.1, 44.4], [11.5, 44.3], [11.8, 44.3], [12.2, 44.2], [12.6, 44.0], [13.0, 43.9], [13.4, 43.7], [13.7, 43.5], [14.1, 43.3], [14.5, 43.0], [14.8, 42.7], [15.2, 42.4], [15.5, 42.0], [15.8, 41.7], [16.1, 41.3], [16.4, 40.9], [16.7, 40.4], [17.0, 40.0], [17.2, 39.5], [17.5, 39.0], [17.7, 38.5], [17.9, 37.9], [18.1, 37.4], [18.3, 36.8], [18.4, 36.2], [18.5, 35.7], [18.7, 35.1], [18.7, 34.5], [18.8, 33.9], [18.9, 33.2], [18.9, 2.0], [2.1, 2.0], [2.1, 33.2], [2.2, 33.9], [2.3, 34.5], [2.3, 35.1], [2.5, 35.7], [2.6, 36.2], [2.7, 36.8], [2.9, 37.4], [3.1, 37.9], [3.3, 38.5], [3.5, 39.0], [3.8, 39.5], [4.0, 40.0], [4.3, 40.4], [4.6, 40.9], [4.9, 41.3], [5.2, 41.7], [5.5, 42.0], [5.8, 42.4], [6.2, 42.7], [6.5, 43.0], [6.9, 43.3], [7.3, 43.5], [7.6, 43.7], [8.0, 43.9], [8.4, 44.0], [8.8, 44.2], [9.2, 44.3], [9.5, 44.3], [9.9, 44.4], [10.5, 44.4]]

    drawings = []

    # Now the coordinates are way over the grid, we need to find the lower left corner and move all the coordinates to account for that
    min_x = min([x[0] for x in points_door])
    min_y = min([x[1] for x in points_door])

    # Move all the coordinates to account for the lower left corner
    points_door = [[x[0] - min_x, x[1]] for x in points_door]

    min_x = min([x[0] for x in points_frame])
    min_y = min([x[1] for x in points_frame])

    # Move all the coordinates to account for the lower left corner
    points_frame = [[x[0] - min_x, x[1]] for x in points_frame]

    # Now find the center of the all the polygons and move them so that the center becomes x=12.5
    # This is the center of the door
    center_x = (max([x[0] for x in points_door]) + min([x[0] for x in points_door])) / 2
    center_x_frame = (max([x[0] for x in points_frame]) + min([x[0] for x in points_frame])) / 2

    # Move all the coordinates to account for the center
    points_door = [[x[0] - center_x + 12.5, x[1] ] for x in points_door]
    points_frame = [[x[0] - center_x_frame + 12.5, x[1] ] for x in points_frame]


    # first, we need to calculate the width of the whole wall
    # width = width * tile_size - 0.5 * material_thickness

    if style == "tabs":
        wall = create_tabbed_wall(width, 25, 2, 25, 4, 0.25)
    else:
        wall = create_slotted_wall(width, 25, 2, 25, 4, 0.25)

    wall = wall[0]

    # The door is at tile 1 as the middle
    # Move it so it is a at half the width
    half = tile_size * position

    # move all the x coordinates by half
    for i in range(len(points_door)):
        points_door[i] = [points_door[i][0] + half, points_door[i][1]]

    for i in range(len(points_frame)):
        points_frame[i] = [points_frame[i][0] + half, points_frame[i][1]]

    for i in range(len(drawings)):
        for j in range(len(drawings[i])):
            drawings[i][j] = (drawings[i][j][0] + half, drawings[i][j][1])

    # We are going to make some brick lines, first the horizontal lines
    # The height is 25, we wee need a half on each side for offset
    area = 25 - 1
    bricklines = []

    # We want 5 rows of bricks, that means 7 lines
    number_of_lines = 6

    # The space between the lines
    space = area / ( number_of_lines - 1 )
    v_space = space

    # Create the lines, start at x + 0.5, and at half
    for i in range(number_of_lines):
        bricklines.append([(0, i * space + 0.5), (half, i * space + 0.5 )])

    # Create the lines, start at x + 0.5, and at half
    for i in range(number_of_lines):
        bricklines.append([(half + 1 * tile_size, i * space + 0.5), (width * tile_size, i * space + 0.5 )])

    # See how much space we have
    # On the left its half * tilesize
    space = half

    brick_size = 25

    number_of_brick = space / brick_size
    number_of_brick += 1

    half_brick = False

    for j in range(number_of_lines-1):
        brickline = []
        for i in range(int(number_of_brick)):
            brickline.append([(i * brick_size, j * v_space + 0.5), (i * brick_size, (j +  1) * v_space + 0.5)])

        if half_brick:
            # move all the lines to left by 12.5
            for i in range(len(brickline)):
                brickline[i][0] = (brickline[i][0][0] - 12.5, brickline[i][0][1])
                brickline[i][1] = (brickline[i][1][0] - 12.5, brickline[i][1][1])

            brickline[0][0] = (0, brickline[0][0][1])
            brickline[0][1] = (0, brickline[0][1][1])

            brickline.append([(half, j * v_space + 0.5), (space, (j + 1) * v_space + 0.5)])

        half_brick = not half_brick
        bricklines.extend(brickline)

    # See how much space we have
    # On the right its width * tilesize - half * tilesize
    space = width * tile_size - ( 1 * tile_size) - half
    offset = half + (1 * tile_size )

    number_of_brick = space / brick_size
    number_of_brick += 1

    half_brick = False

    for j in range(number_of_lines-1):
        brickline = []
        for i in range(int(number_of_brick)):
            brickline.append([(i * brick_size + offset, j * v_space + 0.5), (i * brick_size + offset, (j +  1) * v_space + 0.5)])

        if half_brick:
            # move all the lines to left by 12.5
            for i in range(len(brickline)):
                brickline[i][0] = (brickline[i][0][0] - 12.5, brickline[i][0][1])
                brickline[i][1] = (brickline[i][1][0] - 12.5, brickline[i][1][1])

            brickline[0][0] = (offset, brickline[0][0][1])
            brickline[0][1] = (offset, brickline[0][1][1])

            brickline.append([(space+offset, j * v_space + 0.5), (space + offset, (j + 1) * v_space + 0.5)])

        half_brick = not half_brick
        bricklines.extend(brickline)

#####

    drawings += bricklines

    polygon1 = Polygon(wall)
    polygon2 = Polygon(points_frame)

    # Combine the two polygons into one
    combined_polygon = unary_union([polygon1, polygon2])
    # If you need the combined outline as a list of points
    combined_outline_points = list(combined_polygon.exterior.coords)

    return points_door, combined_outline_points, drawings