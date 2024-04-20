from svgpathtools import parse_path

def extract_points_from_svg_path(path_data):
    path = parse_path(path_data)
    points = []

    for segment in path:
        # Extracting start and end points from each segment
        start_point = (segment.start.real, segment.start.imag)
        end_point = (segment.end.real, segment.end.imag)
        points.append(start_point)
        if segment.end not in [p[1] for p in points]:  # Avoid duplicating the last point
            points.append(end_point)

    return points

# Example usage
path_data = "M 10,10 L 20,20 C 30,30 40,40 50,50 Z"
points = extract_points_from_svg_path(path_data)
print(points)