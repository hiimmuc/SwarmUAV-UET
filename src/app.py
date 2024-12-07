import asyncio
import sys

from PyQt5 import QtWidgets

from interface_wrapper import *


class Runner:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setStyle("Oxygen")
        self.loop = QEventLoop(self.app)
        asyncio.set_event_loop(self.loop)
        self.window = App()

    def run(self):
        self.window.show()
        with self.loop:
            pending = asyncio.all_tasks(loop=self.loop)
            for task in pending:
                task.cancel()
            sys.exit(self.loop.run_forever())


if __name__ == "__main__":
    runner = Runner()
    runner.run()
