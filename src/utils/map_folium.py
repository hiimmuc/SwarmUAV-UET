import io
from datetime import datetime
from pathlib import Path

import folium
import folium.plugins
from folium import CustomIcon, Map, Marker
from folium.elements import MacroElement
from folium.plugins import MarkerCluster
from folium.plugins.draw import Draw
from folium.raster_layers import TileLayer
from jinja2 import Template

NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
_src_path = Path(__file__).resolve().parent.parent

ICON_DIR = Path(__file__).parent.parent / "assets" / "icons"
drone_icon_path = ICON_DIR / "drone.png"

titles = [
    TileLayer(
        tiles="http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}",
        attr="google",
        name="google-hybrid",
        max_zoom=20,
        subdomains=["mt0", "mt1", "mt2", "mt3"],
    ),
    TileLayer(
        tiles="http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
        attr="google",
        name="google-streets",
        max_zoom=20,
        subdomains=["mt0", "mt1", "mt2", "mt3"],
    ),
    TileLayer(
        tiles="http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        attr="google",
        name="google-satellite",
        max_zoom=20,
        subdomains=["mt0", "mt1", "mt2", "mt3"],
    ),
    TileLayer(
        tiles="http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}",
        attr="google",
        name="google-terrain",
        max_zoom=20,
        subdomains=["mt0", "mt1", "mt2", "mt3"],
    ),
    TileLayer(
        tiles="http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        attr="osm",
        name="osm",
        max_zoom=20,
        subdomains=["a", "b", "c"],
    ),
]

ICON = {
    "plane": folium.plugins.BeautifyIcon(
        icon="plane", border_color="#b3334f", text_color="#b3334f", icon_shape="triangle"
    ),
    "number": lambda x: folium.plugins.BeautifyIcon(
        border_color="#00ABDC",
        text_color="#00ABDC",
        number=x,
        inner_icon_style="margin-top:0;",
    ),
}

# cSpell: ignore folium, geojson, lon, lat, polyline, polygon, circlemarker, circlemarker, Geocoder, bottomleft, topright


class UpdateMarkerJs(MacroElement):
    _template = Template(
        """
        <script>
            // JavaScript code to update markers
            let droneMarkers = {};

            function updateUAVMarkerovv(id, latitude, longitude) {
                if (droneMarkers[id]) {
                    droneMarkers[id].setLatLng([latitude, longitude]);
                } else {
                    droneMarkers[id] = L.marker([latitude, longitude], {
                        icon: L.icon({
                            iconUrl: '/home/hansen/Documents/SwarmUAV-UET/assets/icons/drone.png',  // Update the icon path
                            iconSize: [32, 32]  // Adjust as necessary
                        })
                    }).addTo(map);
                }
            }
        </script>
    """
    )


