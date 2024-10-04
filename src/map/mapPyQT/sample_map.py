# from PyQt5.QtWidgets import *
# import sys
# import qgmap
# from qgmap.common import QGoogleMap
# from PyQt5.QtCore import *

# sys.path.insert(0, "../")

# qgmap.use("PyQt5")


# if __name__ == '__main__':

#     def goCoords():
#         def resetError():
#             coordsEdit.setStyleSheet('')

#         try:
#             latitude, longitude = coordsEdit.text().split(",")
#         except ValueError:
#             coordsEdit.setStyleSheet("color: red;")
#             QTimer.singleShot(500, resetError)
#         else:
#             gmap.centerAt(latitude, longitude)
#             gmap.moveMarker("MyDragableMark", latitude, longitude)

#     def goAddress():
#         def resetError():
#             addressEdit.setStyleSheet('')

#         coords = gmap.centerAtAddress(addressEdit.text())
#         if coords is None:
#             addressEdit.setStyleSheet("color: red;")
#             QTimer.singleShot(500, resetError)
#             return
#         gmap.moveMarker("MyDragableMark", *coords)
#         coordsEdit.setText("{}, {}".format(*coords))

#     def onMarkerMoved(key, latitude, longitude):
#         print("Moved!!", key, latitude, longitude)
#         coordsEdit.setText("{}, {}".format(latitude, longitude))

#     def onMarkerRClick(key):
#         print("RClick on ", key)
#         gmap.setMarkerOptions(key, draggable=False)

#     def onMarkerLClick(key):
#         print("LClick on ", key)

#     def onMarkerDClick(key):
#         print("DClick on ", key)
#         gmap.setMarkerOptions(key, draggable=True)

#     def onMapMoved(latitude, longitude):
#         print("Moved to ", latitude, longitude)

#     def onMapRClick(latitude, longitude):
#         print("RClick on ", latitude, longitude)

#     def onMapLClick(latitude, longitude):
#         print("LClick on ", latitude, longitude)

#     def onMapDClick(latitude, longitude):
#         print("DClick on ", latitude, longitude)

#     app = QApplication(sys.argv)
#     w = QDialog()
#     h = QVBoxLayout(w)
#     l = QFormLayout()
#     h.addLayout(l)

#     addressEdit = QLineEdit()
#     l.addRow('Address:', addressEdit)
#     addressEdit.editingFinished.connect(goAddress)
#     coordsEdit = QLineEdit()
#     l.addRow('Coords:', coordsEdit)
#     coordsEdit.editingFinished.connect(goCoords)
#     gmap = QGoogleMap(w)
#     gmap.mapMoved.connect(onMapMoved)
#     gmap.markerMoved.connect(onMarkerMoved)
#     gmap.mapClicked.connect(onMapLClick)
#     gmap.mapDoubleClicked.connect(onMapDClick)
#     gmap.mapRightClicked.connect(onMapRClick)
#     gmap.markerClicked.connect(onMarkerLClick)
#     gmap.markerDoubleClicked.connect(onMarkerDClick)
#     gmap.markerRightClicked.connect(onMarkerRClick)
#     h.addWidget(gmap)
#     gmap.setSizePolicy(
#         QSizePolicy.MinimumExpanding,
#         QSizePolicy.MinimumExpanding)
#     w.showFullScreen()

#     gmap.waitUntilReady()

#     gmap.centerAt(21.028511, 105.804817)
#     gmap.setZoom(15)
#     lat, lng = gmap.centerAtAddress("Hanoi")
#     if lat is not None and lng is not None:

#         # Many icons at: https://sites.google.com/site/gmapsdevelopment/
#         gmap.addMarker("MyDragableMark", lat, lng, **dict(
#             icon="http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_red.png",
#             draggable=True,
#             title="Move me!"
#         ))

#         # Some Static points
#     for place in ["Plaza Ramon Castilla", "Plaza San Martin",]:
#         gmap.addMarkerAtAddress(
#             place, icon="http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_gray.png")
#     # gmap.setZoom(15)

#     sys.exit(app.exec_())

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from qOSM.common import QOSM
import sys
sys.path.insert(0, "../")


if __name__ == '__main__':

    def goCoords():
        def resetError():
            coordsEdit.setStyleSheet('')

        try:
            latitude, longitude = coordsEdit.text().split(",")
        except ValueError:
            coordsEdit.setStyleSheet("color: red;")
            QTimer.singleShot(500, resetError)
        else:
            map.centerAt(latitude, longitude)
            # map.moveMarker("MyDragableMark", latitude, longitude)

    def onMarkerMoved(key, latitude, longitude):
        print("Moved!!", key, latitude, longitude)
        coordsEdit.setText("{}, {}".format(latitude, longitude))

    def onMarkerRClick(key, latitude, longitude):
        print("RClick on ", key)
        # map.setMarkerOptions(key, draggable=False)

    def onMarkerLClick(key, latitude, longitude):
        print("LClick on ", key)

    def onMarkerDClick(key, latitude, longitude):
        print("DClick on ", key)
        # map.setMarkerOptions(key, draggable=True)

    def onMapMoved(latitude, longitude):
        print("Moved to ", latitude, longitude)

    def onMapRClick(latitude, longitude):
        print("RClick on ", latitude, longitude)

    def onMapLClick(latitude, longitude):
        print("LClick on ", latitude, longitude)

    def onMapDClick(latitude, longitude):
        print("DClick on ", latitude, longitude)

    app = QApplication(sys.argv)
    w = QDialog()
    h = QVBoxLayout(w)
    l = QFormLayout()
    h.addLayout(l)
    coordsEdit = QLineEdit()
    l.addRow('Coords:', coordsEdit)
    coordsEdit.editingFinished.connect(goCoords)
    map = QOSM(w)

    map.mapMovedCallback = onMapMoved
    map.markerMovedCallback = onMarkerMoved
    map.mapClickedCallback = onMapLClick
    map.mapDoubleClickedCallback = onMapDClick
    map.mapRightClickedCallback = onMapRClick
    map.markerClickedCallback = onMarkerLClick
    map.markerDoubleClickedCallback = onMarkerDClick
    map.markerRightClickedCallback = onMarkerRClick

    h.addWidget(map)
    map.setSizePolicy(
        QSizePolicy.Policy.Expanding,
        QSizePolicy.Policy.Expanding)
    w.show()

    map.waitUntilReady()

    map.centerAt(21.028511, 105.804817)
    map.setZoom(12)
    # Many icons at: https://sites.google.com/site/gmapsdevelopment/
    # coords = map.center()
    coords = 21.028511, 105.804817 + 0.001
    map.addMarker("MyDragableMark", *coords, **dict(
        icon="http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_gray.png",
        draggable=True,
        title="Move me MyDragableMark!"
    ))

    coords = 21.028511 + 0.001, 105.804817 + 0.001
    map.addMarker("MyDragableMark2", *coords, **dict(
        icon="http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_red.png",
        draggable=True,
        title="Move me MyDragableMark2"
    ))

    sys.exit(app.exec_())
