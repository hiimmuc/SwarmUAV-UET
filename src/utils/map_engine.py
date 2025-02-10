"""DOCS:
# Sample code to add markers and lines to the map
# Add markers to the map
map_engine.addMarker(
    key="1",
    latitude=21.064862,
    longitude=105.792958,
    **dict(icon="../assets/icons/drone.png", draggable=True, title="1"),
)

# Add lines to the map
map_engine.drawPolyLine(
    key="1",
    coordinates=[
        [21.064862, 105.792958], # p1
        [21.065862, 105.792958], # p2
    ],
    options=dict(color="red", weight=5),
)

# Add polygons to the map
map_engine.drawPolygon(
    key="1",
    coordinates=[
        [21.064862, 105.792958], # p1
        [21.065862, 105.792958], # p2
        [21.065862, 105.793958], # p3
        [21.064862, 105.793958], # p4
    ],
    options=dict(color="green", weight=2, fill=True, fillColor="green", fillOpacity=0.2),
)
"""

import json
from typing import List, Optional, Sequence, Union

import decorator
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl, pyqtSlot
from PyQt5.QtNetwork import QNetworkDiskCache
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.QtWidgets import QApplication

QtCore.qInstallMessageHandler(lambda *args: None)

doTrace = False


@decorator.decorator
def trace(function, *args, **k):
    """Decorates a function by tracing the beginning and
    end of the function execution, if doTrace global is True"""

    if doTrace:
        print("> " + function.__name__, args, k)
    result = function(*args, **k)
    if doTrace:
        print("< " + function.__name__, args, k, "->", result)
    return result


class _LoggedPage(QWebEnginePage):
    @trace
    def javaScriptConsoleMessage(self, msg, line, source):
        print("JS: %s line %d: %s" % (source, line, msg))


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
    def mapLeftClicked(self, latitude, longitude):
        self.mapClickedCallback(latitude, longitude)

    @pyqtSlot(float, float)
    def mapDoubleClicked(self, latitude, longitude):
        self.mapDoubleClickedCallback(latitude, longitude)

    # drawn events
    @pyqtSlot(str)
    def geoJsonHandle(self, geojson):
        self.mapGeojsonCallback(geojson)

    def __init__(
        self,
        name="",
        widget=None,
        url=None,
    ):
        QWebEngineView.__init__(self, parent=widget.parent())

        cache = QNetworkDiskCache()
        cache.setCacheDirectory("cache")

        self.initialized = False

        self.map_name = name
        self.map_widget = widget

        if url is not None:
            self.map_widget.load(QUrl(url))

        self.map_page = self.map_widget.page()
        # self.map_widget.getSettings().setJavaScriptEnabled(true)
        web_channel = QWebChannel(self.map_page)
        self.map_page.setWebChannel(web_channel)
        web_channel.registerObject("qtWidget", self)

        self.map_widget.loadFinished.connect(self.onLoadFinished)

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
        print("Map engine initialized for:", self.map_name)

    def waitUntilReady(self):
        while not self.initialized:
            QApplication.processEvents()

    def runScript(self, script):
        # print("Running script:", script)
        return self.map_page.runJavaScript(script)

    def centerAt(self, latitude, longitude):
        self.runScript("setCenterJs({}, {});".format(latitude, longitude))

    def setZoom(self, zoom):
        self.runScript("setZoomJs({});".format(zoom))

    def center(self):
        center = self.runScript("getCenterJs();")
        return center["lat"], center["lng"]

    # ============= Marker functions =============
    def addMarker(self, key, latitude, longitude, **options):
        return self.runScript(
            "addMarkerJs(key={!r},"
            "latitude= {}, "
            "longitude= {}, parameters={});".format(
                key, round(latitude, 12), round(longitude, 12), json.dumps(options)
            )
        )

    def deleteMarker(self, key):
        return self.runScript("deleteMarkerJs(key={!r});".format(key))

    def mapMoveMarker(self, key, latitude, longitude):
        self.runScript(f"moveMarkerJs(key={key}, latitude={latitude}, longitude={longitude});")

    def positionMarker(self, key):
        return tuple(self.runScript("posMarkerJs(key={!r});".format(key)))

    # ============= line functions =============
    def drawPolyLine(self, key, coordinates, options={}):
        if len(coordinates) < 2:
            print("PolyLine requires at least 2 coordinates")
            return

        options = path_options(line=True, **options)
        return self.runScript(
            "drawPolyLineJs(key = {!r}, coords={}, options={});".format(
                key, json.dumps(coordinates), json.dumps(options)
            )
        )

    def deletePolyLine(self, key):
        return self.runScript("deletePolyLineJs(key={!r});".format(key))

    # ============= polygon functions =============
    def drawPolygon(self, key, coordinates, options={}):
        if len(coordinates) < 3:
            print("Polygon requires at least 3 coordinates")
            return

        if coordinates[0] != coordinates[-1]:
            print("Polygon requires the first and last coordinates to be the same")
            return

        options = path_options(line=True, radius=None, fillcolor="#3388ff", **options)
        return self.runScript(
            "drawPolygonJs(key = {!r}, coords={}, options={});".format(
                key, json.dumps(coordinates), json.dumps(options)
            )
        )

    def deletePolygon(self, key):
        return self.runScript("deletePolygonJs(key={!r});".format(key))


