import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel

class VectorPlotter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Vector Plotter")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Create Matplotlib canvas
        self.final_graph = FigureCanvas(plt.Figure())
        self.final_graph.setFixedWidth(60)
        self.layout.addWidget(self.final_graph)

        # Input fields for angle and magnitude
        self.angle_output = QLineEdit()
        self.angle_output.setPlaceholderText("Enter angle (degrees)")
        self.layout.addWidget(self.angle_output)

        self.magnitude_output = QLineEdit()
        self.magnitude_output.setPlaceholderText("Enter magnitude")
        self.layout.addWidget(self.magnitude_output)

        # Plot button
        self.plot_button = QPushButton("Plot Vector")
        self.plot_button.clicked.connect(self.plot_vector)
        self.layout.addWidget(self.plot_button)

        # Status label
        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

    def plot_vector(self, angle, magnitude):
        angle_rad = np.deg2rad(angle)
        x = magnitude * np.cos(angle_rad)
        y = magnitude * np.sin(angle_rad)

        # Clear previous plot
        self.final_graph.figure.clear()

        # Create a new subplot
        ax = self.final_graph.figure.add_subplot(111)
        ax.quiver(0, 0, x, y, angles='xy', scale_units='xy', scale=1, color='black')
        ax.set_xlim(-magnitude-1, magnitude+1)
        ax.set_ylim(-magnitude-1, magnitude+1)
        ax.set_aspect('equal')

        # Draw the updated plot
        self.final_graph.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VectorPlotter()
    window.show()
    sys.exit(app.exec_())
