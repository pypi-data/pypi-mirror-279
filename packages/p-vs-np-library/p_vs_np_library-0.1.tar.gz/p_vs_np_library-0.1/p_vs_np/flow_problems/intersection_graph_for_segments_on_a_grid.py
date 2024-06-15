#Intersection graph for segments on a grid

def check_segment_intersections(segments):
    n = len(segments)

    for i in range(n):
        for j in range(i + 1, n):
            if do_segments_intersect(segments[i], segments[j]):
                return True

    return False

def do_segments_intersect(segment1, segment2):
    # Extract coordinates from line segments
    x1, y1, x2, y2 = segment1
    x3, y3, x4, y4 = segment2

    # Check for intersection based on relative positions
    if max(x1, x2) < min(x3, x4) or max(x3, x4) < min(x1, x2):
        return False

    if max(y1, y2) < min(y3, y4) or max(y3, y4) < min(y1, y2):
        return False

    orientation1 = calculate_orientation(x1, y1, x2, y2, x3, y3)
    orientation2 = calculate_orientation(x1, y1, x2, y2, x4, y4)
    orientation3 = calculate_orientation(x3, y3, x4, y4, x1, y1)
    orientation4 = calculate_orientation(x3, y3, x4, y4, x2, y2)

    # Check for proper intersection
    if orientation1 != orientation2 and orientation3 != orientation4:
        return True

    # Check for collinear segments
    if orientation1 == 0 and on_segment(x1, y1, x2, y2, x3, y3):
        return True

    if orientation2 == 0 and on_segment(x1, y1, x2, y2, x4, y4):
        return True

    if orientation3 == 0 and on_segment(x3, y3, x4, y4, x1, y1):
        return True

    if orientation4 == 0 and on_segment(x3, y3, x4, y4, x2, y2):
        return True

    return False

def calculate_orientation(x1, y1, x2, y2, x3, y3):
    val = (y2 - y1) * (x3 - x2) - (x2 - x1) * (y3 - y2)

    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2

def on_segment(x1, y1, x2, y2, x, y):
    if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
        return True

    return False

# Example usage:
segments = [
    (1, 1, 4, 1),
    (3, 0, 3, 3),
    (2, 2, 5, 2),
    (4, 1, 4, 4)
]

intersecting = check_segment_intersections(segments)

if intersecting:
    print("Segments intersect")
else:
    print("Segments do not intersect")
