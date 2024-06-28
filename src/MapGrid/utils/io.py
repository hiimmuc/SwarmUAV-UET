import tkinter as tk
from tkinter import filedialog
def read_points_from_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            x_coords = []
            y_coords = []
            for line in lines:
                x, y = map(float, line.strip().split())
                x_coords.append(x)
                y_coords.append(y)
            return x_coords, y_coords
    except FileNotFoundError:
        return None, None

def write_points_to_file(filename, grid_points):
    """
    Ghi các tọa độ của các điểm vào một tệp văn bản.
    :param filename: Tên tệp để ghi vào
    :param grid_points: Danh sách các điểm lưới giao nhau trong đa giác
    """
    try:
        with open(filename, 'w') as file:
            for x, y in grid_points:
                file.write(f"{x} {y}\n")
    except Exception as e:
        print(f"Error writing points to file: {e}")