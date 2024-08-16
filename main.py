import sys
from PyQt5.QtWidgets import QApplication

from gui.main_window import Application


# This file just runs the gui

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    sys.exit(app.exec_())
