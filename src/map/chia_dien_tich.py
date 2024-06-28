import math
import sys
import copy
from scipy.spatial import ConvexHull
import numpy as np

#-------------CHIA LUOI------------

def ray_casting_point_in_polygon(point, polygon):
    """
    Determine if a point is inside a polygon using the Ray Casting method in a Cartesian coordinate system.

    :param point: A tuple (x, y) representing the point to check.
    :param polygon: A list of tuples [(x, y), ...] representing the polygon vertices.
    :return: True if the point is inside the polygon; False otherwise.
    """
    x, y = point
    inside = False

    n = len(polygon)
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

def generate_grid(vertices, spacing_m):
    """
    Generate grid points within the polygon defined by `vertices` in a Cartesian coordinate system,
    where the vertices are specified in meters.

    :param vertices: List of (x, y) tuples for the vertices of the polygon.
    :param spacing_m: Distance between points in the grid, in meters.
    :return: List of (x, y) tuples for the grid points inside the polygon.
    """
    min_x = min(v[0] for v in vertices)
    max_x = max(v[0] for v in vertices)
    min_y = min(v[1] for v in vertices)
    max_y = max(v[1] for v in vertices)

    points = []
    for i in range(int((max_y - min_y) / spacing_m) + 1):
        for j in range(int((max_x - min_x) / spacing_m) + 1):
            x = min_x + (j * spacing_m)
            y = min_y + (i * spacing_m)
            if ray_casting_point_in_polygon((x, y), vertices):
                points.append((x, y))

    return points

# def ray_casting_point_in_polygon(point, polygon, tolerance=1e-4):
#     """
#     Determine if a point is inside a polygon using the Ray Casting method with tolerance for comparisons.

#     :param point: A tuple (x, y) representing the point to check.
#     :param polygon: A list of tuples [(x, y), ...] representing the polygon vertices.
#     :param tolerance: Numerical tolerance for floating-point comparisons.
#     :return: True if the point is inside the polygon; False otherwise.
#     """
#     x, y = point
#     inside = False
#     n = len(polygon)
#     p1x, p1y = polygon[0]

#     for i in range(1, n + 1):
#         p2x, p2y = polygon[i % n]
#         if p1y == p2y and abs(y - p1y) <= tolerance:
#             # The point is on a horizontal line of the polygon.
#             if min(p1x, p2x) - tolerance <= x <= max(p1x, p2x) + tolerance:
#                 return True
#         elif (p1y < y + tolerance and p2y >= y - tolerance) or (p1y >= y - tolerance and p2y < y + tolerance):
#             # The ray crosses through the edge of the polygon.
#             xints = p2x if p1y == p2y else (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
#             if abs(x - xints) <= tolerance or x < xints:
#                 inside = not inside
#         p1x, p1y = p2x, p2y

#     return inside

# def generate_grid(vertices, spacing, tolerance=1e-6):
#     """
#     Generate grid points within the polygon defined by `vertices` in a Cartesian coordinate system
#     accounting for negative values and a tolerance in comparisons.

#     :param vertices: List of (x, y) tuples for the vertices of the polygon.
#     :param spacing: Distance between points in the grid, in the same units as the polygon coordinates.
#     :param tolerance: Numerical tolerance for floating-point comparisons.
#     :return: List of (x, y) tuples for the grid points inside the polygon.
#     """
#     min_x = min(v[0] for v in vertices)
#     max_x = max(v[0] for v in vertices)
#     min_y = min(v[1] for v in vertices)
#     max_y = max(v[1] for v in vertices)

#     points = []
#     y = min_y
#     while y <= max_y + tolerance:  # Include upper boundary within tolerance
#         x = min_x
#         while x <= max_x + tolerance:  # Include right boundary within tolerance
#             if ray_casting_point_in_polygon((x, y), vertices, tolerance):
#                 points.append((x, y))
#             x += spacing
#         y += spacing

#     return points


