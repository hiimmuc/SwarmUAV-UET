"""
MapEngine - A PyQt wrapper for Leaflet maps

This module provides a Python interface to Leaflet.js maps embedded in a PyQt WebEngineView.
It allows for programmatic control of maps, including adding/removing markers, lines,
and polygons, as well as handling map events.

Example Usage:
-------------
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
        [21.064862, 105.792958],  # p1
        [21.065862, 105.792958],  # p2
    ],
    options=dict(color="red", weight=5),
)

# Add polygons to the map
map_engine.drawPolygon(
    key="1",
    coordinates=[
        [21.064862, 105.792958],  # p1
        [21.065862, 105.792958],  # p2
        [21.065862, 105.793958],  # p3
        [21.064862, 105.793958],  # p4
    ],
    options=dict(color="green", weight=2, fill=True, fillColor="green", fillOpacity=0.2),
)
"""

import json
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

import decorator
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl, pyqtSlot
from PyQt5.QtNetwork import QNetworkDiskCache
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.QtWidgets import QApplication

# Suppress QtWebEngine logging
QtCore.qInstallMessageHandler(lambda *args: None)

# Debug flag for function tracing
doTrace = False


@decorator.decorator
def trace(function, *args, **k):
    """
    Trace decorator for debugging function calls.
    
    When doTrace is True, prints function entry and exit with arguments and return value.
    """
    if doTrace:
        print("> " + function.__name__, args, k)
    result = function(*args, **k)
    if doTrace:
        print("< " + function.__name__, args, k, "->", result)
    return result


class _LoggedPage(QWebEnginePage):
    """Custom WebEnginePage that logs JavaScript console messages."""
    
    @trace
    def javaScriptConsoleMessage(self, msg: str, line: int, source: str) -> None:
        """Log JavaScript console messages with source and line information."""
        print(f"JS: {source} line {line}: {msg}")


def geojson_to_coordinates(geojson: Union[str, Dict[str, Any]]) -> List:
    """
    Convert GeoJSON to coordinates array.
    
    Args:
        geojson: GeoJSON data as string or dictionary
        
    Returns:
        List containing [geometry_type, coordinates]
    """
    if isinstance(geojson, str):
        geojson = json.loads(geojson)
        
    geometry_type = geojson.get("geometry", {}).get("type", "")
    coordinates = geojson.get("geometry", {}).get("coordinates", [])

    if not coordinates:
        print("No coordinates found in GeoJSON")
        return []

    return [geometry_type, coordinates]


def camelize(key: str) -> str:
    """
    Convert a python_style_variable_name to lowerCamelCase.
    
    Args:
        key: Snake case string
        
    Returns:
        Camel case string
        
    Examples:
        >>> camelize("variable_name")
        'variableName'
        >>> camelize("variableName")
        'variableName'
    """
    return "".join(x.capitalize() if i > 0 else x for i, x in enumerate(key.split("_")))


def marker_options(**kwargs) -> dict:
    """
    Create options dictionary for map markers.
    
    Args:
        **kwargs: Marker options in either snake_case or camelCase
            
    Supported Options:
        draggable (bool): Whether marker is draggable. Default: False
        title (str): Tooltip text on hover. Default: ''
        icon (str): Icon path or name. Default: 'not_listed_location'
        icon_size (dict): Dictionary with width and height in pixels. Default: {width: 10, height: 10}
    
    Returns:
        dict: Formatted marker options for JavaScript
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
    Create options dictionary for vector overlays.
    
    Args:
        line (bool): Whether the path is a line. Default: False
        radius (float, optional): Radius for circle overlays. Default: None
        **kwargs: Path options in either snake_case or camelCase
    
    Supported Options:
        stroke (bool): Whether to draw stroke along the path. Default: True
        color (str): Stroke color. Default: '#3388ff'
        weight (int): Stroke width in pixels. Default: 3
        opacity (float): Stroke opacity. Default: 1.0
        line_cap (str): Shape at end of stroke ('round', 'butt', 'square'). Default: 'round'
        line_join (str): Shape at corners ('round', 'miter', 'bevel'). Default: 'round'
        dash_array (str): Stroke dash pattern. Default: None
        dash_offset (str): Distance into dash pattern to start. Default: None
        fill (bool): Whether to fill the path with color. Default: False
        fill_color (str): Fill color. Default: Same as stroke color
        fill_opacity (float): Fill opacity. Default: 0.2
        fill_rule (str): How inside of shape is determined ('evenodd', 'nonzero'). Default: 'evenodd'
        gradient (bool): Apply gradient to stroke and fill. Default: None
        
    Returns:
        dict: Formatted path options for JavaScript
    
    Note:
        If fill_color is specified, fill will be set to True regardless of fill parameter.
    """
    # Convert snake_case to camelCase
    kwargs = {camelize(key): value for key, value in kwargs.items()}

    # Set overlay-specific options
    extra_options = {}
    if line:
        extra_options = {
            "smoothFactor": kwargs.pop("smoothFactor", 1.0),
            "noClip": kwargs.pop("noClip", False),
        }
    if radius:
        extra_options.update({"radius": radius})

    # Handle color and fill options
    color = kwargs.pop("color", "#3388ff")
    fill_color = kwargs.pop("fillColor", False)
    
    if fill_color:
        fill = True
    elif not fill_color:
        fill_color = color
        fill = kwargs.pop("fill", False)

    # Handle additional options
    gradient = kwargs.pop("gradient", None)
    if gradient is not None:
        extra_options.update({"gradient": gradient})

    if kwargs.get("tags"):
        extra_options["tags"] = kwargs.pop("tags")

    if kwargs.get("className"):
        extra_options["className"] = kwargs.pop("className")

    # Build final options dictionary
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


