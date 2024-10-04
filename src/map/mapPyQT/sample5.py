import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication
# import bs4

maphtml = '''

    <!DOCTYPE HTML>
    <html>
      <head>
        <script src="http://www.webglearth.com/v2/api.js"></script>
        <script>
          function initialize() {
            var earth = new WE.map('earth_div');
            WE.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
              attribution: '© OpenStreetMap contributors'
            }).addTo(earth);
          }
        </script>
        <style>
          html, body{padding: 0; margin: 0;}
          #earth_div{top: 0; right: 0; bottom: 0; left: 0; position: absolute !important;}
        </style>
        <title>WebGL Earth API: Hello World</title>
      </head>
      <body onload="initialize()">
        <div id="earth_div"></div>
      </body>
    </html>
    '''


class Browser(QApplication):
    def __init__(self):
        QApplication.__init__(self, [])
        self.window = QWidget()

        self.web = QWebEngineView(self.window)

        self.web.setHtml(maphtml)
        self.layout = QVBoxLayout(self.window)
        self.layout.addWidget(self.web)
        self.window.show()


if __name__ == "__main__":
    app = Browser()
    sys.exit(app.exec_())