#-------------CHIA DIEN TICH------------
def does_line_intersect_polygon(mid, slope, intercept, vertices, tolerance=1e-6):
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]

        # Check for vertical edge (x1 == x2)
        if x1 == x2:
            if slope is None:  # The line is also vertical, check if they are the same line
                if abs(x1 - mid[0]) <= tolerance:  # The line coincides with the edge
                    continue
                else:  # Parallel lines, no intersection
                    return None
            else:
                intersect_x = x1
                intersect_y = slope * intersect_x + intercept
                if min(y1, y2) <= intersect_y <= max(y1, y2) and \
                   abs(intersect_x - mid[0]) > tolerance and abs(intersect_y - mid[1]) > tolerance:
                    return intersect_x, intersect_y
        
        else:  # Non-vertical edge
            edge_slope = (y2 - y1) / (x2 - x1)
            edge_intercept = y1 - edge_slope * x1
            
            if slope is None:  # The line is vertical, use its x-intercept (which is actually the x coordinate)
                intersect_x = intercept
                intersect_y = edge_slope * intersect_x + edge_intercept
                if min(x1, x2) <= intersect_x <= max(x1, x2) and \
                   abs(intersect_y - mid[1]) > tolerance:
                    return intersect_x, intersect_y

            elif slope != edge_slope:  # The line is not vertical and not parallel to the edge
                intersect_x = (edge_intercept - intercept) / (slope - edge_slope)
                intersect_y = slope * intersect_x + intercept

                if min(x1, x2) <= intersect_x <= max(x1, x2) and min(y1, y2) <= intersect_y <= max(y1, y2) and \
                   (abs(intersect_x - mid[0]) > tolerance or abs(intersect_y - mid[1]) > tolerance):
                    return intersect_x, intersect_y
    return None



def haversine(lat1, lon1, lat2, lon2):
    R = 6378000  # Earth's radius in meters
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
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

def calculate_polygon_edges(positions):
    """
    Calculate all the edges of a polygon and return their lengths.
    
    :param positions: A list of tuples [(lat, lon), ...] representing the polygon vertices.
    :return: A list of distances for each edge of the polygon.
    """
    num_vertices = len(positions)
    distances = []
    
    # Iterate through each vertex and calculate distance to the next vertex
    for i in range(num_vertices):
        # Get current vertex and the next vertex, wrapping around to the first vertex
        lat1, lon1 = positions[i]
        lat2, lon2 = positions[(i + 1) % num_vertices]  # Wrap around using modulo
        
        # Calculate the distance between the vertices
        distance = haversine(lat1, lon1, lat2, lon2)
        distances.append(distance)
    
    return distances

def calculate_edge_lengths(cartesian_coords):
    """
    Calculate the lengths of edges in a polygon given its vertices in Cartesian coordinates.
    
    :param cartesian_coords: A list of tuples (x, y) representing the Cartesian coordinates of the polygon vertices.
    :return: A list of lengths of each edge in the polygon.
    """
    num_vertices = len(cartesian_coords)
    edge_lengths = []
    
    for i in range(num_vertices):
        # Current vertex
        x1, y1 = cartesian_coords[i]
        # Next vertex, with wrap-around using modulo to close the polygon
        x2, y2 = cartesian_coords[(i + 1) % num_vertices]
        
        # Calculate the distance between the current vertex and the next vertex
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        edge_lengths.append(distance)
    
    return edge_lengths

def calculate_polygon_area(cartesian_coords):
    """
    Calculate the area of a polygon given its vertices in Cartesian coordinates using the Shoelace theorem.
    
    :param cartesian_coords: A list of tuples (x, y) representing the Cartesian coordinates of the polygon vertices.
    :return: The area of the polygon in square meters.
    """
    n = len(cartesian_coords)  # Number of vertices
    area = 0

    # Sum over the vertices
    for i in range(n):
        j = (i + 1) % n  # Next vertex index, wraps around
        x_i, y_i = cartesian_coords[i]
        x_j, y_j = cartesian_coords[j]
        area += x_i * y_j - y_i * x_j

    area = abs(area) / 2.0
    return area

