from dataclasses import dataclass
from functools import cached_property

from PyQt5.QtCore import (
    QElapsedTimer,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
    QTime,
    QTimer,
)
from PyQt5.QtWidgets import (
    QApplication,
    QHeaderView,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


@dataclass
class TimerData:
    name_index: QPersistentModelIndex
    time_index: QPersistentModelIndex

    @cached_property
    def timer(self):
        timer = QTimer(interval=500)
        timer.timeout.connect(self._handle_timeout)
        return timer

    @cached_property
    def timer_elapsed(self):
        return QElapsedTimer()

    def start(self):
        self.timer_elapsed.start()
        self.timer.start()
        self._handle_timeout()

    def stop(self):
        self.timer.stop()

    def _handle_timeout(self):
        if self.time_index.isValid():
            time = QTime.fromMSecsSinceStartOfDay(self.timer_elapsed.elapsed())
            model = self.time_index.model()
            model.setData(QModelIndex(self.time_index), time.toString("mm:ss"))


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._timer_datas = list()

        self.button = QPushButton("Add")
        self.table = QTableWidget(0, 2)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        lay = QVBoxLayout(self)
        lay.addWidget(self.button)
        lay.addWidget(self.table)

        self.button.clicked.connect(self.handle_clicked)

    def handle_clicked(self):
        self.add_timer()

    def add_timer(self):
        row = self.table.rowCount()
        name_item = QTableWidgetItem(f"name-{row}")
        name_item.setTextAlignment(Qt.AlignCenter)
        time_item = QTableWidgetItem()
        time_item.setTextAlignment(Qt.AlignCenter)
        self.table.insertRow(row)
        self.table.setItem(row, 0, name_item)
        self.table.setItem(row, 1, time_item)
        timer_data = TimerData(
            QPersistentModelIndex(self.table.indexFromItem(name_item)),
            QPersistentModelIndex(self.table.indexFromItem(time_item)),
        )
        self._timer_datas.append(timer_data)
        timer_data.start()


def main():
    import sys

    app = QApplication(sys.argv)

    w = Widget()
    w.resize(640, 480)
    w.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
