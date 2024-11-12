import math
from tkinter import filedialog
import math
import numpy as np
from scipy.spatial import ConvexHull, Delaunay
from .calculation_helpers import *

x_coords = []
y_coords = []


def read_points_from_file(filename):
    try:
        with open(filename, 'r') as file:
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


def calculate_angle(a, b, c):
    ba = (a[0] - b[0], a[1] - b[1])
    bc = (c[0] - b[0], c[1] - b[1])
    dot_prod = ba[0] * bc[0] + ba[1] * bc[1]
    mag_ab = math.sqrt(ba[0]**2 + ba[1]**2)
    mag_bc = math.sqrt(bc[0]**2 + bc[1]**2)
    if mag_ab == 0 or mag_bc == 0:
        return 0
    # Clamping value to the valid range of acos
    cosine_angle = max(-1, min(1, dot_prod / (mag_ab * mag_bc)))
    angle = math.acos(cosine_angle)
    cross_product = ba[0] * bc[1] - ba[1] * bc[0]
    angle_degrees = math.degrees(angle)
    if cross_product > 0:
        angle_degrees = 360 - angle_degrees
    return angle_degrees


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
            if point_on_line(list_A[i], point, list_A[i+1]):
                updated_list_A.append(point)
                updated_list_B.remove(point)
                break  # Move to the next point after finding its place

    return updated_list_A, updated_list_B


def reorder_list(start_point, list1):
    distances = []
    # Calculate the distance from start_point to each point in list1
    for point in list1:
        distance = haversine(
            start_point[0], start_point[1], point[0], point[1])
        distances.append((point, distance))

    # Find the nearest point and its index
    # TÌM ĐIỂM GẦN NHẤT VỚI DRONE
    nearest_point, _ = min(distances, key=lambda x: x[1])
    nearest_index = list1.index(nearest_point)

    # Reorder the list starting with the nearest point
    reordered_list = list1[int(nearest_index):] + list1[:int(nearest_index)]

    return reordered_list


def split_at_farthest_point(start_position, reordered_points, list_2):
    # Calculate the distance of each point from the start position
    distances = [haversine(start_position[0], start_position[1],
                           point[0], point[1]) for point in reordered_points]

    # Find the index of the farthest point
    farthest_index = distances.index(
        max(distances))  # TÌM ĐIỂM XA NHẤT VỚI DRONE

    # Split the reordered list at the farthest point, including the farthest point in the first part
    keep_points = reordered_points[:farthest_index+1]
    move_to_list_2 = reordered_points[farthest_index+1:]
    list_2.extend(move_to_list_2)

    # Duplicate the last point in keep_points
    last_point = keep_points[-1]

    # Put it at the beginning of list_2
    list_2.insert(0, last_point)

    return keep_points, list_2


def find_nearest_to_A(points, point_A):
    # Calculate distances to point A and find the minimum
    distances = [haversine(point[0], point[1], point_A[0],
                           point_A[1]) for point in points]
    min_distance_index = distances.index(min(distances))
    return points[min_distance_index]


def find_shortest_path(start_position, points_list):
    # Calculate the distance from point A to all other points
    distances_to_A = [haversine(
        start_position[0], start_position[1], point[0], point[1]) for point in points_list]

    # Identify the nearest point to point A (to be the last point)
    nearest_to_A_index = distances_to_A.index(min(distances_to_A))
    # Remove and save the nearest point
    point_nearest_to_A = points_list.pop(nearest_to_A_index)

    # Start with the beginning point, already placed from keep_points
    path = [points_list.pop(0)]

    # Use a modified nearest neighbor algorithm to construct the path
    while points_list:
        last_point = path[-1]
        nearest_index = min(range(len(points_list)), key=lambda i: haversine(
            last_point[0], last_point[1], points_list[i][0], points_list[i][1]))
        nearest_point = points_list.pop(nearest_index)
        path.append(nearest_point)

    # Append the point nearest to A at the end of the path
    path.append(point_nearest_to_A)

    return path


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


def find_path(points, point_A):
    # TÌM CẠNH CỦA ĐA GIÁC (BƯỚC NÀY TÌM ĐƯỢC GÓC CỦA ĐA GIÁC)
    List1, List2 = find_polygon_edges(points)

    for i, point in enumerate(List1):
        print(f"{point}")

    # TÌM CẠNH CỦA ĐA GIÁC (BƯỚC NÀY TÌM ĐƯỢC CÁC ĐIỂM NẰM TRÊN CẠNH ĐA GIÁC)
    list_A, list_B = check_and_move_points(List1, List2)

    # Sắp xếp các điểm trên cạnh của đa giác theo thứ tự
    list_A = sort_polygon_vertices(list_A)

    # Sắp xếp các điểm trên cạnh của đa giác bắt đầu từ điểm gần drone nhất
    list_A = reorder_list(point_A, list_A)

    # Tách đường đi của Drone thành 2 phần, phần 1 đi từ điểm gần drone nhất đến điểm xã drone nhất theo cạnh của đa giác
    list_A, list_B = split_at_farthest_point(point_A, list_A, list_B)
    # phần 2 đi đường zig-zag từ điểm xa drone nhất về điểm gần drone thứ 2

    # Assuming list_2 and point_A are defined
    # tìm đường zig-zag ngắn nhất cho phần đường đi thứ 2
    path_list_2 = find_shortest_path(point_A, list_B.copy())

    list_A.pop()  # bỏ đi điểm cuối cùng của phần thứ nhất vì trùng với điểm đầu phần thứ 2
    list_A.extend(path_list_2)  # nối 2 phần

    return list_A