def find_longest_edge(cartesian_coords):
    """
    Find the vertices that form the longest edge in a polygon given its vertices in Cartesian coordinates.
    
    :param cartesian_coords: A list of tuples (x, y) representing the Cartesian coordinates of the polygon vertices.
    :return: A tuple containing:
        - the length of the longest edge,
        - the coordinates of the start vertex of the longest edge,
        - the coordinates of the end vertex of the longest edge.
    """
    num_vertices = len(cartesian_coords)
    longest_edge_length = 0
    longest_edge_vertices = (None, None)
    
    for i in range(num_vertices):
        # Current vertex
        x1, y1 = cartesian_coords[i]
        # Next vertex, with wrap-around using modulo to close the polygon
        x2, y2 = cartesian_coords[(i + 1) % num_vertices]
        
        # Calculate the distance between the current vertex and the next vertex
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        # Check if this is the longest edge found so far
        if distance > longest_edge_length:
            longest_edge_length = distance
            longest_edge_vertices = ((x1, y1), (x2, y2))
    
    return longest_edge_length, longest_edge_vertices

def find_midpoint(point1, point2):
    # Extract coordinates from the points
    x1, y1 = point1
    x2, y2 = point2
    
    # Calculate the midpoint coordinates
    mid_x = (x1 + x2) / 2.0
    mid_y = (y1 + y2) / 2.0
    
    return (mid_x, mid_y)

def line_equation_from_points(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    
    # Check for vertical line
    if x1 == x2:
        # The line is vertical, slope is undefined, and the line equation is x = x1
        return None, x1

    # Check for horizontal line
    elif y1 == y2:
        # The line is horizontal, slope is 0, and the line equation is y = y1
        return 0, y1

    else:
        # For non-vertical and non-horizontal lines, calculate slope and intercept
        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1
        return slope, intercept

def angle_with_x_axis(slope):
    if slope is None:  # Vertical line
        angle_degrees = 90
    else:
        angle_radians = math.atan(slope)
        angle_degrees = math.degrees(angle_radians)

    return angle_degrees

def perpendicular_line_equation(midpoint, slope, tolerance=1e-6):
    """
    Calculate the slope and y-intercept of the line perpendicular to the line with the given slope,
    passing through the given midpoint.

    :param midpoint: A tuple (x, y) representing the midpoint through which the perpendicular line passes.
    :param slope: The slope of the original line. Can be a number, zero, or None for vertical lines.
    :param tolerance: The tolerance range for slope comparisons to account for floating-point inaccuracies.
    :return: A tuple (perpendicular slope, y-intercept) representing the perpendicular line.
             Returns (None, y-coordinate of midpoint) for vertical lines and
             (0, x-coordinate of midpoint) for horizontal lines.
    """
    mx, my = midpoint

    # Check if the original slope is near zero (horizontal line)
    if slope is not None:
        if -tolerance < slope < tolerance:
            # The perpendicular line would be vertical
            return None, my

    # Check if the original slope is undefined (vertical line)
    elif slope is None:
        # The perpendicular line would be horizontal
        return 0, my

    # Otherwise, calculate the perpendicular slope and intercept
    perp_slope = -1 / slope
    perp_intercept = my - perp_slope * mx
    return perp_slope, perp_intercept

    
def calculate_new_lat_lon(origin_lat, origin_lon, distance_north, distance_east):
    """ Calculate new latitude and longitude from origin given distances north and east. """
    R = 6378000  # Radius of Earth in meters
    delta_lat = distance_north / R  # Change in latitude in radians
    new_lat = origin_lat + math.degrees(delta_lat)  # New latitude in degrees

    # Adjust for change in longitude, which depends on latitude
    r = R * math.cos(math.radians(new_lat))  # Effective radius at new latitude
    delta_lon = distance_east / r  # Change in longitude in radians
    new_lon = origin_lon + math.degrees(delta_lon)  # New longitude in degrees

    return (new_lat, new_lon)

    
def divide_line_into_segments(x1, y1, x2, y2, n):
    points = []
    for i in range(1, n):  # We skip 0 and n because they correspond to the endpoints.
        t = i / n
        xt = (1 - t) * x1 + t * x2
        yt = (1 - t) * y1 + t * y2
        points.append((xt, yt))

    return points

def perpendicular_line_intersect_polygon(slope, intercept, vertices):
    across_points = []
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]

        # Check if the edge is vertical
        if x1 == x2:
            if slope is None:
                # Both the line and edge are vertical, so check if they are the same line
                if x1 == intercept:  # Using intercept as x since the line is vertical
                    # Overlapping vertical lines intersect at any point along their span
                    overlap_range = [max(min(y1, y2), intercept), min(max(y1, y2), intercept)]
                    if overlap_range[0] != overlap_range[1]:
                        # Return a representative point from the overlapping segment
                        point = (x1, sum(overlap_range) / 2)
                        across_points.append(point)
            else:
                # The edge is vertical while the line is not, calculate y using line's equation
                intersect_y = slope * x1 + intercept
                if min(y1, y2) <= intersect_y <= max(y1, y2):
                    point = (x1, intersect_y)
                    across_points.append(point)
        
        # Check if the edge is non-vertical
        elif x2 != x1:
            m_e = (y2 - y1) / (x2 - x1)
            b_e = y1 - m_e * x1
            if slope is None:
                # The line is vertical, calculate x using edge's equation
                intersect_x = intercept  # Using intercept as x since the line is vertical
                intersect_y = m_e * intercept + b_e
                if min(x1, x2) <= intersect_x <= max(x1, x2):
                    point = (intersect_x, intersect_y)
                    across_points.append(point)
            elif slope != m_e:
                # Ensure the lines are not parallel and calculate the intersection
                intersect_x = (b_e - intercept) / (slope - m_e)
                intersect_y = slope * intersect_x + intercept
                if min(x1, x2) <= intersect_x <= max(x1, x2) and min(y1, y2) <= intersect_y <= max(y1, y2):
                    point = (intersect_x, intersect_y)
                    across_points.append(point)

    return across_points



