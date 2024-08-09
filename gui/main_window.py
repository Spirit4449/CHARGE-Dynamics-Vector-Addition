from PyQt5.QtGui import QPixmap, QIcon, QFont, QPainter, QColor, QDropEvent, QDragEnterEvent, QGuiApplication, QImage
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QApplication, QWidget, QButtonGroup, QRadioButton, QHBoxLayout, QSlider
from PyQt5.QtCore import Qt, QTimer, QSize, QRect, QEvent

class Application(QWidget):
    def __init__(self):
        super().__init__()

        # Global variables
        self.image_path = 'gui/images'

        self.init_window()
        self.init_widgets()

    def init_window(self):
        # Center window on screen
        screen = QGuiApplication.primaryScreen().availableGeometry()
        self.window_width = round(screen.width() * 0.6) # 60% of screen width
        self.window_height = round(screen.height() * 0.7) # 70% of screen heigth
        self.window_x = int((screen.width() - self.window_width) / 2)
        self.window_y = int((screen.height() - self.window_height) / 2)
        self.setGeometry(self.window_x, self.window_y, self.window_width, self.window_height) # Set the position and size of window

        # Window details
        self.setWindowTitle("Vector Addition")
        self.setWindowIcon(QIcon(f'{self.image_path}/window_icon.png'))

    def init_widgets(self):

        # add gui here
        
        self.show()