class MapFolium:
    def __init__(
        self,
        location: list = [0, 0],
        zoom_start: int = 10,
        plugins: list = ["Draw", "Geocoder", "MeasureControl", "MiniMap"],
    ):
        self.plugins = plugins
        self._init_map(location, zoom_start)
        self._init_plugins()
        self.maker_cluster = MarkerCluster(
            name="1000 clustered icons", overlay=True, control=False, icon_create_function=None
        )

    def _init_map(self, location: list, zoom_start: int) -> None:
        self.m = folium.Map(
            tiles=titles[0],
            location=location,
            zoom_start=zoom_start,
            prefer_canvas=True,
            zoom_control=False,
        )
        # Add your custom JavaScript code
        self.m.get_root().add_child(UpdateMarkerJs())

        # self.m.default_js.append(("qtwebchannel", "src/utils/qwebchannel.js"))

        folium.LayerControl().add_to(self.m)

    def _init_plugins(self):
        if "Draw" in self.plugins:
            drawer = Draw(
                export=False,
                filename=f"data_{NOW}.geojson",
                position="topright",
                draw_options={
                    "polygon": {
                        "shapeOptions": {
                            "color": "rgb(0% 98.576% 15.974%)",
                            "fillColor": "#6bc2e5",
                            "fillOpacity": 0.5,
                        },
                        "drawError": {"color": "#dd253b", "timeout": 1000, "message": "Oops!"},
                        "allowIntersection": False,
                        "showArea": True,
                        "metric": True,
                        "repeatMode": True,
                        "marker": True,
                    },
                    "polyline": {
                        "shapeOptions": {
                            "color": "red",
                        },
                        "marker": True,
                    },
                    "rectangle": {
                        "shapeOptions": {
                            "color": "#6bc2e5",
                        }
                    },
                    "circle": False,
                    "circlemarker": False,
                },
                edit_options={"poly": {"allowIntersction": False}},
            ).add_to(self.m)

            # with open(f"src/utils/template_draw.js", "r") as f:
            #     template = f.read()

            # drawer._template = Template(template)

            # self.m.add_child(drawer)

        # geo-coder plugin
        if "Geocoder" in self.plugins:
            folium.plugins.Geocoder().add_to(self.m)

        # Measure control
        if "MeasureControl" in self.plugins:
            folium.plugins.MeasureControl().add_to(self.m)

        # Minimap
        if "MiniMap" in self.plugins:
            folium.plugins.MiniMap(tile_layer=titles[1]).add_to(self.m)

        # mouse position
        folium.plugins.MousePosition(
            position="bottomleft",
            separator="<br />",
            empty_string="",
            lng_first=False,
            num_digits=10,
        ).add_to(self.m)

    def _save_map(self, path: str) -> None:
        self.m.save(path, close_file=False)

    def center_to(self, latitude: float, longitude: float) -> None:
        self.m.location = [latitude, longitude]

        return self.render_map()

    # def add_marker(
    #     self, key: str, latitude: float, longitude: float, tooltip=None, icon=None
    # ) -> None:
    #     marker = folium.Marker(
    #         location=[latitude, longitude],
    #         popup=None,
    #         tooltip=tooltip,
    #         icon=folium.Icon(color=icon["color"], icon=icon["icon"], prefix="fa"),
    #         draggable=False,
    #     )
    #     popup = "{}<br>lat:{}<br>lon:{}".format(key, latitude, longitude)
    #     folium.Popup(popup, show=True).add_to(marker)

    #     self.maker_cluster.add_child(marker)
    #     self.maker_cluster.add_to(self.m)

    #     return self.render_map()

    def add_marker(
        self, key: str, latitude: float, longitude: float, tooltip=None, icon=None
    ) -> None:
        # print("Adding", key, latitude, longitude)
        # print(type(longitude), type(latitude))

        # Use a custom icon if a file path is provided
        if icon and "icon_path" in icon:
            # Convert the icon path to a string to avoid PosixPath issues
            icon_path = str(icon["icon_path"])  # Convert PosixPath to string
            custom_icon = CustomIcon(
                icon_image=icon_path,  # Path to the custom icon image
                icon_size=(32, 32),  # Adjust the size as needed
            )
            marker = folium.Marker(
                location=[latitude, longitude],
                popup=None,
                tooltip=tooltip,
                icon=custom_icon,
                draggable=False,
            )
        else:
            # Fallback to default Folium Icon if no custom icon path is specified
            marker = folium.Marker(
                location=[latitude, longitude],
                popup=None,
                tooltip=tooltip,
                icon=folium.Icon(color=icon["color"], icon=icon["icon"], prefix="fa"),
                draggable=False,
            )

        popup = "{}<br>lat:{}<br>lon:{}".format(key, latitude, longitude)
        folium.Popup(popup, show=True).add_to(marker)

        self.maker_cluster.add_child(marker)
        self.maker_cluster.add_to(self.m)
        return self.render_map()

    def add_line(
        self,
        key: str,
        points: list,
    ) -> None:

        for point in points:
            folium.CircleMarker(
                location=point,
                radius=5,
                color="red",
                stroke=False,
                fill=True,
                fill_opacity=0.8,
                opacity=1,
            ).add_to(self.m)

        folium.PolyLine(
            points,
            color="#FF0000",
            weight=3,
        ).add_to(self.m)

        return self.render_map()

    def add_polygon(self, key: str, points: list) -> None:
        # draw edges

        for point in points:
            folium.Marker(
                location=point,
                color="green",
                icon=folium.Icon(color="green", icon="map-pin", prefix="fa"),
            ).add_to(self.m)
        # draw polygon
        folium.Polygon(
            locations=points,
            color="rgb(0% 98.576% 15.974%)",
            weight=6,
            fill_color="#6bc2e5",
            fill_opacity=0.5,
            fill=True,
        ).add_to(self.m)

        return self.render_map()

    def render_map(self) -> None:
        data = io.BytesIO()
        self.m.save(data, close_file=False)
        return data.getvalue().decode()


if __name__ == "__main__":
    m = MapFolium(location=[0, 0], zoom_start=16)
    m.center_to(*[21.064862, 105.792958])
    m.add_marker("Hanoi", 21.064862, 105.792958, icon={"color": "blue", "icon": "1"})
    m.add_line("Hanoi", [[21.064966, 105.795968], [21.064863, 105.793959]])
    m.add_polygon(
        "Hanoi",
        [
            [21.05940, 105.79529],
            [21.05940, 105.79929],
            [21.05725, 105.79714],
            [21.05719, 105.79516],
        ],
    )
    m._save_map(f"{_src_path}/data/map_current.html")
