import io
import json
import json as json_module
import os
from collections import namedtuple

import decorator
import folium
from folium.plugins.draw import Draw
from folium.raster_layers import TileLayer
from PyQt5 import QtCore, QtWebEngineWidgets, QtWidgets
from PyQt5.QtCore import QFile, QUrl, pyqtSlot
from PyQt5.QtNetwork import QNetworkDiskCache
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineProfile, QWebEngineScript, QWebEngineView
from PyQt5.QtWidgets import QApplication

QtCore.qInstallMessageHandler(lambda *args: None)


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

    #


def load_map(location=[21.064862, 105.792958]) -> None:
    titles = TileLayer(
        tiles="http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}",
        attr="google",
        name="google",
        max_zoom=20,
        subdomains=["mt0", "mt1", "mt2", "mt3"],
    )
    m = folium.Map(
        tiles=titles,
        location=location,
        zoom_start=16,
    )
    Draw(
        export=True,
        filename="./logs/data.geojson",
        position="topright",
        draw_options={
            "polygon": {
                "shapeOptions": {
                    "color": "#6bc2e5",
                    "fillColor": "#6bc2e5",
                    "fillOpacity": 0.5,
                },
                "drawError": {"color": "#dd253b", "timeout": 1000, "message": "Oups!"},
                "allowIntersection": False,
                "showArea": True,
                "metric": True,
                "repeatMode": True,
            },
            "polyline": {
                "shapeOptions": {
                    "color": "red",
                }
            },
            "rectangle": {
                "shapeOptions": {
                    "color": "#6bc2e5",
                }
            },
            "circle": False,
            "circlemarker": False,
        },
        edit_options={"poly": {"allowIntersection": False}},
    ).add_to(m)
    data = io.BytesIO()
    m.save(data, close_file=False)
    return data.getvalue().decode()
