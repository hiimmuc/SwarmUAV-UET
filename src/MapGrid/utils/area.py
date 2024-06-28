import tkinter as tk
def shoelace_area(x_coords, y_coords):
    n = len(x_coords)
    if n != len(y_coords) or n < 3:
        return None  

    area = 0.0
    for i in range(n - 1):
        area += x_coords[i] * y_coords[i + 1] - x_coords[i + 1] * y_coords[i]

    area += x_coords[n - 1] * y_coords[0] - x_coords[0] * y_coords[n - 1]

    return abs(area) / 2.0

def draw_polygon(canvas, x_coords, y_coords):
    n = len(x_coords)
    for i in range(n):
        x1, y1 = x_coords[i] + 400, 300 - y_coords[i] 
        x2, y2 = x_coords[(i + 1) % n] + 400, 300 - y_coords[(i + 1) % n]
        canvas.create_line(x1, y1, x2, y2, fill="red") 
        canvas.create_text(x1, y1, text=f"({x_coords[i]}, {y_coords[i]})", anchor=tk.SE, font=("Arial", 8))

def calculate_area_and_display(x_coords, y_coords, label):
    area = shoelace_area(x_coords, y_coords)
    if area is not None:
        label.config(text=f"Diện tích của đa giác là: {area}")
    else:
        label.config(text="Không thể tính diện tích. Hãy đảm bảo nhập đủ điểm và số lượng điểm ít nhất là 3.")

def is_point_inside_polygon(x, y, x_coords, y_coords):
    n = len(x_coords)
    inside = False
    p1x, p1y = x_coords[0], y_coords[0]
    for i in range(n + 1):
        p2x, p2y = x_coords[i % n], y_coords[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside