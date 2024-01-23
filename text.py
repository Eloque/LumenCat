# Convert text to SVG paths

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
import re

POINTS_PER_MM = 0.352778

def text_to_svg_path(text, font_path, font_size, start_x=0, start_y=0):
    font = TTFont(font_path)

    svg_paths = []
    units_per_em = font['head'].unitsPerEm

    # Static conversion factor from points to millimeters
    points_per_mm = POINTS_PER_MM
    font_size_pt = font_size * points_per_mm

    current_x = 0  # Horizontal cursor position

    for char in text:
        # Get the glyph object
        glyph = font.getGlyphSet().get(char)
        if glyph is None:  # Skip characters not found in the font

            if char == " ":
                # Get the advance width of the space character
                space_glyph = font.getGlyphSet().get("space")
                if space_glyph:
                    space_advance = space_glyph.width
                else:
                    # Default space width if "space" glyph does not exist
                    space_advance = font_size_pt

                current_x += space_advance
                continue

            continue

        # Create a pen for drawing the glyph path
        pen = SVGPathPen(font.getGlyphSet())

        # Apply a translation of the pen by 100mm in the y direction
        # This is to move the text down to the bed
        translate = Transform().translate(start_x, start_y)
        location_pen = TransformPen(pen, translate)

        # Apply scaling for font size and flip vertically
        scale = Transform().scale(font_size_pt / units_per_em, -font_size_pt / units_per_em)
        scaled_pen = TransformPen(location_pen, scale)

        # Apply translation along the x-axis and move down by the font's height
        translate = Transform().translate(current_x, -units_per_em)
        transformed_pen = TransformPen(scaled_pen, translate)

        # Draw the character with the scaled pen
        glyph.draw(transformed_pen)

        # Get the path
        path = pen.getCommands()

        # Check if there are any M commands in the path with a regex
        pattern = r'([MLCQAZHVmlcqazhv][^MLCQAZHVmlcqazhv]*)'
        components = re.findall(pattern, path)

        return_path = ""

        for item in components:
            if item[0] == "M":
                coordinates = re.split(r'[ ,]+', item[1:])

                # This is hack to fix an issue with the move command and the first line command being combined
                if len(coordinates) > 2:
                    move_command = f"M{coordinates[0]},{coordinates[1]} "
                    return_path += move_command

                    # Pop off the coordinates two at at a time
                    while len(coordinates) >= 2:
                        x = coordinates.pop(0)
                        y = coordinates.pop(0)
                        line_command = f"L{x},{y}"

                        return_path += line_command

                else:
                    return_path += item + " "

            else:
                return_path += item + " "


        # Add the path to the list, as an SVG element
        svg_paths.append(f"<path d='{return_path}' />")

        # Update the current x position based on the glyph's advance width
        current_x += glyph.width

    return svg_paths
