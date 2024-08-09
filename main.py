import sys
from PyQt5.QtWidgets import QApplication

from gui.main_window import Application




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    sys.exit(app.exec_())
