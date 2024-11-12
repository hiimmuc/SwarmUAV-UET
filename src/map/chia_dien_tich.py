import math
import sys
import copy
from scipy.spatial import ConvexHull
import numpy as np
from .calculation_helpers import *
from pathlib import Path

parent_dir = Path(__file__).parent.parent

# -------------CHIA LUOI------------


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


# -------------CHIA DIEN TICH------------
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

            # The line is vertical, use its x-intercept (which is actually the x coordinate)
            if slope is None:
                intersect_x = intercept
                intersect_y = edge_slope * intersect_x + edge_intercept
                if min(x1, x2) <= intersect_x <= max(x1, x2) and \
                   abs(intersect_y - mid[1]) > tolerance:
                    return intersect_x, intersect_y

            elif slope != edge_slope:  # The line is not vertical and not parallel to the edge
                intersect_x = (edge_intercept - intercept) / \
                    (slope - edge_slope)
                intersect_y = slope * intersect_x + intercept

                if min(x1, x2) <= intersect_x <= max(x1, x2) and min(y1, y2) <= intersect_y <= max(y1, y2) and \
                   (abs(intersect_x - mid[0]) > tolerance or abs(intersect_y - mid[1]) > tolerance):
                    return intersect_x, intersect_y
    return None


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

    # Find the largest edge
    longest, longest_edge_point = find_longest_edge(cartesian_coordinates)
    print(f"\nEdge: {longest}")
    for coord in longest_edge_point:
        print(coord)

    # Find midpont of largest edge
    midpoint = find_midpoint(longest_edge_point[0], longest_edge_point[1])
    print(f"\nMidpoint: {midpoint}")
    new = calculate_new_lat_lon(min_lat, min_lon, midpoint[1], midpoint[0])
    print(f"\nGPS Midpoint: {new}")

    # Find line equation of largest edge (to figure out the slope of it)
    slope, intercept = line_equation_from_points(
        longest_edge_point[0], longest_edge_point[1])
    print(f"\nSlope: {slope}")
    angle = angle_with_x_axis(slope)
    print(f"\nAngle: {angle}")

    new_point = rotate_and_shift_point(
        midpoint[0], midpoint[1], (-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1]))
    print(f"ROTATED MIDPOINT{new_point}")

    # Find the perpendicular's line equation (perpendicular of largest edge)
    perp_slope, perp_intercept = perpendicular_line_equation(midpoint, slope)
    print(f"\nPerp_slope: {perp_slope},Perp_intercep: {perp_intercept}")

    # Find the other intersection of the perpendicular with the polygon
    intersect_point = does_line_intersect_polygon(
        midpoint, perp_slope, perp_intercept, cartesian_coordinates)
    print(f"\nIntersect: {intersect_point[0]},{intersect_point[1]}")
    new = calculate_new_lat_lon(
        min_lat, min_lon, intersect_point[1], intersect_point[0])
    print(f"\nGPS Intersect: {new}")

    # ---------------------------------

    # ---------------------------------
    # Divide the perpendicular into equal parts
    perpendicular_points = divide_line_into_segments(
        midpoint[0], midpoint[1], intersect_point[0], intersect_point[1], number_of_part)

    per_GPS_list = []
    for point in perpendicular_points:
        new = calculate_new_lat_lon(min_lat, min_lon, point[1], point[0])
        per_GPS_list.append(new)
        print(f"{point}")
    p_filename = f"{parent_dir}/data/per.txt"  # Set the filename
    with open(p_filename, 'w') as file:
        for pos in per_GPS_list:
            file.write(f"{pos[0]}, {pos[1]}\n")

    # Find the divide point on the polygon edge
    div_GPS_list = []
    div_points = divide_points(
        perpendicular_points, cartesian_coordinates, perp_slope, slope)
    for point in div_points:
        new = calculate_new_lat_lon(min_lat, min_lon, point[1], point[0])
        div_GPS_list.append(new)
        print(f"{new}")

    div_filename = f"{parent_dir}/data/div.txt"  # Set the filename
    with open(div_filename, 'w') as file:
        for pos in div_GPS_list:
            file.write(f"{pos[0]}, {pos[1]}\n")

    # Rotate and shift the coordinate
    rotated_div_points = []
    print(f"DIV_ROTATED")
    for point in div_points:
        new_point = rotate_and_shift_point(
            point[0], point[1], (-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1]))
        rotated_div_points.append(new_point)
        print(f"{new_point}")

    rotated_perpendicular_points = []
    print(f"PERP_ROTATED")
    for point in perpendicular_points:
        new_point = rotate_and_shift_point(
            point[0], point[1], (-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1]))
        rotated_perpendicular_points.append(new_point)
        print(f"{new_point}")

    print(f"PERP_UNROTATED")
    for point in perpendicular_points:
        print(f"{point}")

    print(f"POLYGON_ROTATED")
    rotated_cartesian_coordinates = []
    for point in cartesian_coordinates:
        new_point = rotate_and_shift_point(
            point[0], point[1], (-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1]))
        rotated_cartesian_coordinates.append(new_point)
        print(f"{new_point}")
    print(f"POLYGON_UNROTATED")
    for point in cartesian_coordinates:
        print(f"{point}")

    rotate_polygon = []
    # Points lie on polygon egde = vertices + divide points
    rotate_polygon = rotated_div_points + rotated_cartesian_coordinates

    # Separate the point into different parts
    rotated_area = split_area(rotate_polygon, rotated_perpendicular_points)
    final_area = []

    print(f"POLYGON_UNROTATED_BACK")
    for point in rotated_cartesian_coordinates:
        # convert back in previous coordinate
        new_point = revert_rotate_and_shift_point(
            point[0], point[1], (-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1]), clockwise=True)
        print(f"{new_point}")

    for i in range(len(rotated_area)):
        area = rotated_area[i]
        unrotated_area = []
        print(f"{area}")
        for point in area:
            # convert back in previous coordinate
            new_point = revert_rotate_and_shift_point(
                point[0], point[1], (-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1]), clockwise=True)
            unrotated_area.append(new_point)
        per_GPS_list = []
        for point in unrotated_area:
            new = calculate_new_lat_lon(min_lat, min_lon, point[1], point[0])
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
        area_filename = f"{parent_dir}/data/area{i+1}.txt"  # Set the filename
        with open(area_filename, 'w') as file:
            for pos in points:
                file.write(f"{pos[0]}, {pos[1]}\n")

    print(f"FINAL AREA")
    for i in range(len(final_area)):
        print(f"{i}")
        print(f"{final_area[i]}")

    return final_area, rotated_area


