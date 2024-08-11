#Imports
import math

#Starting Message
print("Welcome to the PhysVEK Calculator")
mode_selection= int(input("Select an option by inputting a number\n1. 2-D Vector Addition\n2. Speed Calculation\n3. Quit\n"))

#Vector Addition Functions (hey, that's our main goal here!)
def vector_fission(angle_degree,initial_vector_magnitude):
    #SOHCAHTOA
    #Python doesn't like degrees, we must convert it into radians
    angle_radian = angle_degree*(math.pi/180)
    #Let's find X
    x_value = math.cos(angle_radian)*initial_vector_magnitude
    #Then Y
    y_value = math.sin(angle_radian)*initial_vector_magnitude
    return x_value, y_value
def vector_addition(x_value_list,y_value_list):
    #To get the X(resultant) and Y(resultant), we need to add all of the x and y values together
    x_value_resultant= sum(x_value_list)
    y_value_resultant= sum(y_value_list)
    #Arctan
    resultant_angle_radians= math.atan(y_value_resultant/x_value_resultant)
    #Angle Adjustment Thingy for Quadrants
    if x_value_resultant > 0 and y_value_resultant > 0: #Quadrant 1
        resultant_angle_degree= resultant_angle_radians*(180/math.pi)
    if x_value_resultant < 0 and y_value_resultant > 0: #Quadrant 2
        resultant_angle_degree= resultant_angle_radians*(180/math.pi)+180
    if x_value_resultant < 0 and y_value_resultant < 0: #Quadrant 3
        resultant_angle_degree= resultant_angle_radians*(180/math.pi)+180
    if x_value_resultant > 0 and y_value_resultant < 0: #Quadrant 4
        resultant_angle_degree= resultant_angle_radians*(180/math.pi)+360
    if x_value_resultant > 0 and y_value_resultant == 0: #East Axis
        resultant_angle_degree= resultant_angle_radians*(180/math.pi)
    if x_value_resultant == 0 and y_value_resultant > 0: #North Axis
        resultant_angle_degree= resultant_angle_radians*(180/math.pi)
    if x_value_resultant < 0 and y_value_resultant == 0: #West Axis
        resultant_angle_degree= resultant_angle_radians*(180/math.pi)+180
    if x_value_resultant == 0 and y_value_resultant < 0: #South Axis
        resultant_angle_degree= resultant_angle_radians*(180/math.pi)+360
    #Pythagorean Theorem Time!
    resultant_magnitude= math.sqrt((x_value_resultant**2)+(y_value_resultant**2))
    return resultant_angle_degree, resultant_magnitude

#Speed Calculation Function (extra useless features!)
def speed_calculation(vector_magnitude,starting_time,ending_time):
    deltaT= ending_time-starting_time
    speed= vector_magnitude/deltaT
    return speed

#List of X and Y values
x_value_list= []
y_value_list= []

#Mode Selection 1
if mode_selection == 1:
    loop = True
    while loop== True:
        #A loop that allows you to add additional vectors until you want to stop
        add_additional_vectors= input("Add additional vectors? Y/N\n")
        if add_additional_vectors== ("Y"):
            angle_degree= float(input("Input angle as a degree\n"))
            initial_vector_magnitude= float(input("Input magnitude. Do not include units\n"))
            x_value, y_value = vector_fission(angle_degree, initial_vector_magnitude)
            x_value_list.append(float(x_value))
            y_value_list.append(float(y_value))
            print(x_value_list)
            print(y_value_list)
        if add_additional_vectors== ("N"):
            resultant_angle_degree, resultant_magnitude = vector_addition(x_value_list,y_value_list)
            print("Resultant Vector Magnitude:", round(resultant_magnitude,3)," units\nResultant Vector Angle:", round(resultant_angle_degree,3)," degrees")
            loop= False

#Mode Selection 2
if mode_selection == 2:
    vector_magnitude= abs(float(input("Input magnitude. Do not include units\n")))
    starting_time= float(input("Input starting time, do not include units\n"))
    ending_time= float(input("Input ending time, do not include units\n"))
    speed = speed_calculation(vector_magnitude,starting_time,ending_time)
    print("Speed:", round(speed,3)," unit(s)/time unit")

#Mode Selection 3
if mode_selection == 3:
    quit()
