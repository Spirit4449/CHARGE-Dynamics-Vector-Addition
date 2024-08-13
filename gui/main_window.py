from PyQt5.QtGui import QPixmap, QIcon, QFont, QPainter, QColor, QDropEvent, QDragEnterEvent, QGuiApplication, QImage
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QApplication, QWidget, QButtonGroup, QRadioButton, QHBoxLayout, QSlider, QSpacerItem, QSizePolicy, QLineEdit, QFrame
from PyQt5.QtCore import Qt, QTimer, QSize, QRect, QEvent

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

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
        self.window_width = round(screen.width() * 0.2) # 60% of screen width
        self.window_height = round(screen.height() * 0.6) # 70% of screen heigth
        self.window_x = int((screen.width() - self.window_width) / 2)
        self.window_y = int((screen.height() - self.window_height) / 2)
        self.setGeometry(self.window_x, self.window_y, self.window_width, self.window_height) # Set the position and size of window

        # Window details
        self.setWindowTitle("Vector Addition")
        self.setWindowIcon(QIcon(f'{self.image_path}/window_icon.png'))

        # Styles
        self.setStyleSheet('background-color: #241e22; color: white;')
        QApplication.setFont(QFont('Segoe UI', 10))

    def init_widgets(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        # Output viewing layout
        self.output_layout = QHBoxLayout()
        self.output_layout.setAlignment(Qt.AlignTop)
        self.output_layout.setContentsMargins(25,25,25,20)
        
        self.canvas_container = QWidget(self)
        self.canvas_container.setStyleSheet(
            "background-color: #323232; border-radius: 10px; padding: 10px;")  # Rounded corners and padding

        self.figure, self.ax = plt.subplots()
        self.final_graph = FigureCanvas(self.figure)
        
        # Set the size of the container and the canvas
        self.graph_size = int(self.window_height * 0.3)
        self.final_graph.setFixedSize(QSize(self.graph_size, self.graph_size))

        # Create a layout for the container
        container_layout = QVBoxLayout()
        container_layout.addWidget(self.final_graph)
        self.canvas_container.setLayout(container_layout)
        self.output_layout.addWidget(self.canvas_container, stretch=2)
        self.plot_vector(40, 234)

        spacer_size = round(self.window_width * 0.02)
        spacer = QSpacerItem(spacer_size, spacer_size)
        
        self.output_layout.addSpacerItem(spacer)

        # Output numbers
        self.output_numbers_layout = QVBoxLayout()

        # Magnitude
        self.magnitude_output_layout = QVBoxLayout()

        self.magnitude_label_layout = QHBoxLayout()

        self.magnitude_icon = QLabel(self)
        self.magnitude_icon.setPixmap(QPixmap('gui/images/magnitude.png'))
        self.magnitude_icon.setFixedWidth(50)

        self.magnitude_output = QLineEdit("0")
        self.magnitude_output.setStyleSheet("border: none; background-color: #323232; border-radius: 10px; padding: 0px 20px;")
        self.magnitude_output.setFont(QFont('Segoe UI Semibold', 35))
        self.magnitude_output.setReadOnly(True)
        self.magnitude_output_label = QLabel('Magnitude')

        self.magnitude_label_layout.addWidget(self.magnitude_icon)
        self.magnitude_label_layout.addWidget(self.magnitude_output_label)
        self.magnitude_output_layout.addLayout(self.magnitude_label_layout)
        self.magnitude_output_layout.addWidget(self.magnitude_output)
        self.output_numbers_layout.addLayout(self.magnitude_output_layout)
        
        # Angle
        self.angle_output_layout = QVBoxLayout()

        self.angle_label_layout = QHBoxLayout()

        self.angle_icon = QLabel(self)
        self.angle_icon.setPixmap(QPixmap('gui/images/angle.png'))
        self.angle_icon.setFixedWidth(50)

        self.angle_output = QLineEdit('0')
        self.angle_output.setStyleSheet("border: none; background-color: #323232; border-radius: 10px; padding: 0px 20px;")
        self.angle_output.setFont(QFont('Segoe UI Semibold', 35))
        self.angle_output.setReadOnly(True)
        self.angle_output_label = QLabel('Angle')
        
        self.angle_label_layout.addWidget(self.angle_icon)
        self.angle_label_layout.addWidget(self.angle_output_label)
        self.angle_output_layout.addLayout(self.angle_label_layout)
        self.angle_output_layout.addWidget(self.angle_output)
        self.output_numbers_layout.addLayout(self.angle_output_layout)


        self.output_layout.addLayout(self.output_numbers_layout, stretch=4)
        self.layout.addLayout(self.output_layout)




        # Divider
        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.HLine)
        self.divider.setFrameShadow(QFrame.Sunken)
        self.divider.setStyleSheet("background-color: white;")
        self.divider.setFixedHeight(1)
        self.layout.addWidget(self.divider)


        # Input Layout
        self.input_layout = QHBoxLayout()
        self.input_layout.setContentsMargins(15,20,15,15)

        self.vector_layout = QVBoxLayout()

        #self.#


        self.button_layout = QVBoxLayout()
        
        self.add = QPushButton()
        self.add.setIcon(QIcon('gui/images/add.png'))
        self.add.setCursor(Qt.PointingHandCursor)
        self.add.setStyleSheet("""
            QPushButton {
                background-color: #323232;
                color: white;
                border-radius: 8px;
                padding: 20px 40px;
            }
            QPushButton:hover {
                background-color: #3e3e3e;   
            }
        """)
        #self.add.toggled.connect(self.updateImagePreview)
        self.button_layout.addWidget(self.add)

        self.duplicate = QPushButton()
        self.duplicate.setIcon(QIcon('gui/images/duplicate.png'))
        self.duplicate.setCursor(Qt.PointingHandCursor)
        self.duplicate.setStyleSheet("""
            QPushButton {
                background-color: #323232;
                color: white;
                border-radius: 8px;
                padding: 20px 40px;
            }
            QPushButton:hover {
                background-color: #3e3e3e;   
            }
        """)
        #self.add.toggled.connect(self.updateImagePreview)
        self.button_layout.addWidget(self.duplicate)

        self.remove = QPushButton()
        self.remove.setIcon(QIcon('gui/images/delete.png'))
        self.remove.setCursor(Qt.PointingHandCursor)
        self.remove.setStyleSheet("""
            QPushButton {
                background-color: #323232;
                color: white;
                border-radius: 8px;
                padding: 20px 40px;
            }
            QPushButton:hover {
                background-color: #3e3e3e;   
            }
        """)
        #self.add.toggled.connect(self.updateImagePreview)
        self.button_layout.addWidget(self.remove)

        self.calculate = QPushButton()
        self.calculate.setIcon(QIcon('gui/images/equals.png'))
        self.calculate.setCursor(Qt.PointingHandCursor)
        self.calculate.setStyleSheet("""
            QPushButton {
                background-color: #4cc2ff;
                color: white;
                border-radius: 8px;
                padding: 30px 40px;
            }
            QPushButton:hover {
                background-color: #39b5f5;   
            }
        """)
        #self.add.toggled.connect(self.updateImagePreview)
        self.button_layout.addWidget(self.calculate)

        self.input_layout.addLayout(self.vector_layout, stretch=1)
        self.input_layout.addLayout(self.button_layout)

        self.layout.addLayout(self.input_layout)

        self.show()

    def plot_vector(self, angle, magnitude):
        try:
            angle_rad = np.deg2rad(angle)
            x = magnitude * np.cos(angle_rad)
            y = magnitude * np.sin(angle_rad)

            # Clear previous plot
            self.final_graph.figure.clear()

            # Create a new subplot
            self.ax = self.final_graph.figure.add_subplot(111)


            # Set axis limits with additional margin
            margin = 0.2 * magnitude
            self.ax.set_xlim(-magnitude - margin, magnitude + margin)
            self.ax.set_ylim(-magnitude - margin, magnitude + margin)

            # Set aspect ratio to be equal
            self.ax.set_aspect('equal')

            # Draw X and Y axes
            self.ax.axhline(0, color='white', linewidth=1)
            self.ax.axvline(0, color='white', linewidth=1)

            # Hide spines
            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)
            self.ax.spines['left'].set_visible(False)
            self.ax.spines['bottom'].set_visible(False)

            # Remove grid lines
            self.ax.grid(False)

            # Set ticks and labels
            self.ax.set_xticks([0, magnitude])
            self.ax.set_yticks([0, magnitude])
            self.ax.set_xticklabels([str(0), str(magnitude)])
            self.ax.set_yticklabels([str(0), str(magnitude)])
            self.ax.tick_params(axis='both', colors='white', which='both', width=0)  # Hide tick lines

            # Set background color for the axes and figure
            self.figure.patch.set_facecolor('#323232')
            self.ax.set_facecolor('#323232')

            # Draw the updated plot


            # Arrow and line
            self.ax.plot([0, x], [0, y], color='green', linestyle='-', linewidth=2)
            self.ax.quiver(0, 0, x, y, angles='xy', scale_units='xy', scale=.9, color='green', 
                    width=0.01, headwidth=7, headlength=6, headaxislength=4)


            # Draw the updated plot
            self.final_graph.draw()
        except Exception as e:
            print(e)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.magnitude_output.hasFocus() or self.angle_output.hasFocus():
                self.magnitude_output.setFocus(False)
                self.angle_output.setFocus(False)
        super().mousePressEvent(event)