def chia_luoi(rotated_area, distance):
    print(f"rotated")
    print(f"{rotated_area}")
    areas_dot = []
    for i, area in enumerate(rotated_area):

        points = np.array(area)

        # Calculate the convex hull
        hull = ConvexHull(points)

        # Extract the vertices of the convex hull
        hull_vertices = points[hull.vertices]

        # Convert the vertices back to a list of tuples
        points = [tuple(point) for point in hull_vertices]

        grid_points = generate_grid(points, float(distance))

        areas_dot.append(grid_points)

    print(f"areas")
    print(f"{areas_dot}")

    grid_GPS = []
    for i, area in enumerate(areas_dot):
        area = areas_dot[i]
        unrotated_area = []
        for point in area:
            # convert back in previous coordinate
            new_point = revert_rotate_and_shift_point(
                point[0], point[1], (-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1]), clockwise=True)
            unrotated_area.append(new_point)
        per_GPS_list = []
        for point in unrotated_area:
            new = calculate_new_lat_lon(min_lat, min_lon, point[1], point[0])
            per_GPS_list.append(new)
        grid_GPS.append(per_GPS_list)
    print(f"GPS")
    print(f"{grid_GPS}")

    return grid_GPS


def chia_luoi_one(area, distance):

    min_lat = min(area, key=lambda x: x[0])[0]
    min_lon = min(area, key=lambda x: x[1])[1]
    # Convert the geographic positions to Cartesian coordinates
    cartesian_coordinates = convert_to_cartesian(area)
    print("Cartesian Coordinates:")
    for coord in cartesian_coordinates:
        print(coord)

    # Find the largest edge
    longest, longest_edge_point = find_longest_edge(cartesian_coordinates)
    print(f"\nEdge: {longest}")
    for coord in longest_edge_point:
        print(coord)

    # Find midpont of largest edge
    midpoint = find_midpoint(longest_edge_point[0], longest_edge_point[1])
    print(f"\nMidpoint: {midpoint}")
    new = calculate_new_lat_lon(min_lat, min_lon, midpoint[1], midpoint[0])
    print(f"\nGPS Midpoint: {new}")

    # Find line equation of largest edge (to figure out the slope of it)
    slope, intercept = line_equation_from_points(
        longest_edge_point[0], longest_edge_point[1])
    print(f"\nSlope: {slope}")
    angle = angle_with_x_axis(slope)
    print(f"\nAngle: {angle}")

    rotated = []
    for point in cartesian_coordinates:
        new_point = rotate_and_shift_point(
            point[0], point[1], (-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1]))
        rotated.append(new_point)
        print(f"{new_point}")

    points = np.array(rotated)

    # Calculate the convex hull
    hull = ConvexHull(points)

    # Extract the vertices of the convex hull
    hull_vertices = points[hull.vertices]

    # Convert the vertices back to a list of tuples
    points = [tuple(point) for point in hull_vertices]

    grid_points = generate_grid(points, int(distance))

    unrotated_area = []
    for point in grid_points:
        # convert back in previous coordinate
        new_point = revert_rotate_and_shift_point(
            point[0], point[1], (-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1]), clockwise=True)
        unrotated_area.append(new_point)
    per_GPS_list = []
    for point in unrotated_area:
        new = calculate_new_lat_lon(min_lat, min_lon, point[1], point[0])
        per_GPS_list.append(new)

    return per_GPS_list