#
def camelize(key: str) -> str:
    """Convert a python_style_variable_name to lowerCamelCase.

    Examples
    --------
    >>> camelize("variable_name")
    'variableName'
    >>> camelize("variableName")
    'variableName'
    """
    return "".join(x.capitalize() if i > 0 else x for i, x in enumerate(key.split("_")))


def marker_options(**kwargs) -> dict:
    """
    Contains options and constants shared between all markers.

    Parameters
    ----------
    draggable: Bool, False
        Whether the marker is draggable with mouse/touch or not.
    title: str, ''
        Text for the browser tooltip that appear on marker hover.
    iconSize: Dict(width, height), None
        The size of the icon image in pixels.
    """
    kwargs = {camelize(key): value for key, value in kwargs.items()}

    return {
        "icon": kwargs.pop("icon", "not_listed_location"),
        "draggable": kwargs.pop("draggable", False),
        "title": kwargs.pop("title", ""),
        "iconSize": kwargs.pop("iconSize", {"width": 10, "height": 10}),
    }


def path_options(line: bool = False, radius: Optional[float] = None, **kwargs) -> dict:
    """
    Contains options and constants shared between vector overlays
    (Polygon, Polyline, Circle, CircleMarker, and Rectangle).

    Parameters
    ----------
    stroke: Bool, True
        Whether to draw stroke along the path.
        Set it to false to disable borders on polygons or circles.
    color: str, '#3388ff'
        Stroke color.
    weight: int, 3
        Stroke width in pixels.
    opacity: float, 1.0
        Stroke opacity.
    line_cap: str, 'round' (lineCap)
        A string that defines shape to be used at the end of the stroke.
        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-linecap
    line_join: str, 'round' (lineJoin)
        A string that defines shape to be used at the corners of the stroke.
        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-linejoin
    dash_array: str, None (dashArray)
        A string that defines the stroke dash pattern.
        Doesn't work on Canvas-powered layers in some old browsers.
        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-dasharray
    dash_offset:, str, None (dashOffset)
        A string that defines the distance into the dash pattern to start the dash.
        Doesn't work on Canvas-powered layers in some old browsers.
        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-dashoffset
    fill: Bool, False
        Whether to fill the path with color.
        Set it to false to disable filling on polygons or circles.
    fill_color: str, default to `color` (fillColor)
        Fill color. Defaults to the value of the color option.
    fill_opacity: float, 0.2 (fillOpacity)
        Fill opacity.
    fill_rule: str, 'evenodd' (fillRule)
        A string that defines how the inside of a shape is determined.
        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill-rule
    bubbling_mouse_events: Bool, True (bubblingMouseEvents)
        When true a mouse event on this path will trigger the same event on the
        map (unless L.DomEvent.stopPropagation is used).
    gradient: bool, default None
        When a gradient on the stroke and fill is available,
        allows turning it on or off.

    Note that the presence of `fill_color` will override `fill=False`.

    This function accepts both snake_case and lowerCamelCase equivalents.

    See https://leafletjs.com/reference.html#path

    """

    kwargs = {camelize(key): value for key, value in kwargs.items()}

    extra_options = {}
    if line:
        extra_options = {
            "smoothFactor": kwargs.pop("smoothFactor", 1.0),
            "noClip": kwargs.pop("noClip", False),
        }
    if radius:
        extra_options.update({"radius": radius})

    color = kwargs.pop("color", "#3388ff")
    fill_color = kwargs.pop("fillColor", False)
    if fill_color:
        fill = True
    elif not fill_color:
        fill_color = color
        fill = kwargs.pop("fill", False)  # type: ignore

    gradient = kwargs.pop("gradient", None)
    if gradient is not None:
        extra_options.update({"gradient": gradient})

    if kwargs.get("tags"):
        extra_options["tags"] = kwargs.pop("tags")

    if kwargs.get("className"):
        extra_options["className"] = kwargs.pop("className")

    default = {
        "stroke": kwargs.pop("stroke", True),
        "color": color,
        "weight": kwargs.pop("weight", 3),
        "opacity": kwargs.pop("opacity", 1.0),
        "lineCap": kwargs.pop("lineCap", "round"),
        "lineJoin": kwargs.pop("lineJoin", "round"),
        "dashArray": kwargs.pop("dashArray", None),
        "dashOffset": kwargs.pop("dashOffset", None),
        "fill": fill,
        "fillColor": fill_color,
        "fillOpacity": kwargs.pop("fillOpacity", 0.2),
        "fillRule": kwargs.pop("fillRule", "evenodd"),
        "bubblingMouseEvents": kwargs.pop("bubblingMouseEvents", True),
    }
    default.update(extra_options)
    return default
