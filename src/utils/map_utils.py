import datetime
import io
import json
import json as json_module
import os
from collections import namedtuple

import decorator
import folium
import folium.plugins
from folium.plugins import MarkerCluster
from folium.plugins.draw import Draw
from folium.raster_layers import TileLayer
from PyQt5 import QtCore, QtWebEngineWidgets, QtWidgets
from PyQt5.QtCore import QFile, QUrl, pyqtSlot
from PyQt5.QtNetwork import QNetworkDiskCache
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineProfile, QWebEngineScript, QWebEngineView
from PyQt5.QtWidgets import QApplication

QtCore.qInstallMessageHandler(lambda *args: None)
NOW = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def geojson_to_coordinates(geojson) -> str:
    if type(geojson) is str:
        geojson = json.loads(geojson)
    else:
        geojson = geojson

    geometry_type = geojson.get("geometry", {}).get("type", "")
    coordinates = geojson.get("geometry", {}).get("coordinates", [])

    if len(coordinates) == 0:
        print("No coordinates found in GeoJSON")
        return []

    return [geometry_type, coordinates]


class MapEngine(QWebEngineView):
    # marker events
    @pyqtSlot(str, float, float)
    def markerMoved(self, key, latitude, longitude):
        self.markerMovedCallback(key, latitude, longitude)

    @pyqtSlot(str, float, float)
    def markerRightClicked(self, key, latitude, longitude):
        self.markerRightClickedCallback(key, latitude, longitude)

    @pyqtSlot(str, float, float)
    def markerClicked(self, key, latitude, longitude):
        self.markerClickedCallback(key, latitude, longitude)

    @pyqtSlot(str, float, float)
    def markerDoubleClicked(self, key, latitude, longitude):
        self.markerDoubleClickedCallback(key, latitude, longitude)

    # map events
    @pyqtSlot(float, float)
    def mapMoved(self, latitude, longitude):
        self.mapMovedCallback(latitude, longitude)

    @pyqtSlot(float, float)
    def mapRightClicked(self, latitude, longitude):
        self.mapRightClickedCallback(latitude, longitude)

    @pyqtSlot(float, float)
    def mapClicked(self, latitude, longitude):
        self.mapClickedCallback(latitude, longitude)

    @pyqtSlot(float, float)
    def mapDoubleClicked(self, latitude, longitude):
        self.mapDoubleClickedCallback(latitude, longitude)

    # drawn events
    @pyqtSlot(str)
    def geoJsonHandle(self, geojson):
        self.mapGeojsonCallback(geojson)

    def __init__(self, widget=None):
        super().__init__(parent=widget)

        cache = QNetworkDiskCache()
        cache.setCacheDirectory("cache")

        self.initialized = False

        self.map_widget = widget
        self.map_page = self.map_widget.page()
        # self.map_widget.getSettings().setJavaScriptEnabled(true)
        web_channel = QWebChannel(self.map_page)
        self.map_page.setWebChannel(web_channel)
        web_channel.registerObject("qtWidget", self)

        self.loadFinished.connect(self.onLoadFinished)
        # set callback to transfer data from JS to Python
        self.mapMovedCallback = None
        self.mapClickedCallback = None
        self.mapRightClickedCallback = None
        self.mapDoubleClickedCallback = None

        self.markerMovedCallback = None
        self.markerClickedCallback = None
        self.markerDoubleClickedCallback = None
        self.markerRightClickedCallback = None

        self.mapGeojsonCallback = None

    def onLoadFinished(self, ok):
        if self.initialized:
            return

        if not ok:
            print("Error initializing Map")

        self.initialized = True

    def waitUntilReady(self):
        while not self.initialized:
            QApplication.processEvents()

    def runScript(self, script):
        return self.map_page.runJavaScript(script)

    def centerAt(self, latitude, longitude):
        self.runScript("setCenterJs({}, {})".format(latitude, longitude))

    def setZoom(self, zoom):
        self.runScript("setZoomJs({})".format(zoom))

    def center(self):
        center = self.runScript("getCenterJs()")
        return center["lat"], center["lng"]

    def addMarker(self, key, latitude, longitude):
        return self.runScript(
            f"addMarkerJs(key={key}, latitude={latitude}, longitude={longitude})"
        )

    def mapMoveMarker(self, key, latitude, longitude):
        self.runScript(f"moveMarkerJs(key={key}, latitude={latitude}, longitude={longitude})")

    def positionMarker(self, key):
        return tuple(self.runScript("posMarker(key={!r});".format(key)))

    def drawGeoJson(self, geojson):
        return self.runScript(f"drawGeoJsonJs({geojson})")


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


