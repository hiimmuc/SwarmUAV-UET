import math


def haversine(lat1, lon1, lat2, lon2):
    R = 6378000  # bán kính Trái Đất (đơn vị: m)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


def calculate_angle(a, b, c):
    """Calculate angle at b given points a, b, c, including reflex angles."""
    ba = (a[0] - b[0], a[1] - b[1])
    bc = (c[0] - b[0], c[1] - b[1])

    # Dot product
    dot_prod = ba[0] * bc[0] + ba[1] * bc[1]
    # Magnitude of vector AB and BC
    mag_ab = math.sqrt(ba[0]**2 + ba[1]**2)
    mag_bc = math.sqrt(bc[0]**2 + bc[1]**2)

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

# -----------------TÍNH DIỆN TÍCH------------------------------------------------------------


def heron_formula(a, b, c):
    """Apply Heron's formula to calculate the area of a triangle given its side lengths."""
    s = (a + b + c) / 2
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    return area


def angle_list(position_list):
    angles = []
    N = len(position_list)
    for i in range(len(position_list)):
        if i == 0:
            a = position_list[N - 1]  # Previous vertex
            b = position_list[i]      # Current vertex
            # Next vertex, using modulo for circular indexing
            c = position_list[(i + 1) % len(position_list)]
            print(f"a= {a} b= {b} c= {c}")
        elif i == (len(position_list) - 1):
            a = position_list[i - 1]  # Previous vertex
            b = position_list[i]      # Current vertex
            c = position_list[0]
            print(f"a= {a} b= {b} c= {c}")
        else:
            a = position_list[i - 1]  # Previous vertex
            b = position_list[i]      # Current vertex
            # Next vertex, using modulo for circular indexing
            c = position_list[(i + 1) % len(position_list)]

        angle = calculate_angle(a, b, c)
        angles.append(angle)

    for index, goc in enumerate(angles):
        print(f"Angle {index + 1} is: {goc}")


def find_biggest_angle(points):
    """Find the biggest angle in the polygon made up of positions, correctly identifying reflex angles."""
    angles = []
    N = len(points)
    for i in range(len(points)):
        if i == 0:
            a = points[N - 1]  # Previous vertex
            b = points[i]      # Current vertex
            # Next vertex, using modulo for circular indexing
            c = points[(i + 1) % len(points)]
            print(f"a= {a} b= {b} c= {c}")
        elif i == (len(points) - 1):
            a = points[i - 1]  # Previous vertex
            b = points[i]      # Current vertex
            c = points[0]
            print(f"a= {a} b= {b} c= {c}")
        else:
            a = points[i - 1]  # Previous vertex
            b = points[i]      # Current vertex
            # Next vertex, using modulo for circular indexing
            c = points[(i + 1) % len(points)]

        angle = calculate_angle(a, b, c)
        angles.append(angle)

    return angles


def calculate_polygon_area(sides, angles, points):
    angles = find_biggest_angle(points)  # Tính các góc của đa giác
    # Find the index of the largest angle
    index_of_largest_angle = angles.index(
        max(angles))  # tìm ra góc lớn nhất
    print(f"index_of_largest_angle is: {index_of_largest_angle}")

    # Calculate areas of triangles formed with the vertex of the largest angle
    total_area = 0
    n = len(sides)
    for i in range(n):
        if i != index_of_largest_angle and (i + 1) % n != index_of_largest_angle:
            distances = []
            # Calculate the sides of the triangle
            a = points[index_of_largest_angle]
            b = points[i]
            c = points[(i + 1) % n]
            print(f"a= {a} b= {b} c= {c}")
            canh = [a, b, c]
            for i in range(len(canh)):
                for j in range(i + 1, len(canh)):
                    distance = haversine(
                        canh[i][0], canh[i][1], canh[j][0], canh[j][1])
                    distances.append(distance)
                    print(
                        f"Distance between point {i+1} and point {j+1} is: {distance}")

            # Calculate area using Heron's formula
            area = heron_formula(distances[0], distances[1], distances[2])
            print(f"Triangle {i} is: {area}")
            total_area += area

    return total_area


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
        # Wrap around using modulo
        lat2, lon2 = positions[(i + 1) % num_vertices]

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
    # We skip 0 and n because they correspond to the endpoints.
    for i in range(1, n):
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
                    overlap_range = [max(min(y1, y2), intercept), min(
                        max(y1, y2), intercept)]
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
        per_dot = perpendicular_line_intersect_polygon(
            perp_slope, perp_intercept, polygon)

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
