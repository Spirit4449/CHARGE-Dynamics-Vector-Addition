# GUI imports (PyQt5)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QGuiApplication
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QApplication, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, QLineEdit, QFrame, QScrollArea, QMessageBox
from PyQt5.QtCore import Qt, QSize

# Math imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Other file imports
from gui.vector import Vector
from add import vector_addition, vector_fission

# Main Application class
class Application(QWidget):
    def __init__(self):
        super().__init__()

        # Global variables
        self.image_path = 'gui/images'

        # Variables for vector handling
        self.vector_instances = {}
        self.instance_count = 0
        self.naming_count = 0

        self.is1920x1080 = False

        self.init_window()
        self.init_widgets()


    def init_window(self):
        # Center window on screen
        screen = QGuiApplication.primaryScreen().availableGeometry()
        if screen.width() <= 2000 and screen.height() <= 1200:
            self.is1920x1080 = True

        # Small adjustments to the window if the screen is lower resolution
        if self.is1920x1080 == True:
            self.window_width = round(screen.width() * 0.35)
            self.window_height = round(screen.height() * 0.7) 
        else:
            self.window_width = round(screen.width() * 0.25) 
            self.window_height = round(screen.height() * 0.6) 

        self.window_x = int((screen.width() - self.window_width) / 2)
        self.window_y = int((screen.height() - self.window_height - 50) / 2)
        self.setGeometry(self.window_x, self.window_y, self.window_width, self.window_height) # Set the position and size of window

        # Window details
        self.setWindowTitle("Vector Addition")
        self.setWindowIcon(QIcon(f'{self.image_path}/window_icon.png'))

        # Styles
        self.setStyleSheet('background-color: #241e22; color: white;')
        QApplication.setFont(QFont('Segoe UI', 10))

    # All the different widgets in the gui
    def init_widgets(self):
        # Main layout is a vertical layout in which all the widgets are added
        # Layouts are used so that the gui is responsive to different screens
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        # Output viewing layout
        self.output_layout = QHBoxLayout()
        self.output_layout.setAlignment(Qt.AlignTop)
        self.output_layout.setContentsMargins(25,25,25,10)
        
        self.canvas_container = QWidget(self) # Holds the graph in this container
        self.canvas_container.setStyleSheet(
            "background-color: #323232; border-radius: 10px; padding: 10px;")

        # Resulting Graph
        self.figure, self.ax = plt.subplots()
        self.final_graph = FigureCanvas(self.figure)
        
        # Set the size of the container and the canvas
        if self.is1920x1080 == True:
            self.graph_size = int(self.window_height * 0.4)
        else:
            self.graph_size = int(self.window_height * 0.3)
        self.final_graph.setFixedSize(QSize(self.graph_size, self.graph_size))

        # Create a layout for the container
        container_layout = QVBoxLayout()
        container_layout.addWidget(self.final_graph)
        self.canvas_container.setLayout(container_layout)
        self.output_layout.addWidget(self.canvas_container, stretch=1)
        self.plot_vector(0, 0) # Plot an initial non-existant vector to show the axis lines in the container

        # Small spacer between the graph and the output values
        spacer_size = round(self.window_width * 0.02)
        spacer = QSpacerItem(spacer_size, spacer_size)
        self.output_layout.addSpacerItem(spacer)

        # Output numbers
        self.output_numbers_layout = QVBoxLayout()

        # Magnitude
        self.magnitude_output_layout = QVBoxLayout()

        self.magnitude_label_layout = QHBoxLayout() # horizontal layout

        self.magnitude_icon = QLabel(self)
        self.magnitude_icon.setPixmap(QPixmap(f'{self.image_path}/magnitude.png'))
        self.magnitude_icon.setFixedWidth(50)

        self.magnitude_output = QLineEdit("0") # Initial text of 0
        self.magnitude_output.setStyleSheet("border: none; background-color: #323232; border-radius: 10px; padding: 0px 20px;")
        self.magnitude_output.setFont(QFont('Segoe UI Semibold', 20))
        self.magnitude_output.setFixedHeight(100)
        self.magnitude_output.setReadOnly(True)
        self.magnitude_output_label = QLabel('Magnitude')

        # Order the widgets on the page and in the layouts
        self.magnitude_label_layout.addWidget(self.magnitude_icon)
        self.magnitude_label_layout.addWidget(self.magnitude_output_label)
        self.magnitude_output_layout.addLayout(self.magnitude_label_layout)
        self.magnitude_output_layout.addWidget(self.magnitude_output)
        self.output_numbers_layout.addLayout(self.magnitude_output_layout)
        
        # Angle
        self.angle_output_layout = QVBoxLayout()

        self.angle_label_layout = QHBoxLayout()

        self.angle_icon = QLabel(self)
        self.angle_icon.setPixmap(QPixmap(f'{self.image_path}/angle.png'))
        self.angle_icon.setFixedWidth(50)
        self.angle_output = QLineEdit('0') # Initial text of 0
        self.angle_output.setStyleSheet("border: none; background-color: #323232; border-radius: 10px; padding: 0px 20px;")
        self.angle_output.setFont(QFont('Segoe UI Semibold', 20))
        self.angle_output.setFixedHeight(100)
        self.angle_output.setReadOnly(True)
        self.angle_output_label = QLabel('Angle')
        
        # Order the widgets on the page and in the layouts
        self.angle_label_layout.addWidget(self.angle_icon)
        self.angle_label_layout.addWidget(self.angle_output_label)
        self.angle_output_layout.addLayout(self.angle_label_layout)
        self.angle_output_layout.addWidget(self.angle_output)
        self.output_numbers_layout.addLayout(self.angle_output_layout)

        # add the numbers to the output layout but with a stretch of 4 so that it takes up more space
        self.output_layout.addLayout(self.output_numbers_layout, stretch=4)
        self.layout.addLayout(self.output_layout)




        # Divider - thin line between output and input containers
        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.HLine)
        self.divider.setFrameShadow(QFrame.Sunken)
        self.divider.setStyleSheet("background-color: #8d8d8d;")
        self.divider.setFixedHeight(1)
        self.layout.addWidget(self.divider)

        # Input Layout
        self.input_layout = QHBoxLayout()
        self.input_layout.setContentsMargins(15,10,15,15)

        # This widget allows for scrolling. All the vectors are placed in here and they can be scrolled
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  # Ensures the vector layout resizes with the scroll area
        self.scroll_area.setStyleSheet("""
            QScrollArea{
                border: none;
                background-color: #252525;
                border-radius: 15px;
                padding-top: 10px;
                padding-bottom: 10px;
                padding-right: 8px;
                border: #444444 2px;
            }
            QScrollBar:vertical {
                background: #333;
                width: 15px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #3e3e3e;
                min-height: 0px;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical {
                background: #333;
                border-radius: 6px;
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
                                       
            }
            QScrollBar::sub-line:vertical {
                height: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
        """)

        vertical_scrollbar = self.scroll_area.verticalScrollBar() # This is the scroll bar element. I need it to set the scroll speed
        vertical_scrollbar.setSingleStep(10)  # Set scroll speed
        vertical_scrollbar.setPageStep(20) # Step when pressing pgup and pgdown
        
        # This is the widget that can be scrolled. The scroll widget is placed inside of this
        self.vector_widget = QWidget()
        self.vector_widget.setStyleSheet('background-color: transparent;') # Allow see through so that you can see the scroll widget
        self.vector_layout = QVBoxLayout(self.vector_widget)
        self.vector_layout.setContentsMargins(0,0,0,0)

        # Add two vectors to begin with
        self.add_vector()
        self.add_vector()

        self.scroll_area.setWidget(self.vector_widget)  # Set the scrollable widget


        # The buttons
        self.button_layout = QVBoxLayout()

        self.select_all = QPushButton()
        self.select_all.setIcon(QIcon(f'{self.image_path}/select_all.png'))
        self.select_all.setCursor(Qt.PointingHandCursor)
        self.select_all.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                color: white;
                border-radius: 8px;
                padding: 20px 40px;
                border: 1px solid #3e3e3e;
            }
            QPushButton:hover {
                background-color: #3e3e3e;   
            }
        """)
        self.select_all.clicked.connect(self.select_all_vectors) # This is the callback function when clicking it
        self.button_layout.addWidget(self.select_all)

        self.deselect_all = QPushButton()
        self.deselect_all.setIcon(QIcon(f'{self.image_path}/deselect_all.png'))
        self.deselect_all.setCursor(Qt.PointingHandCursor)
        self.deselect_all.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                color: white;
                border-radius: 8px;
                padding: 20px 40px;
                border: 1px solid #3e3e3e;
            }
            QPushButton:hover {
                background-color: #3e3e3e;   
            }
        """)
        self.deselect_all.clicked.connect(self.deselect_all_vectors) # This is the callback function when clicking it
        self.button_layout.addWidget(self.deselect_all)
        
        self.add = QPushButton()
        self.add.setIcon(QIcon(f'{self.image_path}/add.png'))
        self.add.setCursor(Qt.PointingHandCursor)
        self.add.setStyleSheet("""
            QPushButton {
                background-color: #323232;
                color: white;
                border-radius: 8px;
                border: 1px solid #3e3e3e;
                padding: 20px 40px;
            }
            QPushButton:hover {
                background-color: #3e3e3e;   
            }
        """)
        self.add.clicked.connect(self.add_vector) # This is the callback function when clicking it
        self.button_layout.addWidget(self.add)

        self.duplicate = QPushButton()
        self.duplicate.setIcon(QIcon(f'{self.image_path}/duplicate.png'))
        self.duplicate.setCursor(Qt.PointingHandCursor)
        self.duplicate.setStyleSheet("""
            QPushButton {
                background-color: #323232;
                color: white;
                border-radius: 8px;
                border: 1px solid #3e3e3e;
                padding: 20px 40px;
            }
            QPushButton:hover {
                background-color: #3e3e3e;   
            }
        """)
        self.duplicate.clicked.connect(self.duplicate_vector) # This is the callback function when clicking it
        self.button_layout.addWidget(self.duplicate)

        self.remove = QPushButton()
        self.remove.setIcon(QIcon(f'{self.image_path}/delete.png'))
        self.remove.setCursor(Qt.PointingHandCursor)
        self.remove.setStyleSheet("""
            QPushButton {
                background-color: #323232;
                color: white;
                border-radius: 8px;
                border: 1px solid #3e3e3e;
                padding: 20px 40px;
            }
            QPushButton:hover {
                background-color: #3e3e3e;   
            }
        """)
        self.remove.clicked.connect(self.delete_vector) # This is the callback function when clicking it
        self.button_layout.addWidget(self.remove)

        self.calculate = QPushButton()
        self.calculate.setIcon(QIcon(f'{self.image_path}/equals.png'))
        self.calculate.setCursor(Qt.PointingHandCursor)
        self.calculate.setStyleSheet("""
            QPushButton {
                background-color: #4cc2ff;
                color: white;
                border-radius: 8px;
                border: 1px solid #52c4ff;
                padding: 20px 40px;
            }
            QPushButton:hover {
                background-color: #39b5f5;   
            }
        """)
        self.calculate.clicked.connect(self.calculate_vector) # This is the callback function when clicking it
        self.button_layout.addWidget(self.calculate)

        self.input_layout.addWidget(self.scroll_area, stretch=1)
        self.input_layout.addLayout(self.button_layout)

        self.layout.addLayout(self.input_layout) # Adds all the input elements onto the page

        QApplication.setStyle('Fusion') # Simple app theme that looks nice. Built in

        self.show() # Shows the gui and opens the window

    # Methods

    # Button Methods
    def select_all_vectors(self):
        for vector in self.vector_instances: # Iterates through every vector in the vector dictionary
            vector_element = self.vector_instances[vector] # gets the value 
            if not vector_element.check_element.isChecked(): # checks if the vector is not already checked
                vector_element.widget.setStyleSheet('background-color: #0b57a3; border-radius: 10px;') # visually changes the appearence
                vector_element.checked = True # Sets the checked variable of the class to TRUE
                vector_element.check_element.setChecked(True) # Visually changes the element to be checked
                
    def deselect_all_vectors(self):
        for vector in self.vector_instances: # Iterates through every vector in the vector dictionary
            vector_element = self.vector_instances[vector] # gets the value 
            if vector_element.check_element.isChecked(): # checks if the vector is already checked
                vector_element.widget.setStyleSheet('background-color: #2f2f2f; border-radius: 10px;') # visually changes the appearence
                vector_element.checked = False # Sets the checked variable of the class to False
                vector_element.check_element.setChecked(False) # Visually changes the element to not be checked

    def add_vector(self, index=None, initial_magnitude=None, initial_angle=None):
        # Saves a Vector Class into the vector dictionary. A string is passed into the class to specify the name of the vector (Vector 1, 2, 5....)
        # The naming count is used to make sure duplicate vector names aren't created in the dictionary
        self.vector_instances[f'Vector {self.naming_count + 1}'] = Vector(f'Vector {self.instance_count + 1}')
        # Get the vector object
        vector = self.vector_instances[f'Vector {self.naming_count + 1}']
        # Calls the init function to initialize the gui and show it
        vector.init_vector()

        # Prevents the vector from stretching out to fit the space
        vector.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        vector.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # This is used when duplicating vectors 
        if initial_magnitude != None and initial_magnitude != False:
            vector.magnitude_input.setText(str(initial_magnitude))
        
        if initial_angle != None and initial_magnitude != False:
            vector.angle_input.setText(str(initial_angle))

        # If a specific index hasn't been supplied.. aka... duplicate function not being called, it sets it to the last index of the list
        if not index:
            index = len(self.vector_instances) - 1

        self.vector_layout.insertWidget(index, vector)
        self.instance_count += 1
        self.naming_count += 1


    def delete_vector(self):
        vectors_to_delete = []
        for vector in self.vector_instances:
            vector_element = self.vector_instances[vector]
            if vector_element.checked == True:
                self.vector_layout.removeWidget(vector_element) # Removes from layout
                vector_element.deleteLater() # Deletes the object from memory
                vectors_to_delete.append(vector) # Appends to list to delete from list later. It will throw error if updating list size during iteration
        
        # Deletes the vector from the list
        for vector in vectors_to_delete:
            del self.vector_instances[vector]

        self.instance_count -= len(vectors_to_delete)
        self.rename_vectors() # Makes sure the vectors are in numerical order

    def rename_vectors(self):
        count = 1
        for vector in self.vector_instances:
            vector_element = self.vector_instances[vector]
            vector_element.name_element.setText(f'Vector {count}')
            count += 1

    def duplicate_vector(self):
        vectors_to_dupe = {}
        for vector in self.vector_instances:
            vector_element = self.vector_instances[vector]
            if vector_element.checked == True:
                list_of_vectors = list(self.vector_instances.keys())
                index = list_of_vectors.index(vector)
                vectors_to_dupe[index] = vector_element # Appends to list to add to vector list later. It will throw error if updating list size during iteration

        # Adds to vector list
        for index, vector in vectors_to_dupe.items():
            self.add_vector(index + 1, vector.magnitude_input.text(), vector.angle_input.text())

    def calculate_vector(self):
        xvalues = []
        yvalues = []

        # Simple error checking
        if len(self.vector_instances) == 0:
            return self.error_text('No vectors to add')
        elif len(self.vector_instances) == 1:
            return self.error_text('Need atleast 2 vectors')
        
        for vector in self.vector_instances:
            vector_element = self.vector_instances[vector]
            try:
                magnitude = float(vector_element.magnitude_input.text())
                angle = float(vector_element.angle_input.text())
            except:
                return self.error_text('Enter valid values') # If any given input is blank, it will error here

            try: 
                x, y = vector_fission(angle, magnitude) # Turns the vector into components <x, y>
                xvalues.append(x)
                yvalues.append(y)
            except Exception as e:
                self.error_text(str(e))

        # All components are added to a seperate x and y list and then fused together
        
        try:
            result_angle, result_magnitude = vector_addition(xvalues, yvalues) # Adds all the vectors and returns the result

            result_angle = round(result_angle, 2) # Round to 2 decimal places
            result_magnitude = round(result_magnitude, 2) # Round to 2 decimal places

            result_magnitude = self.sci_notation(result_magnitude) # If greather than 8 digits, it converts to scientific notation

            self.magnitude_output.setText(str(result_magnitude)) # Sets gui text to the result
            self.angle_output.setText(str(result_angle)) # Sets gui text to the result

            self.plot_vector(result_angle, result_magnitude) # Plots the vector on the graph

            # Ensures the error styles are not displayed (red background and small text)
            self.magnitude_output.setStyleSheet("border: none; background-color: #323232; border-radius: 10px; padding: 0px 20px;")
            self.angle_output.setStyleSheet("border: none; background-color: #323232; border-radius: 10px; padding: 0px 20px;")
        except Exception as e:
           self.error_text(str(e))

    # Scientific notation function
    def sci_notation(self, value):
        if abs(value) >= 1e8 or abs(value) < 1e-8:
            formatted_text = f'{value:.2e}' 
        else:
            formatted_text = value
        return formatted_text

    # Graphing function
    def plot_vector(self, angle, magnitude, initial=False):
        try:
            float(angle)
            float(magnitude)
        except Exception as e:
            return self.error_text(str(e))
        
        # Initial value means there is nothing to plot. It is just setting up the coordinate system and labels so its not blank
        try:
            if initial==True:
                magnitude = 0
                angle = 0

            angle_rad = np.deg2rad(angle) # Convert the angle from degrees to radians
            x = magnitude * np.cos(angle_rad) # The cosine of the angle gives the horizontal component
            y = magnitude * np.sin(angle_rad) # The sine of the angle gives the vertical component

            # Clear previous plot
            self.final_graph.figure.clear()

            # Create a new subplot
            self.ax = self.final_graph.figure.add_subplot(111)

            # Set axis limits with additional margin
            if magnitude == 0:
                margin = 0.2
            else:
                margin = 0.2 * magnitude
            # this prevents the labels from going offscreen. It puts them in the correct place
            self.ax.set_xlim(-magnitude - margin - 1, magnitude + margin + 1)
            self.ax.set_ylim(-magnitude - margin - 1, magnitude + margin + 1)

            # Set aspect ratio to be equal
            self.ax.set_aspect('equal')

            # Draw X and Y axes (coordinate plane)
            self.ax.axhline(0, color='white', linewidth=1)
            self.ax.axvline(0, color='white', linewidth=1)

            self.ax.set_title('Final Vector Graph', color='white') # Nice title

            # Hide spines (This is a box outline along the graph. It doesn't look good)
            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)
            self.ax.spines['left'].set_visible(False)
            self.ax.spines['bottom'].set_visible(False)

            # Remove grid lines
            self.ax.grid(False) # These grid lines are for charts. Not needed here

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
            self.ax.quiver(0, 0, x, y, angles='xy', scale_units='xy', scale=.9, color='green',  # Quiver is an arrow
                    width=0.01, headwidth=7, headlength=6, headaxislength=4)  # I played around with these values to draw a nice arrow

            self.final_graph.draw()
        except Exception as e:
            # In case of error.
            # This specific error occurs when the number is very large. Not sure why
            # I handle it gracefully by displaying an error box
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText(f"Cannot graph vector for large numbers")
            msg_box.setWindowTitle("Information")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            print(e) # Printing out the exact error to the console

    # Function to set the output text when the user did not input values correctly
    def error_text(self, text):
        self.magnitude_output.setStyleSheet("border: none; background-color: #7b200e; border-radius: 10px; padding: 0px 20px; font-size: 21px")
        self.angle_output.setStyleSheet("border: none; background-color: #7b200e; border-radius: 10px; padding: 0px 20px; font-size: 21px")

        self.magnitude_output.setText(text)
        self.angle_output.setText(text)

        self.plot_vector(0, 0, initial=True) # Plots dummy vector

    # This removes focus from output line edits when clicking off of them. PyQt5 does not do this by deault
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.magnitude_output.hasFocus() or self.angle_output.hasFocus():
                self.magnitude_output.setFocus(False) # Remove focus
                self.angle_output.setFocus(False)
        super().mousePressEvent(event) # Call the super function made by the library