def divide_points(per_points, polygon, slope1, edge_slope):
    each_point = []
    for point in per_points:
        perp_slope, perp_intercept = perpendicular_line_equation(point, slope1)
        per_dot = perpendicular_line_intersect_polygon(perp_slope, perp_intercept,polygon)

        each_point.extend(per_dot)

    return each_point

def rotate_and_shift_point(x, y, angle, pivot_x, pivot_y, shift_x=0, shift_y=0, units="DEGREES", clockwise=False):
    """
    Rotates a point around a pivot point either clockwise or counterclockwise and then applies a shift.

    :param x: The x-coordinate of the point to be rotated.
    :param y: The y-coordinate of the point to be rotated.
    :param angle: The angle of rotation. Positive angles will result in counterclockwise rotation, 
                  and negative angles will result in clockwise rotation if `clockwise` is set to True.
    :param pivot_x: The x-coordinate of the pivot point.
    :param pivot_y: The y-coordinate of the pivot point.
    :param shift_x: The distance to shift along the x-axis after rotation.
    :param shift_y: The distance to shift along the y-axis after rotation.
    :param units: The units of the angle: 'DEGREES' (default) or 'RADIANS'.
    :param clockwise: If True, the rotation will be clockwise, otherwise counterclockwise.
    :return: A tuple containing the rotated and shifted x and y coordinates.
    """

    # Convert angle from degrees to radians if specified in degrees
    if units.upper() == "DEGREES":
        angle = math.radians(angle)

    # If clockwise rotation is desired, negate the angle
    if clockwise:
        angle = -angle

    # Translate point to pivot
    x -= pivot_x
    y -= pivot_y

    # Apply rotation
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)
    x_rotated = (x * cos_theta) - (y * sin_theta)
    y_rotated = (x * sin_theta) + (y * cos_theta)

    # Translate point back from pivot and apply additional shift
    x_final = x_rotated + pivot_x + shift_x
    y_final = y_rotated + pivot_y + shift_y

    return x_final, y_final

