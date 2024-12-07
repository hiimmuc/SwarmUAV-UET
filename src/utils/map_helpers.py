import copy
import math
import sys
from pathlib import Path

import numpy as np
from scipy.spatial import ConvexHull

from .calculation_helpers import *

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
                if (
                    min(y1, y2) <= intersect_y <= max(y1, y2)
                    and abs(intersect_x - mid[0]) > tolerance
                    and abs(intersect_y - mid[1]) > tolerance
                ):
                    return intersect_x, intersect_y

        else:  # Non-vertical edge
            edge_slope = (y2 - y1) / (x2 - x1)
            edge_intercept = y1 - edge_slope * x1

            # The line is vertical, use its x-intercept (which is actually the x coordinate)
            if slope is None:
                intersect_x = intercept
                intersect_y = edge_slope * intersect_x + edge_intercept
                if (
                    min(x1, x2) <= intersect_x <= max(x1, x2)
                    and abs(intersect_y - mid[1]) > tolerance
                ):
                    return intersect_x, intersect_y

            elif slope != edge_slope:  # The line is not vertical and not parallel to the edge
                intersect_x = (edge_intercept - intercept) / (slope - edge_slope)
                intersect_y = slope * intersect_x + intercept

                if (
                    min(x1, x2) <= intersect_x <= max(x1, x2)
                    and min(y1, y2) <= intersect_y <= max(y1, y2)
                    and (
                        abs(intersect_x - mid[0]) > tolerance
                        or abs(intersect_y - mid[1]) > tolerance
                    )
                ):
                    return intersect_x, intersect_y
    return None


def split_area(positions, number_of_part):
    def split(area, perp, tolerance=1e-6):
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
                        if y_geq_with_tolerance(
                            point[1], previous_perp_y
                        ) and y_leq_with_tolerance(point[1], perp_y):
                            one_area.append(point)
                    area_list.append(one_area)
                    one_area = []
                    for point in area:
                        if y_geq_with_tolerance(point[1], perp_y):
                            one_area.append(point)

                else:
                    previous_perp_y = perp[i - 1][1]
                    for point in area:
                        if y_geq_with_tolerance(
                            point[1], previous_perp_y
                        ) and y_leq_with_tolerance(point[1], perp_y):
                            one_area.append(point)

                area_list.append(one_area)

        return area_list

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
    slope, intercept = line_equation_from_points(longest_edge_point[0], longest_edge_point[1])
    print(f"\nSlope: {slope}")
    angle = angle_with_x_axis(slope)
    print(f"\nAngle: {angle}")

    new_point = rotate_and_shift_point(
        midpoint[0],
        midpoint[1],
        (-angle),
        midpoint[0],
        midpoint[1],
        (-midpoint[0]),
        (-midpoint[1]),
    )
    print(f"ROTATED MIDPOINT{new_point}")

    # Find the perpendicular's line equation (perpendicular of largest edge)
    perp_slope, perp_intercept = perpendicular_line_equation(midpoint, slope)
    print(f"\nPerp_slope: {perp_slope},Perp_intercep: {perp_intercept}")

    # Find the other intersection of the perpendicular with the polygon
    intersect_point = does_line_intersect_polygon(
        midpoint, perp_slope, perp_intercept, cartesian_coordinates
    )
    print(f"\nIntersect: {intersect_point[0]},{intersect_point[1]}")
    new = calculate_new_lat_lon(min_lat, min_lon, intersect_point[1], intersect_point[0])
    print(f"\nGPS Intersect: {new}")

    # ---------------------------------

    # ---------------------------------
    # Divide the perpendicular into equal parts
    perpendicular_points = divide_line_into_segments(
        midpoint[0], midpoint[1], intersect_point[0], intersect_point[1], number_of_part
    )

    per_GPS_list = []
    for point in perpendicular_points:
        new = calculate_new_lat_lon(min_lat, min_lon, point[1], point[0])
        per_GPS_list.append(new)
        print(f"{point}")
    p_filename = f"{parent_dir}/data/per.txt"  # Set the filename
    with open(p_filename, "w") as file:
        for pos in per_GPS_list:
            file.write(f"{pos[0]}, {pos[1]}\n")

    # Find the divide point on the polygon edge
    div_GPS_list = []
    div_points = divide_points(perpendicular_points, cartesian_coordinates, perp_slope, slope)
    for point in div_points:
        new = calculate_new_lat_lon(min_lat, min_lon, point[1], point[0])
        div_GPS_list.append(new)
        print(f"{new}")

    div_filename = f"{parent_dir}/data/div.txt"  # Set the filename
    with open(div_filename, "w") as file:
        for pos in div_GPS_list:
            file.write(f"{pos[0]}, {pos[1]}\n")

    # Rotate and shift the coordinate
    rotated_div_points = []
    print(f"DIV_ROTATED")
    for point in div_points:
        new_point = rotate_and_shift_point(
            point[0], point[1], (-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1])
        )
        rotated_div_points.append(new_point)
        print(f"{new_point}")

    rotated_perpendicular_points = []
    print(f"PERP_ROTATED")
    for point in perpendicular_points:
        new_point = rotate_and_shift_point(
            point[0], point[1], (-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1])
        )
        rotated_perpendicular_points.append(new_point)
        print(f"{new_point}")

    print(f"PERP_UNROTATED")
    for point in perpendicular_points:
        print(f"{point}")

    print(f"POLYGON_ROTATED")
    rotated_cartesian_coordinates = []
    for point in cartesian_coordinates:
        new_point = rotate_and_shift_point(
            point[0], point[1], (-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1])
        )
        rotated_cartesian_coordinates.append(new_point)
        print(f"{new_point}")
    print(f"POLYGON_UNROTATED")
    for point in cartesian_coordinates:
        print(f"{point}")

    rotate_polygon = []
    # Points lie on polygon egde = vertices + divide points
    rotate_polygon = rotated_div_points + rotated_cartesian_coordinates

    # Separate the point into different parts
    rotated_area = split(rotate_polygon, rotated_perpendicular_points)
    final_area = []

    print(f"POLYGON_UN-ROTATED_BACK")
    for point in rotated_cartesian_coordinates:
        # convert back in previous coordinate
        new_point = revert_rotate_and_shift_point(
            point[0],
            point[1],
            (-angle),
            midpoint[0],
            midpoint[1],
            (-midpoint[0]),
            (-midpoint[1]),
            clockwise=True,
        )
        print(f"{new_point}")

    for i in range(len(rotated_area)):
        area = rotated_area[i]
        unrotated_area = []
        print(f"{area}")
        for point in area:
            # convert back in previous coordinate
            new_point = revert_rotate_and_shift_point(
                point[0],
                point[1],
                (-angle),
                midpoint[0],
                midpoint[1],
                (-midpoint[0]),
                (-midpoint[1]),
                clockwise=True,
            )
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
        with open(area_filename, "w") as file:
            for pos in points:
                file.write(f"{pos[0]}, {pos[1]}\n")

    print(f"FINAL AREA")
    for i in range(len(final_area)):
        print(f"{i}")
        print(f"{final_area[i]}")

    return final_area, rotated_area


