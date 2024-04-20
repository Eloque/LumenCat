import random

def generate_bricks(min_x, max_x, min_y, max_y, min_length, max_length, height):
    bricks = []
    current_y = min_y + 1
    min_x = min_x + 1
    mortar_space = 1  # Space between bricks

    while current_y + height <= max_y:  # Ensure there's enough space for a brick plus vertical mortar
        current_x = min_x
        row = []
        while current_x < max_x:
            space_left = max_x - current_x
            if space_left < min_length + mortar_space:
                # If space left is less than the minimum size for a new brick plus mortar,
                # extend the previous brick instead of creating a new one.
                if row:  # Check if there's at least one brick in the current row
                    last_brick = row[-1]
                    # Extend the last brick to the end of the row minus mortar space
                    extended_brick = (last_brick[0], (max_x - mortar_space, last_brick[1][1]))
                    row[-1] = extended_brick
                # No more bricks can be added to this row, break the loop
                break
            else:
                # Space is sufficient for a new brick with mortar.
                length = random.randint(min_length, min(max_length, space_left - mortar_space))
                brick = ((current_x, current_y), (current_x + length, current_y + height))
                row.append(brick)
                current_x += length + mortar_space  # Move to the next position, including mortar space

        bricks.append(row)
        current_y += height + mortar_space  # Move to the next row, including vertical mortar space

    return bricks


def brick_to_path(top_left, bottom_right):
    """
    Generate a path (list of points) around a brick given its top-left and bottom-right coordinates.

    Args:
    - top_left (tuple): The (x, y) coordinates of the top-left corner of the brick.
    - bottom_right (tuple): The (x, y) coordinates of the bottom-right corner of the brick.

    Returns:
    - List of tuples representing the path around the brick.
    """
    # Unpack the top-left and bottom-right coordinates
    top_left_x, top_left_y = top_left
    bottom_right_x, bottom_right_y = bottom_right

    # Calculate the bottom-left and top-right coordinates
    bottom_left = (top_left_x, bottom_right_y)
    top_right = (bottom_right_x, top_left_y)

    # Define the path as a list of points starting from the top-left corner and moving clockwise
    path = [top_left, top_right, bottom_right, bottom_left, top_left]

    return path


def generate_bricks_with_y_variation(min_x, max_x, min_y, max_y, min_length, max_length, height, mortar_space,
                                     y_variation):
    bricks = []
    current_y = min_y + 1

    while current_y + height <= max_y:  # Ensure there's enough space for a brick plus vertical mortar
        current_x = min_x + 1
        row = []
        while current_x < max_x:
            space_left = max_x - current_x
            y_offset = random.randint(0, y_variation)  # Random Y-axis offset for each brick

            # Adjust the current_y with y_offset, but ensure bricks don't "overflow" the max_y
            adjusted_current_y = min(current_y + y_offset, max_y - height - mortar_space)

            if space_left < min_length + mortar_space:
                if row:  # Extend the previous brick if there's not enough space for a new one
                    last_brick = row[-1]
                    extended_brick = (last_brick[0], (max_x - mortar_space, last_brick[1][1]))
                    row[-1] = extended_brick
                break
            else:
                length = random.randint(min_length, min(max_length, space_left - mortar_space))
                brick = ((current_x, adjusted_current_y), (current_x + length, adjusted_current_y + height))
                row.append(brick)
                current_x += length + mortar_space  # Account for horizontal mortar space

        bricks.append(row)
        current_y += height + mortar_space  # Move to the next row, including vertical mortar space

    return bricks

def generate_stones(area_width, area_height, num_stones, min_size, max_size, mortar):
    grid = [[False] * area_height for _ in range(area_width)]  # Occupancy grid
    stones = []

    def can_place_stone(x, y, width, height):
        """Check if the stone can be placed without overlapping or going out of bounds."""
        if x + width + mortar > area_width or y + height + mortar > area_height:
            return False
        for i in range(max(0, x - mortar), min(area_width, x + width + mortar)):
            for j in range(max(0, y - mortar), min(area_height, y + height + mortar)):
                if grid[i][j]:  # Check if the cell is already occupied
                    return False
        return True

    def place_stone(x, y, width, height):
        """Mark the stone's position as occupied on the grid."""
        for i in range(x, x + width):
            for j in range(y, y + height):
                grid[i][j] = True
        stones.append(((x, y), (x + width, y + height)))

    for _ in range(num_stones):
        width, height = random.randint(min_size, max_size), random.randint(min_size, max_size)
        attempts = 0
        placed = False
        while not placed and attempts < 100:  # Limit attempts to avoid infinite loops
            x, y = random.randint(0, area_width - width), random.randint(0, area_height - height)
            if can_place_stone(x, y, width, height):
                place_stone(x, y, width, height)
                placed = True
            attempts += 1

    return stones