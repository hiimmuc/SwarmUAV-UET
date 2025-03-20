import copy
import math
import sys
from pathlib import Path
from tkinter import filedialog

import numpy as np
from scipy.spatial import ConvexHull, Delaunay

from .calculation_helpers import *

parent_dir = Path(__file__).parent.parent


# -------------User defined functions------------
def area_of_polygon(vertices):
    """Calculate the area of a polygon defined by the given vertices.

    Args:
        vertices (List[List(float)]): [[x1, y1], [x2, y2], ...] such that the polygon is defined by the vertices.

    Returns:
        Float: Area of the polygon.
    """
    area = 0
    n = len(vertices)
    if len(vertices) < 3:
        return 0

    for i in range(n - 1):
        p1 = vertices[i]
        p2 = vertices[i + 1]
        area += convert_degrees_to_radius(p2[1] - p1[1]) * (
            2
            + math.sin(convert_degrees_to_radius(p1[0]))
            + math.sin(convert_degrees_to_radius(p2[0]))
        )
    area = area * EARTH_RADIUS**2 / 2

    # return in square meters, kilometers, and ha
    return {
        "m2": abs(area),
        "km2": abs(area) / 1e6,
        "ha": abs(area) / 1e4,
    }


def split_polygon_into_areas(vertices, number_of_parts):
    """Split a polygon defined by the given vertices into a number of parts.

    Args:
        vertices (List[List(float)]): [[x1, y1], [x2, y2], ...] such that the polygon is defined by the vertices.
        number_of_parts (int): Number of parts to split the polygon into.

    Returns:
        List[List[List(float)]]: A list of lists of vertices defining the split areas.
    """
    splitted_areas = {}
    result = {}
    # Convert the list of positions to a NumPy array
    points = np.array(vertices)

    ref_lat = min(points, key=lambda x: x[0])[0]
    ref_lon = min(points, key=lambda x: x[1])[1]

    if len(points) < 3:
        return result

    cartesian_coordinates = convert_to_cartesian(points)

    if not is_polygon_convex(cartesian_coordinates):
        return result

    # 1. Find longest edge
    longest_edge_points = find_longest_edge(cartesian_coordinates)
    # 2. Find the perpendicular line to the longest edge at midpoint
    main_perpendicular_line = perpendicular_lines_at_points(longest_edge_points, N=2)[0]
    intersection_pts_of_perpendicular_line = find_polygon_line_intersections(
        cartesian_polygon=cartesian_coordinates, line=main_perpendicular_line
    )
    perp_line_within_polygon = intersection_pts_of_perpendicular_line
    # 3. Divide the perpendicular line into equal parts, and find the lines parallel to the longest edge
    parallel_lines_to_longest_edge = perpendicular_lines_at_points(
        perp_line_within_polygon, N=number_of_parts
    )
    parallel_lines_to_longest_edge.sort(key=lambda x: x[1])  # sort by the intercept

    # 4. Find the intersection points of the parallel lines with the polygon
    intersection_pts_of_parallel_lines = [
        find_polygon_line_intersections(cartesian_coordinates, line)
        for line in parallel_lines_to_longest_edge
    ]

    # 5. Split the polygon into equal parts
    for index, line in enumerate(parallel_lines_to_longest_edge):
        for point in cartesian_coordinates[:-1]:
            if is_left_of_line(point, line):
                splitted_areas.setdefault(index, {}).setdefault("left", []).append(point)
            else:
                splitted_areas.setdefault(index, {}).setdefault("right", []).append(point)

    result[0] = splitted_areas[0]["right"] + intersection_pts_of_parallel_lines[0]

    # between 2 lines add the points that are between them
    for i in range(1, number_of_parts - 1):
        addition_pts = [
            pt
            for pt in cartesian_coordinates[:-1]
            if is_between_lines(
                pt, parallel_lines_to_longest_edge[i - 1], parallel_lines_to_longest_edge[i]
            )
        ]
        # addition_pts = [pt for pt in splitted_areas[i]['right'] if pt not in result[i - 1]]
        result[i] = (
            addition_pts
            + intersection_pts_of_parallel_lines[i - 1]
            + intersection_pts_of_parallel_lines[i]
        )

    result[number_of_parts - 1] = (
        splitted_areas[number_of_parts - 1 - 1]["left"] + intersection_pts_of_parallel_lines[-1]
    )
    # convert the result to lat lon
    gps_result = {}
    for key, value in result.items():
        gps_result[key] = []
        for point in value:
            gps_result[key].append(convert_to_lat_lon([ref_lat, ref_lon], point))

    return {
        "cartesian": result,
        "lat_lon": gps_result,
    }


