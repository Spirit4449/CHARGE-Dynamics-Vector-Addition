# PyQt5 imports
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QCheckBox
from PyQt5.QtCore import Qt, QSize

# Math imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Vector class
class Vector(QWidget):
    def __init__(self, name):
        super().__init__()

        # Name of the label
        self.name = name

        # Checked state
        self.checked = False

    def init_vector(self):
        # Main layout
        self.widget_layout = QVBoxLayout()

        # Main widget with the main layout
        self.widget = QWidget()
        self.widget.setLayout(self.widget_layout)

        self.widget.setStyleSheet(
            "background-color: #2f2f2f; border-radius: 15px; border: 3px solid #323232"
        )

        # Pointing cursor. When clicking this element, it highlights it
        self.setCursor(Qt.PointingHandCursor)

        # Top and bottom layouts
        self.top_layout = QHBoxLayout()
        self.bottom_layout = QHBoxLayout()

        # This is the name. We use self.name variable here
        self.name_element = QLabel(self.name)
        self.name_element.setStyleSheet('border: none;') # Turns off the default border
        self.top_layout.addWidget(self.name_element, stretch=1) # This allows it to take up space

        # Checkbox for when clicking the element
        self.check_element = QCheckBox()
        self.check_element.setStyleSheet('border: none;')
        self.check_element.setAttribute(Qt.WA_TransparentForMouseEvents, True) # No mouse events

        self.top_layout.addWidget(self.check_element)
        
        self.left_layout = QVBoxLayout()

        # Graph container
        self.canvas_container = QWidget(self)
        self.canvas_container.setStyleSheet(
            "background-color: #323232; border-radius: 10px; padding: 10px; border: none;")
        self.canvas_container.setAttribute(Qt.WA_TransparentForMouseEvents, True) # No mouse events

        # Graph
        self.figure, self.ax = plt.subplots()
        self.final_graph = FigureCanvas(self.figure)
        
        # Set the size of the container and the canvas
        self.graph_size = int(100)
        self.final_graph.setFixedSize(QSize(self.graph_size, self.graph_size))

        container_layout = QVBoxLayout()
        container_layout.addWidget(self.final_graph)
        self.canvas_container.setLayout(container_layout)
        self.left_layout.addWidget(self.canvas_container, stretch=2)

        self.right_layout = QVBoxLayout()

        self.magnitude_input_layout = QHBoxLayout()
        self.magnitude_icon = QLabel()
        self.magnitude_icon.setPixmap(QPixmap('gui/images/magnitude.png'))
        self.magnitude_icon.setStyleSheet('border: none;')
        self.magnitude_icon.setFixedWidth(40)

        self.magnitude_input = QLineEdit()
        self.magnitude_input.setPlaceholderText('Magnitude')
        self.magnitude_input.setStyleSheet('border-radius: 6px; border: none; background-color: #232323; padding: 10px 15px; border: 2px solid #202020')
        self.magnitude_input.setValidator(QIntValidator()) # Make sure numbers only are entered in here
        self.magnitude_input.textChanged.connect(self.plot_vector) # Plot vector every time text is changed

        self.magnitude_input_layout.addWidget(self.magnitude_icon)
        self.magnitude_input_layout.addWidget(self.magnitude_input)

        self.angle_input_layout = QHBoxLayout()
        self.angle_icon = QLabel()
        self.angle_icon.setPixmap(QPixmap('gui/images/angle.png'))
        self.angle_icon.setStyleSheet('border: none;')
        self.angle_icon.setFixedWidth(40)

        self.angle_input = QLineEdit()
        self.angle_input.setPlaceholderText('Angle')
        self.angle_input.setStyleSheet('border-radius: 6px; border: none; background-color: #232323; padding: 10px 15px; border: 2px solid #202020')
        self.angle_input.setValidator(QIntValidator()) # Make sure numbers only are entered in ehre
        self.angle_input.textChanged.connect(self.plot_vector) # Plot vector every time text is changed
        
        self.angle_input_layout.addWidget(self.angle_icon)
        self.angle_input_layout.addWidget(self.angle_input)

        self.right_layout.addLayout(self.magnitude_input_layout)
        self.right_layout.addLayout(self.angle_input_layout)


        self.bottom_layout.addLayout(self.left_layout)
        self.bottom_layout.addLayout(self.right_layout)

        self.widget_layout.addLayout(self.top_layout)
        self.widget_layout.addLayout(self.bottom_layout)

        self.plot_vector(initial=True) # Plot the initial vector

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15,5,15,5)
        main_layout.addWidget(self.widget)
        self.setLayout(main_layout)


    # When clicking this element, it toggles the checked state. When checked, various actions can be performed on it such as deleting and duplicating
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if not self.check_element.isChecked(): # Check it
                self.widget.setStyleSheet('background-color: #0b57a3; border-radius: 10px;')
                self.checked = True  # Emit the custom signal
                self.check_element.setChecked(True)
            else: # Check off
                self.widget.setStyleSheet('background-color: #2f2f2f; border-radius: 10px;')
                self.checked = False  # Emit the custom signal
                self.check_element.setChecked(False)


    # Graphing function. This is a repeat function from the other file but I couldn't figure out how to incorporate them together. (shrug)
    def plot_vector(self, initial=False):
        if (not self.magnitude_input.text() == '' and not self.angle_input.text() == '' and not self.angle_input.text() == '-' and not self.magnitude_input.text() == '-') or initial==True: # Makes sure valid input is coming from the text boxes
            if initial == True: # Initial means it is not actually plotting anything. Its just plotting the axes
                magnitude = 0
                angle = 0
            else:
                magnitude = float(self.magnitude_input.text()) # Grab the magnitude from the input
                angle = float(self.angle_input.text()) # Grab the angle from the input
            try:
                angle_rad = np.deg2rad(angle) # Convert from degress to radians
                x = magnitude * np.cos(angle_rad) # Use trig
                y = magnitude * np.sin(angle_rad) # Use trig

                # Clear previous plot
                self.final_graph.figure.clear()

                # Create a new subplot
                self.ax = self.final_graph.figure.add_subplot(111)

                if magnitude == 0:
                    margin = 0.2
                else:
                    margin = 0.2 * magnitude
                self.ax.set_xlim(-magnitude - margin, magnitude + margin)
                self.ax.set_ylim(-magnitude - margin, magnitude + margin)

                # Set aspect ratio to be equal
                self.ax.set_aspect('equal')

                # Draw X and Y axes
                self.ax.axhline(0, color='white', linewidth=1)
                self.ax.axvline(0, color='white', linewidth=1)

                # Hide spines (don't look good)
                self.ax.spines['top'].set_visible(False)
                self.ax.spines['right'].set_visible(False)
                self.ax.spines['left'].set_visible(False)
                self.ax.spines['bottom'].set_visible(False)

                # Remove grid lines
                self.ax.grid(False)

                # Remove ticks
                self.ax.set_xticks([])
                self.ax.set_yticks([])

                self.ax.tick_params(axis='both', colors='white', which='both', width=0)  # Hide tick lines

                
                # Set background color for the axes and figure
                self.figure.patch.set_facecolor('#323232')
                self.ax.set_facecolor('#323232')

                # Arrow and line
                self.ax.plot([0, x], [0, y], color='#2589d8', linestyle='-', linewidth=2)
                self.ax.quiver(0, 0, x, y, angles='xy', scale_units='xy', scale=0.9, color='green', 
                        width=0.012, headwidth=10, headlength=8, headaxislength=6)


                # Draw the updated plot
                self.final_graph.draw()
            except Exception as e:
                print(e)