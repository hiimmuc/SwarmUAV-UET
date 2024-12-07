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


def main():

    positions = [
        (21.040940939772963, 105.79001382653469),
        (21.040940939772963, 105.79097632586914),
        (21.040940939772963, 105.79193882520359),
        (21.040940939772963, 105.79290132453802),
        (21.040940939772963, 105.79386382387247),
        (21.040940939772963, 105.79482632320692),
        (21.040940939772963, 105.79578882254137),
        (21.040940939772963, 105.79675132187582),
        (21.040940939772963, 105.79771382121027),
        (21.040940939772963, 105.7986763205447),
        (21.04004113210685, 105.7986763205447),
        (21.04004113210685, 105.79771382121027),
        (21.04004113210685, 105.79675132187582),
        (21.04004113210685, 105.79578882254137),
        (21.041840747439075, 105.79578882254137),
        (21.041840747439075, 105.79482632320692),
        (21.041840747439075, 105.79386382387247),
        (21.041840747439075, 105.79290132453802),
        (21.041840747439075, 105.79193882520359),
        (21.041840747439075, 105.79097632586914),
        (21.041840747439075, 105.79001382653469),
        (21.042740555105187, 105.79001382653469),
        (21.042740555105187, 105.79097632586914),
        (21.042740555105187, 105.79193882520359),
        (21.042740555105187, 105.79290132453802),
        (21.042740555105187, 105.79386382387247),
        (21.042740555105187, 105.79482632320692),
        (21.042740555105187, 105.79578882254137),
        (21.042740555105187, 105.79675132187582),
        (21.042740555105187, 105.79771382121027),
        (21.041840747439075, 105.79771382121027),
        (21.041840747439075, 105.7986763205447),
        (21.041840747439075, 105.79675132187582),
        (21.0436403627713, 105.79675132187582),
        (21.0436403627713, 105.79578882254137),
        (21.0436403627713, 105.79482632320692),
        (21.0436403627713, 105.79386382387247),
        (21.0436403627713, 105.79290132453802),
        (21.0436403627713, 105.79193882520359),
        (21.0436403627713, 105.79097632586914),
        (21.0436403627713, 105.79001382653469),
        (21.04454017043741, 105.79097632586914),
        (21.04454017043741, 105.79193882520359),
        (21.04454017043741, 105.79290132453802),
        (21.04454017043741, 105.79386382387247),
        (21.04454017043741, 105.79482632320692),
        (21.04454017043741, 105.79578882254137),
        (21.04454017043741, 105.79675132187582),
        (21.04454017043741, 105.79771382121027),
        (21.0436403627713, 105.79771382121027),
        (21.045439978103524, 105.79193882520359),
    ]

    # Starting point A
    start_position = (21.047237124293158, 105.80388472410394)

    position_list1 = []

    # List1, List2 = find_polygon_edges(positions)
    # list_A, list_B = check_and_move_points(List1,List2)

    # # Convert the list of positions to a NumPy array
    # points = np.array(list_A)

    # # Calculate the convex hull
    # hull = ConvexHull(points)

    # # Extract the vertices of the convex hull
    # list_A = points[hull.vertices].tolist()

    # list_A = reorder_list(start_position, list_A)

    # list_A, list_B = split_at_farthest_point(start_position, list_A, list_B)

    # Assuming list_2 and point_A are defined
    # path_list_2 = find_shortest_path( start_position, list_B.copy())  # Using list_2.copy() to keep the original list_2 unchanged for display purposes

    open_file(position_list1)
    grid_points = generate_grid(position_list1, int(100))

    with open("src/data/drone_path_all.txt", "w") as file:
        for pos in grid_points:
            file.write(f"{pos[0]}, {pos[1]}\n")

    Listx, Listy = find_path(grid_points, start_position)
    # Write the result to a text file
    with open("src/data/drone_path_A.txt", "w") as file:
        for pos in Listx:
            file.write(f"{pos[0]}, {pos[1]}\n")

    # Write the result to a text file
    with open("src/data/drone_path_B.txt", "w") as file:
        for pos in Listy:
            file.write(f"{pos[0]}, {pos[1]}\n")


if __name__ == "__main__":
    main()
