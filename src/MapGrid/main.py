import tkinter as tk
from tkinter import filedialog
from utils.area import shoelace_area, draw_polygon, calculate_area_and_display, is_point_inside_polygon
from utils.io import read_points_from_file, write_points_to_file
import tkinter
import tkintermapview
from tkintermapview import TkinterMapView
import geopandas as gpd
from pyproj import Geod
from scipy.spatial import ConvexHull


class GeoPosition:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"({self.latitude}, {self.longitude})"


def main():
    root = tkinter.Tk()
    root.title("Vẽ Đa Giác và Tính Diện Tích")
    root.geometry("800x600")

    map_widget = tkintermapview.TkinterMapView(
        root, width=1200, height=550, corner_radius=0)
    map_widget.set_address("dai hoc quoc gia, hanoi, vietnam")
    map_widget.pack(pady=10)

    x_coords = []
    y_coords = []
    grid_enabled = False
    position_list = []  # danh sach diem
    print_point_list = []  # danh sach diem
    marker_list = []  # danh sach marker
    number = 0  # dem so diem
    polygon_list = []
    path_list = []

    def left_click_event(coordinates_tuple):
        nonlocal number
        print("Left click event with coordinates:", coordinates_tuple)
        number += 1
        latitude, longitude = coordinates_tuple
        # This creates a marker on the map widget
        marker_list.append(map_widget.set_marker(
            latitude, longitude, text="Diem " + str(number)))  # tao marker
        # them diem vao danh sach
        print_point_list.append(GeoPosition(latitude, longitude))
        position_list.append([latitude, longitude])  # them diem vao danh sach
        print(f"Marker set at latitude: {latitude}, longitude: {longitude}")
        print(f"Point {number} set at latitude: {
              latitude}, longitude: {longitude}")

        label_coords.config(text=f"Tọa độ các điểm: {position_list}")

    def open_file():
        nonlocal number
        filename = filedialog.askopenfilename(initialdir="./", title="Chọn file",
                                              filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            x_coords_file, y_coords_file = read_points_from_file(filename)
            if x_coords_file and y_coords_file:
                x_coords.extend(x_coords_file)
                y_coords.extend(y_coords_file)
            n = len(x_coords)
            for x, y in zip(x_coords, y_coords):
                number += 1
                marker_list.append(map_widget.set_marker(
                    x, y, text="Diem " + str(number)))  # tao marker
                # them diem vao danh sach
                print_point_list.append(GeoPosition(x, y))
                position_list.append([x, y])  # them diem vao danh sach
                print(f"Marker set at latitude: {x}, longitude: {y}")
                for index, position in enumerate(print_point_list):
                    print(f"Point {
                          index + 1} set at latitude: {position.latitude}, longitude: {position.longitude}")

            label_coords.config(text="")
            label_coords.config(text=f"Tọa độ các điểm: {position_list}")

    def export_file():
        filename = filedialog.asksaveasfilename(defaultextension=".txt", title="Lưu file",
                                                filetypes=(("Text files", "*.txt"), ("All files", "*.*")))

        if position_list[0] != position_list[-1]:
            position_list.append(position_list[0])

        if filename:
            try:
                with open(filename, 'w') as file:
                    for position in position_list:
                        file.write(f"{position[0]} {position[1]}\n")
            except Exception as e:
                print(f"Error writing positions to file: {e}")

    def add_point():
        nonlocal number
        number += 1
        x = float(entry_x.get())
        y = float(entry_y.get())
        marker_list.append(map_widget.set_marker(
            x, y, text="Diem " + str(number)))  # tao marker
        position_list.append([x, y])  # them diem vao danh sach
        new_marker = map_widget.set_marker(x, y, text="Diem" + str(number))
        marker_list.append(new_marker)
        entry_x.delete(0, tk.END)
        entry_y.delete(0, tk.END)
        label_coords.config(text="")
        label_coords.config(text=f"Tọa độ các điểm: {position_list}")

    def add_polygon():
        print(f"POLYGON: ")
        polygon_list.append(map_widget.set_polygon(position_list))
        for index, position in enumerate(position_list):
            print(
                f"Point {index + 1} set at latitude: {position[0]}, longitude: {position[1]}")

    def add_path():
        path_list.append(map_widget.set_path(position_list))

    def clear_path():
        path_1 = path_list.pop()
        path_1.delete()

    def clear_polygon():
        polygon1 = polygon_list.pop()
        polygon1.delete()
        print(f"Polygon deleted\n")

    def clear_last_point():
        nonlocal number
        position_list.pop()
        print_point_list.pop()
        removed_marker = marker_list.pop()
        removed_marker.delete()
        number -= 1
        label_coords.config(text="")
        label_coords.config(text=f"Tọa độ các điểm: {position_list}")
        if number < 1:
            print(f"All point deleted\n")

    def calculate_geographic_area(position_list):
        geod = Geod(ellps='WGS84')

        if position_list[0] != position_list[-1]:
            position_list.append(position_list[0])

        # Ensure positions form a valid polygon
        if len(position_list) < 4 or position_list[0] != position_list[-1]:
            print("Polygon is not closed or has insufficient points.")
            return None

        # Ensure order is longitude, latitude for pyproj
        lon, lat = zip(*[(lon, lat) for lat, lon in position_list])

        try:
            area, _ = geod.polygon_area_perimeter(lon, lat)
            return abs(area)
        except Exception as e:
            print(f"Failed to calculate area: {e}")
            return None

    def calculate_area_and_display(label):
        area_m2 = calculate_geographic_area(position_list)
        if area_m2 is not None:
            label.config(text=f"Diện tích của đa giác là: {
                         area_m2:.2f} square meters")
        else:
            label.config(
                text="Không thể tính diện tích. Hãy đảm bảo nhập đủ điểm và số lượng điểm ít nhất là 3.")

    def toggle_grid():
        nonlocal grid_enabled
        distance = float(entry_grid_distance.get())
        if grid_enabled:
            map_widget.delete("grid")
            grid_enabled = False
        else:
            for x in range(-400, 400, int(distance)):
                for y in range(-300, 300, int(distance)):
                    if is_point_inside_polygon(x, y, x_coords, y_coords):
                        map_widget.create_oval(
                            x + 398, 302 - y, x + 402, 298 - y, fill="blue")
            grid_enabled = True

    def export_grid_points():
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(
            ("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            grid_points = []
            distance = float(entry_grid_distance.get())
            for x in range(-400, 400, int(distance)):
                for y in range(-300, 300, int(distance)):
                    if is_point_inside_polygon(x, y, x_coords, y_coords):
                        grid_points.append((x, y))
            write_points_to_file(filename, grid_points)

    frame_input = tk.Frame(root)
    frame_input.pack()

    map_widget.add_left_click_map_command(left_click_event)

    tk.Label(frame_input, text="X:").grid(row=0, column=0)
    entry_x = tk.Entry(frame_input)
    entry_x.grid(row=0, column=1)

    tk.Label(frame_input, text="Y:").grid(row=0, column=2)
    entry_y = tk.Entry(frame_input)
    entry_y.grid(row=0, column=3)

    btn_add_point = tk.Button(frame_input, text="Thêm Điểm")
    btn_add_point.grid(row=0, column=4, padx=10)

    btn_clear_last_point = tk.Button(
        frame_input, text="Xóa Điểm Trước Đó", command=clear_last_point)
    btn_clear_last_point.grid(row=0, column=5, padx=10)

    btn_open_file = tk.Button(frame_input, text="Mở File", command=open_file)
    btn_open_file.grid(row=0, column=6, padx=10)

    btn_open_file = tk.Button(
        frame_input, text="Xuất File", command=export_file)
    btn_open_file.grid(row=0, column=7, padx=10)

    label_coords = tk.Label(root, text="")
    label_coords.pack()

    btn_create_polygon = tk.Button(
        frame_input, text="Tạo đa giác", command=add_polygon)
    btn_create_polygon.grid(row=2, column=5, padx=10)

    btn_create_path = tk.Button(
        frame_input, text="Tạo đường đi", command=add_path)
    btn_create_path.grid(row=2, column=6, padx=10)

    btn_create_path = tk.Button(
        frame_input, text="Xóa đường đi", command=clear_path)
    btn_create_path.grid(row=2, column=7, padx=10)

    btn_clear = tk.Button(root, text="Xóa Đa Giác", command=clear_polygon)
    btn_clear.pack(pady=5)

    btn_add_point = tk.Button(frame_input, text="Thêm Điểm", command=add_point)
    btn_add_point.grid(row=0, column=4, padx=10)

    btn_calculate = tk.Button(root, text="Tính Diện Tích")
    btn_calculate.pack(pady=5)
    btn_calculate.config(
        command=lambda: calculate_area_and_display(label_area))

    label_area = tk.Label(root, text="")
    label_area.pack()

    frame_grid = tk.Frame(root)
    frame_grid.pack(pady=5)

    tk.Label(frame_grid, text="Khoảng cách lưới:").grid(row=0, column=0)
    entry_grid_distance = tk.Entry(frame_grid)
    entry_grid_distance.grid(row=0, column=1)

    btn_toggle_grid = tk.Button(
        frame_grid, text="Bật/Tắt Lưới", command=toggle_grid)
    btn_toggle_grid.grid(row=0, column=2, padx=10)

    btn_export_grid_points = tk.Button(
        frame_grid, text="Xuất Điểm Lưới", command=export_grid_points)
    btn_export_grid_points.grid(row=0, column=3, padx=10)

    root.mainloop()


if __name__ == "__main__":
    main()