def revert_rotate_and_shift_point(x, y, angle, pivot_x, pivot_y, shift_x=0, shift_y=0, units="DEGREES", clockwise=False):
    """
    Reverts the rotation and shift applied to a point. First subtracts the shift, then rotates the point back.

    :param x: The x-coordinate of the point that was rotated and shifted.
    :param y: The y-coordinate of the point that was rotated and shifted.
    :param angle: The original angle of rotation used to rotate the point. 
    :param pivot_x: The x-coordinate of the pivot point used in the original rotation.
    :param pivot_y: The y-coordinate of the pivot point used in the original rotation.
    :param shift_x: The x-distance of the shift to revert.
    :param shift_y: The y-distance of the shift to revert.
    :param units: The units of the angle: 'DEGREES' (default) or 'RADIANS'.
    :param clockwise: If the original rotation was clockwise, set True; otherwise, set False.
    :return: A tuple containing the x and y coordinates of the point after reverting the rotation and shift.
    """

    # Subtract the shift
    x -= shift_x
    y -= shift_y

    # Convert angle from degrees to radians if specified in degrees
    if units.upper() == "DEGREES":
        angle = math.radians(angle)

    # Reverse the angle direction for the rotation back
    if not clockwise:
        angle = -angle

    # Translate point to pivot
    x -= pivot_x
    y -= pivot_y

    # Apply rotation in the opposite direction
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)
    x_reverted = (x * cos_theta) + (y * sin_theta)
    y_reverted = (-x * sin_theta) + (y * cos_theta)

    # Translate point back from pivot
    x_final = x_reverted + pivot_x
    y_final = y_reverted + pivot_y

    return x_final, y_final



def split_area(area, perp, tolerance=1e-6):
    area_list = []

    # Helper function to check if y is approximately less than or equal to perp_y
    def y_leq_with_tolerance(y, perp_y):
        return abs(y) <= abs(perp_y) + tolerance

    # Helper function to check if y is approximately greater than or equal to perp_y
    def y_geq_with_tolerance(y, perp_y):
        return abs(y) >= abs(perp_y) - tolerance

    # Case when only one perpendicular point is provided
    if len(perp) == 1:
        below_or_equal, above_or_equal = [], []
        perp_y = perp[0][1]

        for point in area:
            if y_leq_with_tolerance(point[1], perp_y):
                below_or_equal.append(point)
            if y_geq_with_tolerance(point[1], perp_y):
                above_or_equal.append(point)

        area_list.append(below_or_equal)
        area_list.append(above_or_equal)

    # Case when more than one perpendicular point is provided
    else:
        for i, perp_point in enumerate(perp):
            one_area = []
            perp_y = perp_point[1]

            if i == 0:
                for point in area:
                    if y_leq_with_tolerance(point[1], perp_y):
                        one_area.append(point)

            elif i == len(perp) - 1:
                previous_perp_y = perp[i - 1][1]
                for point in area:
                    if y_geq_with_tolerance(point[1], previous_perp_y) and y_leq_with_tolerance(point[1], perp_y):
                        one_area.append(point)
                area_list.append(one_area)
                one_area = []
                for point in area:
                    if y_geq_with_tolerance(point[1], perp_y):
                        one_area.append(point)

            else:
                previous_perp_y = perp[i - 1][1]
                for point in area:
                    if y_geq_with_tolerance(point[1], previous_perp_y) and y_leq_with_tolerance(point[1], perp_y):
                        one_area.append(point)

            area_list.append(one_area)

    return area_list


            
