import math

import numpy as np
from scipy.spatial import ConvexHull
from shapely.geometry import LineString
from sympy import Polygon

EARTH_RADIUS = 6378137  # meters


def convert_degrees_to_radius(degrees):
    return degrees * math.pi / 180


def haversine(lat1, lon1, lat2, lon2):
    distance_lat = math.radians(lat2 - lat1)
    distance_lon = math.radians(lon2 - lon1)
    a = math.sin(distance_lat / 2) * math.sin(distance_lat / 2) + math.cos(
        math.radians(lat1)
    ) * math.cos(math.radians(lat2)) * math.sin(distance_lon / 2) * math.sin(distance_lon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = EARTH_RADIUS * c
    return distance


def convert_to_cartesian(positions):
    # Find the minimum latitude and longitude to use as the origin
    min_lat = min(positions, key=lambda x: x[0])[0]
    min_lon = min(positions, key=lambda x: x[1])[1]

    # Create a list to hold Cartesian coordinates
    cartesian_coords = []

    # Convert each position to Cartesian coordinates
    for lat, lon in positions:
        # Distance from the minimum longitude to the current point's longitude (x-coordinate)
        x = haversine(min_lat, min_lon, min_lat, lon)
        # Distance from the minimum latitude to the current point's latitude (y-coordinate)
        y = haversine(min_lat, min_lon, lat, min_lon)

        # Append the calculated Cartesian coordinates to the list
        cartesian_coords.append((x, y))

    return cartesian_coords


def convert_to_lat_lon(ref_point, distance):
    """Convert a distance in meters to a latitude and longitude offset from a reference point."""
    lat_offset, lon_offset = ref_point
    distance_north, distance_east = distance

    delta_lat = distance_north / EARTH_RADIUS
    point_lat = lat_offset + math.degrees(delta_lat)

    r = EARTH_RADIUS * math.cos(math.radians(lat_offset))
    delta_lon = distance_east / r
    point_lon = lon_offset + math.degrees(delta_lon)

    return (point_lat, point_lon)


def is_polygon_convex(points):
    """Check if a polygon defined by a list of points is convex."""
    polygon = Polygon(*points)
    return polygon.is_convex()


def distance_between_points(p1, p2):
    """
    Calculate the distance between two points in meters.
    Args:
        p1: A tuple (x, y) representing the first point.
        p2: A tuple (x, y) representing the second point.
    returns:
        Float: The distance between the two points in meters.
    """
    return haversine(p1[0], p1[1], p2[0], p2[1])


def find_slope_intercept(p1, p2):
    """Find the slope and intercept of a line defined by two points."""
    x = [p1[0], p2[0]]
    y = [p1[1], p2[1]]
    slope, intercept = np.polyfit(x, y, 1)
    return slope, intercept


def find_perpendicular_slope_intercept(slope, point):
    """Find the slope and intercept of a line perpendicular to a line defined by a slope and a point."""
    x, y = point
    perpendicular_slope = -1 / slope
    perpendicular_intercept = y - perpendicular_slope * x
    return perpendicular_slope, perpendicular_intercept


def find_intersection(p1, p2, slope, intercept):
    """
    Find the intersection point of a line segment and a line.

    Parameters:
        p1 (tuple): The first point of the line segment (x1, y1).
        p2 (tuple): The second point of the line segment (x2, y2).
        slope (float): The slope of the other line.
        intercept (float): The y-intercept of the other line.

    Returns:
        list: The intersection point [x_intersect, y_intersect] if it exists and lies within the segment, otherwise None.
    """

    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2:
        x_intersect = x1
        y_intersect = slope * x_intersect + intercept
    elif y1 == y2:
        y_intersect = y1
        x_intersect = (y_intersect - intercept) / slope
    else:
        slope_edge = (y2 - y1) / (x2 - x1)
        intercept_edge = y1 - slope_edge * x1
        if slope == slope_edge:
            return None
        x_intersect = (intercept_edge - intercept) / (slope - slope_edge)
        y_intersect = slope * x_intersect + intercept
    if min(x1, x2) <= x_intersect <= max(x1, x2) and min(y1, y2) <= y_intersect <= max(y1, y2):
        return [x_intersect, y_intersect]
    return None


def distance_between_cartesian_points(p1, p2):
    """Calculate the Euclidean distance between two points in Cartesian coordinates."""
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def find_longest_edge(points):
    """Find the longest edge of a quadrilateral."""
    max_length = 0
    longest_edge = None

    for i in range(len(points)):
        p1, p2 = points[i], points[(i + 1) % len(points)]
        length = np.linalg.norm(np.array(p1) - np.array(p2))
        if length > max_length:
            max_length = length
            longest_edge = (p1, p2)

    return max_length, longest_edge


def find_segment_points(edge, N=2):
    """Find N equal segment points on an edge."""
    (x1, y1), (x2, y2) = edge
    segment_points = []
    for i in range(1, N):
        x = x1 + (x2 - x1) * i / N
        y = y1 + (y2 - y1) * i / N
        segment_points.append((x, y))
    return segment_points


def perpendicular_lines_at_points(edge, points=[], N=2, length=1000):
    """
    Generate perpendicular lines at specified points along a given edge.
    Parameters:
        edge (tuple): A tuple containing two points (x1, y1) and (x2, y2) that define the edge.
        points (list, optional): A list of points (x, y) where perpendicular lines should be generated.
                                If not provided, points will be generated along the edge.
        N (int, optional): Number of points to generate along the edge if `points` is not provided. Default is 2.
        length (int, optional): Length of the perpendicular lines to be generated. Default is 1000.
    Returns:
        list: A list of tuples, each containing the slope and intercept of the perpendicular lines.
    """

    (x1, y1), (x2, y2) = edge
    perp_lines = []

    if len(points) == 0:
        points = find_segment_points(edge, N)

    for point in points:
        x, y = point

        if x2 - x1 == 0:  # Vertical edge
            perp_line = LineString([(x - length, y), (x + length, y)])
        elif y2 - y1 == 0:  # Horizontal edge
            perp_line = LineString([(x, y - length), (x, y + length)])
        else:
            slope = (y2 - y1) / (x2 - x1)
            perp_slope = -1 / slope
            perp_line = LineString(
                [(x - length, y - length * perp_slope), (x + length, y + length * perp_slope)]
            )
        perp_lines.append(find_slope_intercept(*perp_line.coords[:]))

    return perp_lines


def find_polygon_line_intersections(cartesian_polygon, line):
    """Find intersections of a line with a polygon."""

    intersection_points = []
    cartesian_coordinates = np.array(cartesian_polygon)
    slope, intercept = line

    for i in range(len(cartesian_coordinates)):
        p1 = cartesian_coordinates[i]
        p2 = cartesian_coordinates[(i + 1) % len(cartesian_coordinates)]
        intersection = find_intersection(p1, p2, slope, intercept)

        if intersection:
            intersection_points.append(intersection)

    return intersection_points


def is_between_lines(point, line1, line2):
    """Check if a point lies between two lines."""
    x, y = point
    slope1, intercept1 = line1
    slope2, intercept2 = line2
    return (
        min(slope1 * x + intercept1, slope2 * x + intercept2)
        <= y
        <= max(slope1 * x + intercept1, slope2 * x + intercept2)
    )


def is_left_of_line(point, line):
    """Check if a point lies to the left of a line."""
    x, y = point
    slope, intercept = line
    return y >= slope * x + intercept


def calculate_angle(a, b, c):
    """Calculate angle at b given points a, b, c, including reflex angles."""
    ba = (a[0] - b[0], a[1] - b[1])
    bc = (c[0] - b[0], c[1] - b[1])

    # Dot product
    dot_prod = ba[0] * bc[0] + ba[1] * bc[1]
    # Magnitude of vector AB and BC
    mag_ab = math.sqrt(ba[0] ** 2 + ba[1] ** 2)
    mag_bc = math.sqrt(bc[0] ** 2 + bc[1] ** 2)

    if mag_ab == 0 or mag_bc == 0:
        # Return an angle of 0 or handle it as needed
        return 0

    cosine_angle = (dot_prod) / (mag_ab * mag_bc)
    angle = math.acos(cosine_angle)
    # Calculate the cross product of vectors ba and bc
    cross_product = ba[0] * bc[1] - ba[1] * bc[0]
    # Convert the angle from radians to degrees
    angle_degrees = math.degrees(angle)
    # If the cross product is negative, the angle is reflex, so we adjust the angle
    if cross_product > 0:
        angle_degrees = 360 - angle_degrees
    return angle_degrees


def heron_formula(a, b, c):
    """Apply Heron's formula to calculate the area of a triangle given its side lengths."""
    s = (a + b + c) / 2
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    return area


def read_points_from_file(filename):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            x_coords = []
            y_coords = []
            for line in lines:
                x, y = map(float, line.strip().split(", "))
                x_coords.append(x)
                y_coords.append(y)
            return x_coords, y_coords
    except FileNotFoundError:
        return None, None


def find_polygon_edges(positions):
    # Convert the list of positions to a NumPy array
    points = np.array(positions)

    # Calculate the convex hull
    hull = ConvexHull(points)

    # Extract the vertices of the convex hull
    hull_vertices = points[hull.vertices]

    # Convert the vertices back to a list of tuples
    edge_points = [tuple(point) for point in hull_vertices]

    # Find the rest of the points that are not on the edges
    rest_points = [point for point in positions if point not in edge_points]

    return edge_points, rest_points


def point_on_line(point_a, point_c, point_b, margin_of_error=0.0000001):
    """
    Check if point_c lies on the line defined by point_a and point_b
    within a specified margin of error.
    """
    # Calculate distances between the points
    dist_ab = haversine(point_a[0], point_a[1], point_b[0], point_b[1])
    dist_ac = haversine(point_a[0], point_a[1], point_c[0], point_c[1])
    dist_bc = haversine(point_b[0], point_b[1], point_c[0], point_c[1])

    # Check if the sum of distances AC and BC is approximately equal to AB
    return math.isclose(dist_ab, dist_ac + dist_bc, rel_tol=margin_of_error)


def check_and_move_points(list_A, list_B):
    """
    Update list A (edges) and list B (rest) by moving points from list B to list A if
    they are determined to be on an edge within a tolerance range.
    """
    updated_list_A = list_A[:]
    updated_list_B = list_B[:]

    for point in list_B:
        for i in range(len(list_A) - 1):
            if point_on_line(list_A[i], point, list_A[i + 1]):
                updated_list_A.append(point)
                updated_list_B.remove(point)
                break  # Move to the next point after finding its place

    return updated_list_A, updated_list_B


def reorder_list(start_point, list1):
    distances = []
    # Calculate the distance from start_point to each point in list1
    for point in list1:
        distance = haversine(start_point[0], start_point[1], point[0], point[1])
        distances.append((point, distance))

    # Find the nearest point and its index
    # TÌM ĐIỂM GẦN NHẤT VỚI DRONE
    nearest_point, _ = min(distances, key=lambda x: x[1])
    nearest_index = list1.index(nearest_point)

    # Reorder the list starting with the nearest point
    reordered_list = list1[int(nearest_index) :] + list1[: int(nearest_index)]

    return reordered_list


def split_at_farthest_point(start_position, reordered_points, list_2):
    # Calculate the distance of each point from the start position
    distances = [
        haversine(start_position[0], start_position[1], point[0], point[1])
        for point in reordered_points
    ]

    # Find the index of the farthest point
    farthest_index = distances.index(max(distances))  # TÌM ĐIỂM XA NHẤT VỚI DRONE

    # Split the reordered list at the farthest point, including the farthest point in the first part
    keep_points = reordered_points[: farthest_index + 1]
    move_to_list_2 = reordered_points[farthest_index + 1 :]
    list_2.extend(move_to_list_2)

    # Duplicate the last point in keep_points
    last_point = keep_points[-1]

    # Put it at the beginning of list_2
    list_2.insert(0, last_point)

    return keep_points, list_2


def find_nearest_to_A(points, point_A):
    # Calculate distances to point A and find the minimum
    distances = [haversine(point[0], point[1], point_A[0], point_A[1]) for point in points]
    min_distance_index = distances.index(min(distances))
    return points[min_distance_index]


def find_shortest_path(start_position, points_list):
    # Calculate the distance from point A to all other points
    distances_to_A = [
        haversine(start_position[0], start_position[1], point[0], point[1])
        for point in points_list
    ]

    # Identify the nearest point to point A (to be the last point)
    nearest_to_A_index = distances_to_A.index(min(distances_to_A))
    # Remove and save the nearest point
    point_nearest_to_A = points_list.pop(nearest_to_A_index)

    # Start with the beginning point, already placed from keep_points
    path = [points_list.pop(0)]

    # Use a modified nearest neighbor algorithm to construct the path
    while points_list:
        last_point = path[-1]
        nearest_index = min(
            range(len(points_list)),
            key=lambda i: haversine(
                last_point[0], last_point[1], points_list[i][0], points_list[i][1]
            ),
        )
        nearest_point = points_list.pop(nearest_index)
        path.append(nearest_point)

    # Append the point nearest to A at the end of the path
    path.append(point_nearest_to_A)

    return path


def sort_polygon_vertices(vertices):
    """Sort polygon vertices by angle from centroid (counter-clockwise)."""
    # Calculate centroid of the polygon
    centroid_x = sum(x for x, y in vertices) / len(vertices)
    centroid_y = sum(y for x, y in vertices) / len(vertices)

    # Define a function to calculate the angle between centroid and vertex
    def angle_from_centroid(vertex):
        return math.atan2(vertex[1] - centroid_y, vertex[0] - centroid_x)

    # Sort vertices by the angle from centroid
    return sorted(vertices, key=angle_from_centroid, reverse=True)


def find_path(points, point_A):
    """
    Find an optimized path through the given points starting from point_A.
    
    This function creates a path that:
    1. Finds polygon edges using convex hull
    2. Identifies points on the edges
    3. Sorts edge points starting from nearest to point_A
    4. Splits into two parts at the farthest point
    5. Creates a zig-zag path for interior points
    
    Args:
        points: List of coordinate tuples
        point_A: Starting point coordinates
        
    Returns:
        Optimized path as list of coordinates
    """
    # Find polygon edges using convex hull
    list_edges, list_interior = find_polygon_edges(points)

    # Identify points lying on polygon edges
    list_edges, list_interior = check_and_move_points(list_edges, list_interior)

    # Sort edge points in order around the polygon
    list_edges = sort_polygon_vertices(list_edges)

    # Reorder starting from point nearest to point_A
    list_edges = reorder_list(point_A, list_edges)

    # Split path at farthest point from point_A
    list_edges, list_interior = split_at_farthest_point(point_A, list_edges, list_interior)

    # Find shortest zig-zag path through interior points
    path_interior = find_shortest_path(point_A, list_interior.copy())

    # Combine edge path and interior path
    list_edges.pop()  # Remove duplicate point
    list_edges.extend(path_interior)

    return list_edges
