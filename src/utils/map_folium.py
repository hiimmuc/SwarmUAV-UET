import io

import folium
from folium.plugins.draw import Draw
from folium.raster_layers import TileLayer

titles = TileLayer(
    tiles="http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}",
    attr="google",
    name="google",
    max_zoom=20,
    subdomains=["mt0", "mt1", "mt2", "mt3"],
)


class MapFolium:
    def __init__(self, location: list = [0, 0], zoom_start: int = 10):

        self.m = folium.Map(
            tiles=titles,
            location=location,
            zoom_start=zoom_start,
        )

    def _save_map(self, path: str) -> None:
        self.m.save(path)

    def add_marker(self, key: str, latitude: float, longitude: float) -> None:
        folium.Marker([latitude, longitude], popup=key).add_to(self.m)

    def add_polygon(self, key: str, points: list) -> None:
        folium.Polygon(points, popup=key).add_to(self.m)

    def render_map(self) -> None:
        data = io.BytesIO()
        self.m.save(data, close_file=False)
        return data.getvalue().decode()
