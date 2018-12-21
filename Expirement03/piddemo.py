# Params =======================================================================

# Displacement force (e.g. wind)
DISPLACEMENT_PIXELS_PER_SECOND = 50

# PI(D) controller
Kp = 0
Ki = 0

# PID update frequency in Hertz
PID_UPDATE_HZ = 2

# Frame title
BASE_TITLE = 'PID Demo'

# Display update frequency in Hertz 
DISPLAY_UPDATE_HZ = 100

# Robot 
ROBOT_SIZE_PIXELS             = 20
ROBOT_SPEED_PIXELS_PER_SECOND = 100 


# Canvas 
CANVAS_SIZE          = 500        # square
BACKGROUND_COLOR     = 'black'
FOREGROUND_COLOR     = 'green'
MIDLINE_COLOR        = 'blue'
MARGIN_COLOR         = 'red'

# Safety margin for collision with top, bottom
MARGIN_Y = 20

import sys
from math import *
import breezypythongui

# Robot class ==================================================================

class Robot:
    
    def __init__(self):
        
        # Start in center of canvas
        self.x = CANVAS_SIZE / 2
        self.y = CANVAS_SIZE / 2
        
        # Use count for PID update
        self.count = 0
        
        # Use error sum for integral term
        self.e_sum = 0
        
        
    def getPosition(self):

       dt = 1. / DISPLAY_UPDATE_HZ

       # Robot moves steadily rightward
       dx = ROBOT_SPEED_PIXELS_PER_SECOND * dt
       self.x = (self.x + dx) % CANVAS_SIZE

       # Robot is displaced downward by an external force
       dy = DISPLACEMENT_PIXELS_PER_SECOND * dt
       y = self.y + dy

       # Use count for PID update
       self.count += 1
       
       pid_period = DISPLAY_UPDATE_HZ / PID_UPDATE_HZ

       if self.count == pid_period:
           self.count = 0
           
       # Simulate corrective force via time decay    
       decay = pow(exp(-float(self.count) / pid_period), 6)
                  
       # Error term is difference between new position and desired
       e = y - CANVAS_SIZE / 2
                                
       # PI correction
       self.y = y - decay*(Kp*e + Ki*self.e_sum)
       
       # Accumulate error sum
       self.e_sum += e
       
       return (self.x, self.y)
        
# GUI ==========================================================================

class PID_GUI(breezypythongui.EasyFrame):
    
    def __init__(self, robot):
        
        # Set up the window
        breezypythongui.EasyFrame.__init__(self, title = BASE_TITLE)
        
        # Canvas
        self.canvas = self.addCanvas(row = 0, column = 0,
            columnspan = 1,
            width = CANVAS_SIZE,
            height = CANVAS_SIZE,
            background = BACKGROUND_COLOR)
        self.setResizable(False)

        # Line in middle
        self.draw_line(CANVAS_SIZE / 2, MIDLINE_COLOR)
        
        # Lines at margins
        self.draw_line(MARGIN_Y, MARGIN_COLOR)
        self.draw_line(CANVAS_SIZE-MARGIN_Y, MARGIN_COLOR)
        
        
        # Store robot for timer task
        self.robot = robot

        # Init graphics items
        self.circle = None
        
    def draw_line(self, y, color):
        self.canvas.drawLine(0, y, CANVAS_SIZE, y, color, width = 1)



# Timer task for gui update
def task(gui):
    
    # Erase the old robot
    if gui.circle:
        gui.canvas.deleteItem(gui.circle)
        
    # Get the robot's current position
    x, y = robot.getPosition()

    # If too close to top or bottom, done
    if y < MARGIN_Y or y > (CANVAS_SIZE-MARGIN_Y):
        sys.exit(0)

    # Draw the robot in its current position
    r = ROBOT_SIZE_PIXELS / 2
    gui.circle = gui.canvas.drawOval(x-r, y-r, x+r, y+r, fill=FOREGROUND_COLOR)

    # We will update the title based on whether the autpilot is on     
    title = BASE_TITLE 
    
    # Update the title to report autopilot as needed
    gui.setTitle(title)
    
    # Reschedule event
    gui.after(1000/DISPLAY_UPDATE_HZ, task, gui)            
        
        
# main =========================================================================

robot = Robot()
    
# Create gui with host, port, controller
gui = PID_GUI(robot)
    
# Start timer-task
gui.after(1000/DISPLAY_UPDATE_HZ, task, gui)

# Handle GUI events till done
gui.mainloop()