def split_grid(rotated_area, distance):
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
                point[0],
                point[1],
                (-angle),
                midpoint[0],
                midpoint[1],
                (-midpoint[0]),
                (-midpoint[1]),
                clockwise=True,
            )
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
    slope, intercept = line_equation_from_points(longest_edge_point[0], longest_edge_point[1])
    print(f"\nSlope: {slope}")
    angle = angle_with_x_axis(slope)
    print(f"\nAngle: {angle}")

    rotated = []
    for point in cartesian_coordinates:
        new_point = rotate_and_shift_point(
            point[0], point[1], (-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1])
        )
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
            point[0],
            point[1],
            (-angle),
            midpoint[0],
            midpoint[1],
            (-midpoint[0]),
            (-midpoint[1]),
            clockwise=True,
        )
        unrotated_area.append(new_point)
    per_GPS_list = []
    for point in unrotated_area:
        new = calculate_new_lat_lon(min_lat, min_lon, point[1], point[0])
        per_GPS_list.append(new)

    return per_GPS_list


import math
from tkinter import filedialog

import numpy as np
from scipy.spatial import ConvexHull, Delaunay

from utils.calculation_helpers import *

x_coords = []
y_coords = []


def ray_casting_point_in_polygon(point, polygon):
    """
    Determine if a point is inside a polygon using the Ray Casting method.

    :param point: A tuple (lat, lon) representing the point to check.
    :param polygon: A list of tuples [(lat, lon), ...] representing the polygon vertices.
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
    Generate grid points within the polygon defined by `vertices`.
    """
    # Approximate conversion between lat/lon and meters
    lat_to_meters = 111134.861111  # meters per degree latitude
    lon_to_meters = 111319.488  # meters per degree longitude at equator

    # Bounding box
    min_lat = min(v[0] for v in vertices)
    max_lat = max(v[0] for v in vertices)
    min_lon = min(v[1] for v in vertices)
    max_lon = max(v[1] for v in vertices)

    avg_lat = (min_lat + max_lat) / 2
    lon_to_meters *= np.cos(np.radians(avg_lat))

    num_points_lat = int(((max_lat - min_lat) * lat_to_meters) / spacing_m)
    num_points_lon = int(((max_lon - min_lon) * lon_to_meters) / spacing_m)

    points = []  # diem luoi
    for i in range(num_points_lat + 1):
        for j in range(num_points_lon + 1):
            lat = min_lat + (i * spacing_m / lat_to_meters)
            lon = min_lon + (j * spacing_m / lon_to_meters)
            if ray_casting_point_in_polygon((lat, lon), vertices):
                points.append((lat, lon))

    return points


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