def split_polygon_into_areas_old(vertices, number_of_parts):
    """Split a polygon defined by the given vertices into a number of parts.

    Args:
        vertices (List[List(float)]): [[x1, y1], [x2, y2], ...] such that the polygon is defined by the vertices.
        number_of_parts (int): Number of parts to split the polygon into.

    Returns:
        List[List[List(float)]]: A list of lists of vertices defining the split areas.
    """
    # global angle, midpoint, min_lat, min_lon
    positions = vertices
    number_of_part = number_of_parts

    min_lat = min(positions, key=lambda x: x[0])[0]
    min_lon = min(positions, key=lambda x: x[1])[1]
    # Convert the geographic positions to Cartesian coordinates
    cartesian_coordinates = convert_to_cartesian(positions)
    # print("Cartesian Coordinates:")
    # for coord in cartesian_coordinates:
    #     print(coord)

    # Find the largest edge
    _, longest_edge_point = find_longest_edge(cartesian_coordinates)
    # print(f"\nEdge: {longest}")
    # for coord in longest_edge_point:
    #     print(coord)

    # Find midpont of largest edge
    midpoint = find_midpoint(longest_edge_point[0], longest_edge_point[1])
    # print(f"\nMidpoint: {midpoint}")
    new = calculate_new_lat_lon(min_lat, min_lon, midpoint[1], midpoint[0])
    # print(f"\nGPS Midpoint: {new}")

    # Find line equation of largest edge (to figure out the slope of it)
    slope, intercept = line_equation_from_points(longest_edge_point[0], longest_edge_point[1])
    # print(f"\nSlope: {slope}")
    angle = angle_with_x_axis(slope)
    # print(f"\nAngle: {angle}")

    new_point = rotate_and_shift_point(
        midpoint[0],
        midpoint[1],
        (-angle),
        midpoint[0],
        midpoint[1],
        (-midpoint[0]),
        (-midpoint[1]),
    )
    # print(f"ROTATED MIDPOINT{new_point}")

    # Find the perpendicular's line equation (perpendicular of largest edge)
    perp_slope, perp_intercept = perpendicular_line_equation(midpoint, slope)
    # print(f"\nPerp_slope: {perp_slope},Perp_intercep: {perp_intercept}")

    # Find the other intersection of the perpendicular with the polygon
    intersect_point = does_line_intersect_polygon(
        midpoint, perp_slope, perp_intercept, cartesian_coordinates
    )
    # print(f"\nIntersect: {intersect_point[0]},{intersect_point[1]}")
    new = calculate_new_lat_lon(min_lat, min_lon, intersect_point[1], intersect_point[0])
    # print(f"\nGPS Intersect: {new}")

    # ---------------------------------

    # ---------------------------------
    # Divide the perpendicular into equal parts
    perpendicular_points = divide_line_into_segments(
        midpoint[0], midpoint[1], intersect_point[0], intersect_point[1], number_of_part
    )
    # print(f"\nPerpendicular Points: {perpendicular_points}")
    per_GPS_list = []
    for point in perpendicular_points:
        new = calculate_new_lat_lon(min_lat, min_lon, point[1], point[0])
        per_GPS_list.append(new)
        # print(f"{point}")

    # Find the divide point on the polygon edge
    div_GPS_list = []
    div_points = divide_points(perpendicular_points, cartesian_coordinates, perp_slope, slope)
    for point in div_points:
        new = calculate_new_lat_lon(min_lat, min_lon, point[1], point[0])
        div_GPS_list.append(new)
        # print(f"{new}")

    # Rotate and shift the coordinate
    rotated_div_points = []
    # print(f"DIV_ROTATED")
    for point in div_points:
        new_point = rotate_and_shift_point(
            point[0], point[1], (-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1])
        )
        rotated_div_points.append(new_point)
        # print(f"{new_point}")

    rotated_perpendicular_points = []
    # print(f"PERP_ROTATED")
    for point in perpendicular_points:
        new_point = rotate_and_shift_point(
            point[0], point[1], (-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1])
        )
        rotated_perpendicular_points.append(new_point)
        # print(f"{new_point}")

    # print(f"PERP_UNROTATED")
    # for point in perpendicular_points:
    # print(f"{point}")

    # print(f"POLYGON_ROTATED")
    rotated_cartesian_coordinates = []
    for point in cartesian_coordinates:
        new_point = rotate_and_shift_point(
            point[0], point[1], (-angle), midpoint[0], midpoint[1], (-midpoint[0]), (-midpoint[1])
        )
        rotated_cartesian_coordinates.append(new_point)
        # print(f"{new_point}")
    # print(f"POLYGON_UNROTATED")
    # for point in cartesian_coordinates:
    # print(f"{point}")

    rotate_polygon = []
    # Points lie on polygon egde = vertices + divide points
    rotate_polygon = rotated_div_points + rotated_cartesian_coordinates

    # Separate the point into different parts
    rotated_area = split_area(rotate_polygon, rotated_perpendicular_points)
    final_area = []

    # print(f"POLYGON_UNROTATED_BACK")
    # for point in rotated_cartesian_coordinates:
    #     # convert back in previous coordinate
    #     new_point = revert_rotate_and_shift_point(
    #         point[0],
    #         point[1],
    #         (-angle),
    #         midpoint[0],
    #         midpoint[1],
    #         (-midpoint[0]),
    #         (-midpoint[1]),
    #         clockwise=True,
    #     )
    # print(f"{new_point}")

    for i in range(len(rotated_area)):
        area = rotated_area[i]
        unrotated_area = []
        # print(f"{area}")
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
            # print(f"{new}")
        # Convert the list of positions to a NumPy array

        points = np.array(per_GPS_list)

        # Calculate the convex hull
        hull = ConvexHull(points)

        # Extract the vertices of the convex hull
        hull_vertices = points[hull.vertices]

        # Convert the vertices back to a list of tuples
        points = [tuple(point) for point in hull_vertices]
        final_area.append(points)

    return final_area, rotated_area, angle, midpoint, min_lat, min_lon


def split_grids(rotated_area, angle, midpoint, min_lat, min_lon, grid_size, n_areas):

    distance = grid_size

    if n_areas in (0, 1):
        area = rotated_area[0]
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
                point[0],
                point[1],
                (-angle),
                midpoint[0],
                midpoint[1],
                (-midpoint[0]),
                (-midpoint[1]),
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
    else:
        # n areas > 1
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

        return grid_GPS
    pass


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


def remove_duplicate_pts(vertices):
    """
    Remove duplicate points from a list of vertices.

    :param vertices: List of (x, y) tuples for the vertices.
    :return: List of (x, y) tuples for the vertices with duplicates removed.
    """
    temp = []
    for i in vertices:
        if i not in temp:
            temp.append(i)
    return temp


if __name__ == "__main__":
    pass
