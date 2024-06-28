import tkinter as tk
from tkinter import filedialog
from .utils.area import shoelace_area, draw_polygon, calculate_area_and_display, is_point_inside_polygon
from .utils.io import read_points_from_file, write_points_to_file


def main():
    root = tk.Tk()
    root.title("Vẽ Đa Giác và Tính Diện Tích")
    root.geometry("800x600")

    canvas = tk.Canvas(root, width=800, height=600, bg="white")
    canvas.pack(pady=10)

    x_coords = []
    y_coords = []
    grid_enabled = False

    def add_point():
        x = float(entry_x.get())
        y = float(entry_y.get())
        x_coords.append(x)
        y_coords.append(y)
        canvas.create_oval(x + 398, 302 - y, x + 402, 298 - y, fill="red")
        entry_x.delete(0, tk.END)
        entry_y.delete(0, tk.END)
        label_coords.config(text=f"Tọa độ các điểm: {
                            list(zip(x_coords, y_coords))}")

        if len(x_coords) >= 3:
            btn_calculate.config(state=tk.NORMAL)
            calculate_area_and_display(x_coords, y_coords, label_area)

        canvas.delete("polygon")
        draw_polygon(canvas, x_coords, y_coords)

    def clear_last_point():
        if x_coords and y_coords:
            x_coords.pop()
            y_coords.pop()
            canvas.delete("all")
            draw_polygon(canvas, x_coords, y_coords)
            label_coords.config(text=f"Tọa độ các điểm: {
                                list(zip(x_coords, y_coords))}")
            if len(x_coords) < 3:
                btn_calculate.config(state=tk.DISABLED)
                label_area.config(text="")

    def open_file():
        filename = filedialog.askopenfilename(
            initialdir="./", title="Chọn file", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            x_coords_file, y_coords_file = read_points_from_file(filename)
            if x_coords_file and y_coords_file:
                x_coords.extend(x_coords_file)
                y_coords.extend(y_coords_file)
                for x, y in zip(x_coords_file, y_coords_file):
                    canvas.create_oval(x + 398, 302 - y, x +
                                       402, 298 - y, fill="red")
                label_coords.config(text=f"Tọa độ các điểm: {
                                    list(zip(x_coords, y_coords))}")
                if len(x_coords) >= 3:
                    btn_calculate.config(state=tk.NORMAL)
                    calculate_area_and_display(x_coords, y_coords, label_area)
                canvas.delete("polygon")
                draw_polygon(canvas, x_coords, y_coords)

    def toggle_grid():
        nonlocal grid_enabled
        distance = float(entry_grid_distance.get())
        if grid_enabled:
            canvas.delete("grid")
            grid_enabled = False
        else:
            for x in range(-400, 400, int(distance)):
                for y in range(-300, 300, int(distance)):
                    if is_point_inside_polygon(x, y, x_coords, y_coords):
                        canvas.create_oval(
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

    tk.Label(frame_input, text="X:").grid(row=0, column=0)
    entry_x = tk.Entry(frame_input)
    entry_x.grid(row=0, column=1)

    tk.Label(frame_input, text="Y:").grid(row=0, column=2)
    entry_y = tk.Entry(frame_input)
    entry_y.grid(row=0, column=3)

    btn_add_point = tk.Button(frame_input, text="Thêm Điểm", command=add_point)
    btn_add_point.grid(row=0, column=4, padx=10)

    btn_clear_last_point = tk.Button(
        frame_input, text="Xóa Điểm Trước Đó", command=clear_last_point)
    btn_clear_last_point.grid(row=0, column=5, padx=10)

    btn_open_file = tk.Button(frame_input, text="Mở File", command=open_file)
    btn_open_file.grid(row=0, column=6, padx=10)

    label_coords = tk.Label(root, text="")
    label_coords.pack()

    def clear_canvas():
        canvas.delete("all")
        del x_coords[:]
        del y_coords[:]
        label_coords.config(text="")
        label_area.config(text="")
        btn_calculate.config(state=tk.DISABLED)

    btn_clear = tk.Button(root, text="Xóa Đa Giác", command=clear_canvas)
    btn_clear.pack(pady=5)

    btn_calculate = tk.Button(root, text="Tính Diện Tích", state=tk.DISABLED)
    btn_calculate.pack(pady=5)
    btn_calculate.config(command=lambda: calculate_area_and_display(
        x_coords, y_coords, label_area))

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