class MapFolium:
    def __init__(self, location: list = [0, 0], zoom_start: int = 10):
        self._init_map(location, zoom_start)
        self._init_plugins()
        self.maker_cluster = MarkerCluster(
            name="1000 clustered icons", overlay=True, control=False, icon_create_function=None
        )

    def _init_map(self, location: list, zoom_start: int) -> None:
        self.m = folium.Map(
            tiles=None,
            location=location,
            zoom_start=zoom_start,
            prefer_canvas=True,
            zoom_control=False,
        )

        for title in titles[::-1]:
            title.add_to(self.m)

        folium.LayerControl().add_to(self.m)

    def _init_plugins(self):
        #! Disabled
        # folium.plugins.Draw(
        #     export=False,
        #     filename=f"data_{NOW}.geojson",
        #     position="topleft",
        #     draw_options={
        #         "polygon": {
        #             "shapeOptions": {
        #                 "color": "rgb(0% 98.576% 15.974%)",
        #                 "fillColor": "#6bc2e5",
        #                 "fillOpacity": 0.5,
        #             },
        #             "drawError": {"color": "#dd253b", "timeout": 1000, "message": "Oups!"},
        #             "allowIntersection": False,
        #             "showArea": True,
        #             "metric": True,
        #             "repeatMode": True,
        #             "marker": True,
        #         },
        #         "polyline": {
        #             "shapeOptions": {
        #                 "color": "red",
        #             },
        #             "marker": True,
        #         },
        #         "rectangle": {
        #             "shapeOptions": {
        #                 "color": "#6bc2e5",
        #             }
        #         },
        #         "circle": False,
        #         "circlemarker": False,
        #     },
        #     edit_options={"poly": {"allowIntersection": False}},
        # ).add_to(self.m)

        # geo-coder plugin
        folium.plugins.Geocoder().add_to(self.m)

        # Measure control
        folium.plugins.MeasureControl().add_to(self.m)

        #! Disabled
        # full-screen plugin
        # folium.plugins.Fullscreen(
        #     position="topright",
        #     title="Expand me",
        #     title_cancel="Exit me",
        #     force_separate_button=True,
        # ).add_to(self.m)

        # Minimap
        folium.plugins.MiniMap(tile_layer=titles[1]).add_to(self.m)

        #! Disabled
        # mouse position
        # folium.plugins.MousePosition().add_to(self.m)

    def _save_map(self, path: str) -> None:
        self.m.save(path, close_file=False)

    def center_to(self, latitude: float, longitude: float) -> None:
        self.m.location = [latitude, longitude]
        # self._save_map("src/data/map.html")
        return self.render_map()

    def add_marker(
        self, key: str, latitude: float, longitude: float, tooltip=None, icon=None
    ) -> None:
        print("Adding", key, latitude, longitude)
        print(type(longitude), type(latitude))
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
        # self._save_map("src/data/map.html")
        return self.render_map()

    def add_line(
        self,
        key: str,
        points: list,
    ) -> None:
        print("Adding", key, points)
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
        # self._save_map("src/data/map.html")
        return self.render_map()

    def add_polygon(self, key: str, points: list) -> None:
        # draw edges
        print("Adding", key, points)
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
        # self._save_map("src/data/map.html")
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
    m._save_map("src/data/map.html")
