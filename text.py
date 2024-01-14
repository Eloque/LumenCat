from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

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

        # Add the path to the list
        svg_paths.append(path)

        # Update the current x position based on the glyph's advance width
        current_x += glyph.width

    return svg_paths