def chia_dien_tich(positions, number_of_part):
    global angle
    global min_lat
    global min_lon
    global midpoint
    min_lat = min(positions, key=lambda x: x[0])[0]
    min_lon = min(positions, key=lambda x: x[1])[1]
    # Convert the geographic positions to Cartesian coordinates
    cartesian_coordinates = convert_to_cartesian(positions)
    print("Cartesian Coordinates:")
    for coord in cartesian_coordinates:
        print(coord)
    
    #Find the largest edge
    longest, longest_edge_point = find_longest_edge(cartesian_coordinates)
    print(f"\nEdge: {longest}")
    for coord in longest_edge_point:
        print(coord)
    
    #Find midpont of largest edge
    midpoint = find_midpoint(longest_edge_point[0], longest_edge_point[1])
    print(f"\nMidpoint: {midpoint}")
    new = calculate_new_lat_lon(min_lat,min_lon,midpoint[1],midpoint[0])
    print(f"\nGPS Midpoint: {new}")


    

    #Find line equation of largest edge (to figure out the slope of it) 
    slope, intercept = line_equation_from_points(longest_edge_point[0], longest_edge_point[1])
    print(f"\nSlope: {slope}")
    angle = angle_with_x_axis(slope)
    print(f"\nAngle: {angle}")

    new_point = rotate_and_shift_point(midpoint[0], midpoint[1],(-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1]))
    print(f"ROTATED MIDPOINT{new_point}")

    #Find the perpendicular's line equation (perpendicular of largest edge)
    perp_slope, perp_intercept = perpendicular_line_equation(midpoint, slope)
    print(f"\nPerp_slope: {perp_slope},Perp_intercep: {perp_intercept}")

    #Find the other intersection of the perpendicular with the polygon
    intersect_point = does_line_intersect_polygon(midpoint, perp_slope, perp_intercept,cartesian_coordinates)
    print(f"\nIntersect: {intersect_point[0]},{intersect_point[1]}")
    new = calculate_new_lat_lon(min_lat,min_lon,intersect_point[1],intersect_point[0])
    print(f"\nGPS Intersect: {new}")

    #---------------------------------

    #---------------------------------
    #Divide the perpendicular into equal parts
    perpendicular_points = divide_line_into_segments(midpoint[0], midpoint[1], intersect_point[0], intersect_point[1],number_of_part)

    per_GPS_list = []
    for point in perpendicular_points:
        new = calculate_new_lat_lon(min_lat,min_lon,point[1],point[0])
        per_GPS_list.append(new)
        print(f"{point}")
    with open('per.txt', 'w') as file:
        for pos in per_GPS_list:
            file.write(f"{pos[0]}, {pos[1]}\n")

    #Find the divide point on the polygon edge
    div_GPS_list=[]
    div_points = divide_points(perpendicular_points, cartesian_coordinates, perp_slope, slope)
    for point in div_points:
        new = calculate_new_lat_lon(min_lat,min_lon,point[1],point[0])
        div_GPS_list.append(new)
        print(f"{new}")
        
    with open('div.txt', 'w') as file:
        for pos in div_GPS_list:
            file.write(f"{pos[0]}, {pos[1]}\n")

    #Rotate and shift the coordinate 
    rotated_div_points = []
    print(f"DIV_ROTATED")
    for point in div_points:
        new_point = rotate_and_shift_point(point[0], point[1],(-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1]))
        rotated_div_points.append(new_point)
        print(f"{new_point}")
    
    rotated_perpendicular_points = []
    print(f"PERP_ROTATED")
    for point in perpendicular_points:
        new_point = rotate_and_shift_point(point[0], point[1],(-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1]))
        rotated_perpendicular_points.append(new_point)
        print(f"{new_point}")
    
    print(f"PERP_UNROTATED")
    for point in perpendicular_points:
        print(f"{point}")

    print(f"POLYGON_ROTATED")
    rotated_cartesian_coordinates = []
    for point in cartesian_coordinates:
        new_point = rotate_and_shift_point(point[0], point[1],(-angle), midpoint[0],midpoint[1], (-midpoint[0]), (-midpoint[1]))
        rotated_cartesian_coordinates.append(new_point)
        print(f"{new_point}")
    print(f"POLYGON_UNROTATED")
    for point in cartesian_coordinates:
        print(f"{point}")

    rotate_polygon = []
    #Points lie on polygon egde = vertices + divide points
    rotate_polygon = rotated_div_points + rotated_cartesian_coordinates

    #Separate the point into different parts
    rotated_area = split_area(rotate_polygon,rotated_perpendicular_points)
    final_area =[]

    print(f"POLYGON_UNROTATED_BACK")
    for point in rotated_cartesian_coordinates:
        #convert back in previous coordinate
        new_point = revert_rotate_and_shift_point(point[0], point[1],(-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1]), clockwise = True)
        print(f"{new_point}")

    for i in range(len(rotated_area)):
        area = rotated_area[i]
        unrotated_area =[]
        print(f"{area}")
        for point in area:
            #convert back in previous coordinate
            new_point = revert_rotate_and_shift_point(point[0], point[1],(-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1]), clockwise = True)
            unrotated_area.append(new_point)
        per_GPS_list = []
        for point in unrotated_area:
            new = calculate_new_lat_lon(min_lat,min_lon,point[1],point[0])
            per_GPS_list.append(new)
            print(f"{new}")
        # Convert the list of positions to a NumPy array
        
        points = np.array(per_GPS_list)
        
        # Calculate the convex hull
        hull = ConvexHull(points)
        
        # Extract the vertices of the convex hull
        hull_vertices = points[hull.vertices]
        
        # Convert the vertices back to a list of tuples
        points = [tuple(point) for point in hull_vertices]
        final_area.append(points)
        with open(f'area{i+1}.txt', 'w') as file:
            for pos in points:
                file.write(f"{pos[0]}, {pos[1]}\n")
      
    

    print(f"FINAL AREA")
    for i in range(len(final_area)):
            print(f"{i}")
            print(f"{final_area[i]}")
 
    return final_area, rotated_area
    