class MapEngine(QWebEngineView):
    """
    PyQt wrapper for a Leaflet.js map embedded in a QWebEngineView.
    
    Provides Python interface for map manipulation and event handling.
    """
    
    def __init__(
        self,
        name: str = "",
        widget: Optional[QWebEngineView] = None,
        url: Optional[str] = None,
    ):
        """
        Initialize the map engine.
        
        Args:
            name: Identifier for the map
            widget: QWebEngineView widget to use (will create one if None)
            url: URL to load the map from
        """
        QWebEngineView.__init__(self, parent=widget.parent() if widget else None)

        # Setup disk cache
        cache = QNetworkDiskCache()
        cache.setCacheDirectory("cache")

        self.initialized = False
        self.map_name = name
        self.map_widget = widget or self

        # Load URL if provided
        if url is not None:
            self.map_widget.load(QUrl(url))

        # Setup web channel for JS-Python communication
        self.map_page = self.map_widget.page()
        web_channel = QWebChannel(self.map_page)
        self.map_page.setWebChannel(web_channel)
        web_channel.registerObject("qtWidget", self)

        # Connect initialization signal
        self.map_widget.loadFinished.connect(self.onLoadFinished)

        # Initialize callback functions
        self.mapMovedCallback = None
        self.mapClickedCallback = None
        self.mapRightClickedCallback = None
        self.mapDoubleClickedCallback = None

        self.markerMovedCallback = None
        self.markerClickedCallback = None
        self.markerDoubleClickedCallback = None
        self.markerRightClickedCallback = None

        self.mapGeojsonCallback = None

    # ====================== Event Handlers ======================
    
    # Marker events
    @pyqtSlot(str, float, float)
    def markerMoved(self, key: str, latitude: float, longitude: float) -> None:
        """Handle marker moved event from JavaScript."""
        if self.markerMovedCallback:
            self.markerMovedCallback(key, latitude, longitude)

    @pyqtSlot(str, float, float)
    def markerRightClicked(self, key: str, latitude: float, longitude: float) -> None:
        """Handle marker right-click event from JavaScript."""
        if self.markerRightClickedCallback:
            self.markerRightClickedCallback(key, latitude, longitude)

    @pyqtSlot(str, float, float)
    def markerClicked(self, key: str, latitude: float, longitude: float) -> None:
        """Handle marker click event from JavaScript."""
        if self.markerClickedCallback:
            self.markerClickedCallback(key, latitude, longitude)

    @pyqtSlot(str, float, float)
    def markerDoubleClicked(self, key: str, latitude: float, longitude: float) -> None:
        """Handle marker double-click event from JavaScript."""
        if self.markerDoubleClickedCallback:
            self.markerDoubleClickedCallback(key, latitude, longitude)

    # Map events
    @pyqtSlot(float, float)
    def mapMoved(self, latitude: float, longitude: float) -> None:
        """Handle map moved event from JavaScript."""
        if self.mapMovedCallback:
            self.mapMovedCallback(latitude, longitude)

    @pyqtSlot(float, float)
    def mapRightClicked(self, latitude: float, longitude: float) -> None:
        """Handle map right-click event from JavaScript."""
        if self.mapRightClickedCallback:
            self.mapRightClickedCallback(latitude, longitude)

    @pyqtSlot(float, float)
    def mapLeftClicked(self, latitude: float, longitude: float) -> None:
        """Handle map left-click event from JavaScript."""
        if self.mapClickedCallback:
            self.mapClickedCallback(latitude, longitude)

    @pyqtSlot(float, float)
    def mapDoubleClicked(self, latitude: float, longitude: float) -> None:
        """Handle map double-click event from JavaScript."""
        if self.mapDoubleClickedCallback:
            self.mapDoubleClickedCallback(latitude, longitude)

    # GeoJSON events
    @pyqtSlot(str)
    def geoJsonHandle(self, geojson: str) -> None:
        """Handle GeoJSON data from JavaScript."""
        if self.mapGeojsonCallback:
            self.mapGeojsonCallback(geojson)

    # ====================== Initialization ======================
    
    def onLoadFinished(self, ok: bool) -> None:
        """Handle map load completion."""
        if self.initialized:
            return

        if not ok:
            print("Error initializing Map")

        self.initialized = True
        print(f"Map engine initialized for: {self.map_name}")

    def waitUntilReady(self) -> None:
        """Block until map is initialized, processing events."""
        while not self.initialized:
            QApplication.processEvents()

    def runScript(self, script: str) -> Any:
        """
        Run JavaScript in the map page.
        
        Args:
            script: JavaScript code to execute
            
        Returns:
            Result of JavaScript execution
        """
        return self.map_page.runJavaScript(script)

    # ====================== Map Controls ======================
    
    def centerAt(self, latitude: float, longitude: float) -> None:
        """
        Center the map at specified coordinates.
        
        Args:
            latitude: Latitude in degrees
            longitude: Longitude in degrees
        """
        self.runScript(f"setCenterJs({latitude}, {longitude});")

    def setZoom(self, zoom: int) -> None:
        """
        Set map zoom level.
        
        Args:
            zoom: Zoom level (typically 1-18)
        """
        self.runScript(f"setZoomJs({zoom});")

    def center(self) -> Tuple[float, float]:
        """
        Get current map center coordinates.
        
        Returns:
            Tuple of (latitude, longitude)
        """
        center = self.runScript("getCenterJs();")
        return center["lat"], center["lng"]

    # ====================== Marker Functions ======================
    
    def addMarker(self, key: str, latitude: float, longitude: float, **options) -> Any:
        """
        Add a marker to the map.
        
        Args:
            key: Unique identifier for the marker
            latitude: Marker latitude
            longitude: Marker longitude
            **options: Additional marker options (see marker_options)
            
        Returns:
            JavaScript response
        """
        return self.runScript(
            f"addMarkerJs(key={json.dumps(key)},"
            f"latitude={round(latitude, 12)}, "
            f"longitude={round(longitude, 12)}, parameters={json.dumps(options)});"
        )

    def deleteMarker(self, key: str) -> Any:
        """
        Remove a marker from the map.
        
        Args:
            key: Marker identifier
            
        Returns:
            JavaScript response
        """
        return self.runScript(f"deleteMarkerJs(key={json.dumps(key)});")

    def mapMoveMarker(self, key: str, latitude: float, longitude: float) -> None:
        """
        Move a marker to new coordinates.
        
        Args:
            key: Marker identifier
            latitude: New latitude
            longitude: New longitude
        """
        self.runScript(f"moveMarkerJs(key={json.dumps(key)}, latitude={latitude}, longitude={longitude});")

    def positionMarker(self, key: str) -> Tuple[float, float]:
        """
        Get current position of a marker.
        
        Args:
            key: Marker identifier
            
        Returns:
            Tuple of (latitude, longitude)
        """
        return tuple(self.runScript(f"posMarkerJs(key={json.dumps(key)});"))

    # ====================== Line Functions ======================
    
    def drawPolyLine(self, key: str, coordinates: List[List[float]], options: dict = {}) -> Any:
        """
        Draw a polyline on the map.
        
        Args:
            key: Unique identifier for the polyline
            coordinates: List of [lat, lng] coordinate pairs
            options: Line style options (see path_options)
            
        Returns:
            JavaScript response
        """
        if len(coordinates) < 2:
            print("PolyLine requires at least 2 coordinates")
            return

        options = path_options(line=True, **options)
        return self.runScript(
            f"drawPolyLineJs(key={json.dumps(key)}, coords={json.dumps(coordinates)}, options={json.dumps(options)});"
        )

    def deletePolyLine(self, key: str) -> Any:
        """
        Remove a polyline from the map.
        
        Args:
            key: Polyline identifier
            
        Returns:
            JavaScript response
        """
        return self.runScript(f"deletePolyLineJs(key={json.dumps(key)});")

    # ====================== Polygon Functions ======================
    
    def drawPolygon(self, key: str, coordinates: List[List[float]], options: dict = {}) -> Any:
        """
        Draw a polygon on the map.
        
        Args:
            key: Unique identifier for the polygon
            coordinates: List of [lat, lng] coordinate pairs
            options: Polygon style options (see path_options)
            
        Returns:
            JavaScript response
        """
        if len(coordinates) < 3:
            print("Polygon requires at least 3 coordinates")
            return

        # Ensure polygon is closed (first point = last point)
        if coordinates[0] != coordinates[-1]:
            print("Polygon requires the first and last coordinates to be the same")
            return

        options = path_options(line=True, radius=None, fillcolor="#3388ff", **options)
        return self.runScript(
            f"drawPolygonJs(key={json.dumps(key)}, coords={json.dumps(coordinates)}, options={json.dumps(options)});"
        )

    def deletePolygon(self, key: str) -> Any:
        """
        Remove a polygon from the map.
        
        Args:
            key: Polygon identifier
            
        Returns:
            JavaScript response
        """
        return self.runScript(f"deletePolygonJs(key={json.dumps(key)});")