def open_file(position_list):
    filename = filedialog.askopenfilename(
        initialdir="src/logs/points",
        title="Chọn file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
    )
    if filename:
        x_coords_file, y_coords_file = read_points_from_file(filename)
        x_coords.clear()
        y_coords.clear()
        if x_coords_file and y_coords_file:
            x_coords.extend(x_coords_file)
            y_coords.extend(y_coords_file)

        for x, y in zip(x_coords, y_coords):

            position_list.append([x, y])  # them diem vao danh sach


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


def check_and_move_points(edge_points, rest_points, tolerance=10):
    """
    Check if points in rest_points lie on the path created by edge_points and move them accordingly.
    """
    new_edge_points = edge_points.copy()
    to_move = []

    for rp in rest_points:
        for i in range(len(new_edge_points) - 1):
            if new_edge_points[i] == (21.04004113210685, 105.7986763205447) and new_edge_points[
                i + 1
            ] == (21.04004113210685, 105.79578882254137):
                print("YES")

            angle_with_rp = calculate_angle(new_edge_points[i + 1], new_edge_points[i], rp)
            angle_2 = calculate_angle(new_edge_points[i + 1], rp, new_edge_points[i])
            if (
                rp == (21.04004113210685, 105.79771382121027)
                or rp == (21.04004113210685, 105.79675132187582)
            ) and (
                new_edge_points[i] == (21.04004113210685, 105.7986763205447)
                and new_edge_points[i + 1] == (21.04004113210685, 105.79578882254137)
            ):
                print(f"{angle_with_rp}")
                print(f"{angle_2}")
            if angle_with_rp < tolerance or (angle_2 > 350 and angle_2 < 360):
                to_move.append(rp)
                break

    # Move the points that are close enough to the path from rest_points to edge_points
    for point in to_move:
        if point in rest_points:
            rest_points.remove(point)
            new_edge_points.append(point)

    return new_edge_points, rest_points


def reorder_list(start_point, list1):
    distances = []
    # Calculate the distance from start_point to each point in list1
    for point in list1:
        distance = haversine(start_point[0], start_point[1], point[0], point[1])
        distances.append((point, distance))

    # Find the nearest point and its index
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
    farthest_index = distances.index(max(distances))

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


def find_path(points, point_A):
    List1, List2 = find_polygon_edges(points)

    for i, point in enumerate(List1):
        print(f"{point}")

    list_A, list_B = check_and_move_points(List1, List2)

    List_a0, List_a1 = find_polygon_edges(list_A)
    list_B.extend(List_a1)

    list_A, list_B = check_and_move_points(List_a0, list_B)

    list_A = sort_polygon_vertices(list_A)

    list_A = reorder_list(point_A, list_A)

    list_A, list_B = split_at_farthest_point(point_A, list_A, list_B)

    # Assuming list_2 and point_A are defined
    path_list_2 = find_shortest_path(point_A, list_B.copy())

    list_A.pop()
    list_A.extend(path_list_2)

    return list_A, path_list_2


def open_file(position_list):
    filename = filedialog.askopenfilename(
        initialdir="./",
        title="Chọn file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
    )
    if filename:
        x_coords_file, y_coords_file = read_points_from_file(filename)
        x_coords.clear()
        y_coords.clear()
        if x_coords_file and y_coords_file:
            x_coords.extend(x_coords_file)
            y_coords.extend(y_coords_file)

        for x, y in zip(x_coords, y_coords):
            position_list.append([x, y])  # them diem vao danh sach


def sort_polygon_vertices(vertices):
    # Calculate centroid of the polygon
    centroid_x = sum(x for x, y in vertices) / len(vertices)
    centroid_y = sum(y for x, y in vertices) / len(vertices)
    centroid = (centroid_x, centroid_y)

    # Define a function to calculate the angle between centroid and vertex
    def angle_from_centroid(vertex):
        return math.atan2(vertex[1] - centroid_y, vertex[0] - centroid_x)

    # Sort vertices by the angle from centroid
    sorted_vertices = sorted(vertices, key=angle_from_centroid, reverse=True)

    return sorted_vertices


def process_grid_points(grid_points, drone_position):
    global area_grid, ordered_grid_points

    if multi_area:
        for area in grid_points:
            # print("AREA", area)
            # print(drone_position_list)
            ordered_grid_points = find_path(area, drone_position)
            # print(ordered_grid_points)
            area_grid.append(ordered_grid_points)
    else:
        ordered_grid_points = find_path(grid_points, drone_position)
        area_grid.append(ordered_grid_points)

    return area_grid


def point_on_line(point_a, point_c, point_b, margin_of_error=0.0001):
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
