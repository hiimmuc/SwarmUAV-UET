from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.QtNetwork import QNetworkDiskCache
from PyQt5.QtCore import QUrl, pyqtSlot
import decorator
import os
import json
from .config import config

doTrace = False

backend = config['backend']


@decorator.decorator
def trace(function, *args, **k):
    """Decorates a function by tracing the begining and
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
        print('JS: %s line %d: %s' % (source, line, msg))


class QOSM(QWebEngineView):

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

    def __init__(self, parent=None, debug=True):
        QWebEngineView.__init__(self, parent=parent)

        cache = QNetworkDiskCache()
        cache.setCacheDirectory("cache")
        # self.page().networkAccessManager().setCache(cache)
        # self.page().networkAccessManager()

        self.initialized = False

        # self.page().mainFrame().addToJavaScriptWindowObject("qtWidget", self)

        basePath = os.path.abspath(os.path.dirname(__file__))
        basePath = basePath.replace("\\", "/")
        url = 'file:///' + basePath + '/qOSM.html'
        self.load(QUrl(url))

        web_channel = QWebChannel(self.page())
        self.page().setWebChannel(web_channel)
        web_channel.registerObject("qtWidget", self)

        # self.page().setLinkDelegationPolicy(QWebEnginePage.DelegateAllLinks)

        self.loadFinished.connect(self.onLoadFinished)
        # self.linkClicked.connect(QDesktopServices.openUrl)

        self.mapMovedCallback = None
        self.mapClickedCallback = None
        self.mapRightClickedCallback = None
        self.mapDoubleClickedCallback = None

        self.markerMovedCallback = None
        self.markerClickedCallback = None
        self.markerDoubleClickedCallback = None
        self.markerRightClickedCallback = None

    def onLoadFinished(self, ok):
        if self.initialized:
            return

        if not ok:
            print("Error initializing OpenStreetMap")

        self.initialized = True
        self.centerAt(0, 0)
        self.setZoom(10)

    def waitUntilReady(self):
        while not self.initialized:
            QApplication.processEvents()

    def runScript(self, script):
        return self.page().runJavaScript(script)

    def centerAt(self, latitude, longitude):
        self.runScript("osm_setCenter({}, {})".format(latitude, longitude))

    def setZoom(self, zoom):
        self.runScript("osm_setZoom({})".format(zoom))

    def center(self):
        center = self.runScript("osm_getCenter()")
        return center['lat'], center['lng']

    def addMarker(self, key, latitude, longitude, **extra):
        return self.runScript("osm_addMarker(key={!r},"
                              "latitude= {}, "
                              "longitude= {}, {});".format(key, latitude, longitude, json.dumps(extra)))

    def moveMarker(self, key, latitude, longitude):
        self.runScript("osm_moveMarker(key={!r},"
                       "latitude= {}, "
                       "longitude= {});".format(key, latitude, longitude))

    def positionMarker(self, key):
        return tuple(self.runScript("osm_posMarker(key={!r});".format(key)))
