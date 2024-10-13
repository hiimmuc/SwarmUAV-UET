import io
import sys

import folium
from folium.plugins.draw import Draw
from folium.raster_layers import TileLayer
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QFileDialog, QVBoxLayout, QWidget


class Mapy(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.interfejs()

    def interfejs(self):
        vbox = QVBoxLayout(self)
        self.webEngineView = QWebEngineView()
        self.webEngineView.page().profile().downloadRequested.connect(
            self.handle_downloadRequested
        )
        self.loadPage()
        vbox.addWidget(self.webEngineView)
        self.setLayout(vbox)
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle("mapy")
        self.show()

    def loadPage(self):
        titles = TileLayer(
            tiles="http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}",
            attr="google",
            name="google",
            max_zoom=20,
            subdomains=["mt0", "mt1", "mt2", "mt3"],
        )
        m = folium.Map(
            tiles=titles,
            location=[21.064862, 105.792958],
            zoom_start=16,
        )
        Draw(
            export=True,
            filename="my_data.geojson",
            position="topleft",
            draw_options={
                "polyline": False,
                "rectangle": False,
                "circle": False,
                "circlemarker": False,
            },
            edit_options={"poly": {"allowIntersection": False}},
        ).add_to(m)
        data = io.BytesIO()
        m.save(data, close_file=False)
        self.webEngineView.setHtml(data.getvalue().decode())

    def handle_downloadRequested(self, item):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", item.suggestedFileName())
        if path:
            item.setPath(path)
            item.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    okno = Mapy()
    sys.exit(app.exec_())