def chia_luoi(rotated_area,distance):
    print(f"rotated")
    print(f"{rotated_area}")
    areas_dot = []
    for i,area in enumerate(rotated_area):

        points = np.array(area)
        
        # Calculate the convex hull
        hull = ConvexHull(points)
        
        # Extract the vertices of the convex hull
        hull_vertices = points[hull.vertices]
        
        # Convert the vertices back to a list of tuples
        points = [tuple(point) for point in hull_vertices]

        grid_points = generate_grid(points,float(distance))

        areas_dot.append(grid_points)

    print(f"areas")
    print(f"{areas_dot}")

    grid_GPS =[]
    for i,area in enumerate(areas_dot):
        area = areas_dot[i]
        unrotated_area = []
        for point in area:
            #convert back in previous coordinate
            new_point = revert_rotate_and_shift_point(point[0], point[1],(-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1]), clockwise = True)
            unrotated_area.append(new_point)
        per_GPS_list = []
        for point in unrotated_area:
            new = calculate_new_lat_lon(min_lat,min_lon,point[1],point[0])
            per_GPS_list.append(new)
        grid_GPS.append(per_GPS_list)
    print(f"GPS")
    print(f"{grid_GPS}")

    return grid_GPS

def chia_luoi_one(area,distance):

    min_lat = min(area, key=lambda x: x[0])[0]
    min_lon = min(area, key=lambda x: x[1])[1]
    # Convert the geographic positions to Cartesian coordinates
    cartesian_coordinates = convert_to_cartesian(area)
    print("Cartesian Coordinates:")
    for coord in cartesian_coordinates:
        print(coord)

    #Find the largest edge
    longest, longest_edge_point = find_longest_edge(cartesian_coordinates)
    print(f"\nEdge: {longest}")
    for coord in longest_edge_point:
        print(coord)
    
    #Find midpont of largest edge
    midpoint = find_midpoint(longest_edge_point[0], longest_edge_point[1])
    print(f"\nMidpoint: {midpoint}")
    new = calculate_new_lat_lon(min_lat,min_lon,midpoint[1],midpoint[0])
    print(f"\nGPS Midpoint: {new}")


    

    #Find line equation of largest edge (to figure out the slope of it) 
    slope, intercept = line_equation_from_points(longest_edge_point[0], longest_edge_point[1])
    print(f"\nSlope: {slope}")
    angle = angle_with_x_axis(slope)
    print(f"\nAngle: {angle}")

    rotated = []
    for point in cartesian_coordinates:
        new_point = rotate_and_shift_point(point[0], point[1],(-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1]))
        rotated.append(new_point)
        print(f"{new_point}")

    points = np.array(rotated)
    
    # Calculate the convex hull
    hull = ConvexHull(points)
    
    # Extract the vertices of the convex hull
    hull_vertices = points[hull.vertices]
    
    # Convert the vertices back to a list of tuples
    points = [tuple(point) for point in hull_vertices]

    grid_points = generate_grid(points,int(distance))




 
    unrotated_area = []
    for point in grid_points:
        #convert back in previous coordinate
        new_point = revert_rotate_and_shift_point(point[0], point[1],(-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1]), clockwise = True)
        unrotated_area.append(new_point)
    per_GPS_list = []
    for point in unrotated_area:
        new = calculate_new_lat_lon(min_lat,min_lon,point[1],point[0])
        per_GPS_list.append(new)


    return per_GPS_list