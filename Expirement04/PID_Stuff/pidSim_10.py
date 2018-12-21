import Tkinter as tk
from math import sin, cos, pi, sqrt, log
import numpy as np
from random import randint
from pid_controller_3.pid import PID, twiddle

#https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python
def angle_between(p0, p1, p2):
    v0 = np.array(p0) - np.array(p1)
    v1 = np.array(p2) - np.array(p1)
    
    angle = np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1))
    return angle

def rotate(point, origin, angle):
    ''' 
    rotate point around origin
    '''
    x = cos(angle) * (point[0]-origin[0]) - sin(angle) * (point[1]-origin[1]) + origin[0]
    y = sin(angle) * (point[0]-origin[0]) + cos(angle) * (point[1]-origin[1]) + origin[1]
    return (x, y)

def distance(a, b):
    s = [pow(ai - bi, 2) for ai, bi in zip(a,b)]
    return sqrt(sum(s))

CANVAS_SIZE = {
        'width' : 800, 
        'height' : 600
        }

class Robot(object):
    def __init__(self, cx, cy, target, canvas=None):
        self.cx = cx
        self.cy = cy
        self.radius = 25
        
        self.wheelRadius = 25
        self.wheelWidth = 1
        
        self.orientation = 0
        self.leftWheelVelocity =  0
        self.rightWheelVelocity = 0
        
        self.error = 0
        
        self.canvas = canvas
        
        self.angleLineLength = 100
        
        self.target = target
        
        if canvas:
            self.body = self.canvas.create_oval(
                    self.cx - self.radius,
                    self.cy - self.radius,
                    self.cx + self.radius,
                    self.cy + self.radius)
            
            top = rotate(
                    (self.cx + self.radius, self.cy - self.wheelRadius),
                    (self.cx, self.cy),
                    self.orientation + pi/2
                    )
            
            bottom = rotate(
                    (self.cx + self.radius, self.cy + self.wheelRadius),
                    (self.cx, self.cy),
                    self.orientation + pi/2
                    )
            
            self.rightWheel = self.canvas.create_line(
                    top[0], top[1],
                    bottom[0], bottom[1],
                    fill='blue')
            
            top = rotate(
                    (self.cx + self.radius, self.cy - self.wheelRadius),
                    (self.cx, self.cy),
                    self.orientation - pi/2
                    )
            
            bottom = rotate(
                    (self.cx + self.radius, self.cy + self.wheelRadius),
                    (self.cx, self.cy),
                    self.orientation - pi/2
                    )
            
            self.leftWheel = self.canvas.create_line(
                    top[0], top[1],
                    bottom[0], bottom[1],
                    fill='blue')
            
            self.angleLine = self.canvas.create_line(
                    self.cx, self.cy,
                    self.cx + self.angleLineLength, self.cy
                    )
            
            self.targetLine = self.canvas.create_line(
                     self.cx, self.cy,
                     self.target.cx, self.target.cy,
                     fill='yellow'
                    )
        
    def move(self): 
        '''
        equations from help/icckinematics.pdf
        '''
        
        # the distance between the centers of the two wheels
        W = 2 * self.radius
        
        if self.rightWheelVelocity == self.leftWheelVelocity:
            self.cx = cos(self.orientation) * self.rightWheelVelocity + self.cx
            self.cy = sin(self.orientation) * self.leftWheelVelocity + self.cy
        else:
            # the signed distance from the ICC to the midpoint between the wheels
            R = (W / 2.) * ((self.leftWheelVelocity + self.rightWheelVelocity) / 
                 (self.leftWheelVelocity - self.rightWheelVelocity))
            
            ###############################################
            # rate of rotation
            w = (self.leftWheelVelocity - self.rightWheelVelocity) / W
            
            # Instantaneous Center of Curvature 
            ICC = (self.cx - R * sin(self.orientation),
                   self.cy + R * cos(self.orientation))
            #print("R=", R, "w=", w)
            delta_t = 1
            
            A = np.array([
                        [cos(w * delta_t), -sin(w * delta_t), 0],
                        [sin(w * delta_t),  cos(w * delta_t), 0],
                        [0.0,               0.0,              1]
                    ], float)
            B = np.array([
                    [self.cx - ICC[0], ],
                    [self.cy - ICC[1], ],
                    [self.orientation, ]
                    ], float)
            C = np.array([
                    [ICC[0], ],
                    [ICC[1], ],
                    [w * delta_t]
                    ], float)
        
            position = np.dot(A, B) + C
    
            self.cx = position[0][0]
            self.cy = position[1][0]
            self.orientation = position[2][0]
        #print (self.cx, self.cy, self.orientation)
    
    def setLeftVelocity(self, v):
        d = self.distanceToTarget()
        if (d > 200):
            s = 4
        else:
            s = d/200 * 4
            
        v = v/10
        if v > 1: v = 1
        elif v < -1 : v = -1
        
        self.leftWheelVelocity = s + v
        
        if self.leftWheelVelocity < 0: self.leftWheelVelocity = 0
    
    def setRightVelocity(self, v):
        d = self.distanceToTarget()
        if (d > 200):
            s = 4
        else:
            s = d/200 * 4
        
        v = v/10
        if v > 1: v = 1
        elif v < -1 : v = -1
        
        self.rightWheelVelocity = s + v
        
        if self.rightWheelVelocity < 0: self.rightWheelVelocity = 0
        
    def distanceToTarget(self):
        return distance((self.cx, self.cy),
                        (self.target.cx, self.target.cy))
        
    def updateError(self):
        p0 = (cos(self.orientation) * self.angleLineLength + self.cx,
              sin(self.orientation) * self.angleLineLength + self.cy)
        p1 = (self.cx, self.cy)
        p2 = (self.target.cx, self.target.cy )
        
        self.error = angle_between(p0, p1, p2)
        
        self.error = self.error * self.distanceToTarget() 
        
                
            
    def draw(self):
        if not self.canvas: return
        
        self.canvas.coords(self.body, 
                self.cx - self.radius,
                self.cy - self.radius,
                self.cx + self.radius,
                self.cy + self.radius)
        
        top = rotate(
                (self.cx + self.radius, self.cy - self.wheelRadius),
                (self.cx, self.cy),
                self.orientation + pi/2
                )
        
        bottom = rotate(
                (self.cx + self.radius, self.cy + self.wheelRadius),
                (self.cx, self.cy),
                self.orientation + pi/2
                )

        self.canvas.coords(self.rightWheel, 
                    top[0], top[1],
                    bottom[0], bottom[1],)
        
        top = rotate(
                (self.cx + self.radius, self.cy - self.wheelRadius),
                (self.cx, self.cy),
                self.orientation - pi/2
                )
        
        bottom = rotate(
                (self.cx + self.radius, self.cy + self.wheelRadius),
                (self.cx, self.cy),
                self.orientation - pi/2
                )
        
        self.canvas.coords(self.leftWheel, 
                    top[0], top[1],
                    bottom[0], bottom[1],)
        
        self.canvas.coords(self.targetLine, 
                           self.cx, self.cy,
                           self.target.cx, self.target.cy
                           )
        
        self.canvas.coords(self.angleLine, 
                           self.cx, self.cy,
                           cos(self.orientation) * self.angleLineLength + self.cx,
                           sin(self.orientation) * self.angleLineLength + self.cy,
                           )
        
        
class Target(object):
    def __init__(self, cx, cy, canvas=None):
        self.cx = cx
        self.cy = cy
        self.size = 50
        
        self.canvas = canvas
        if canvas:
            self.target = self.canvas.create_rectangle(
                    self.cx - self.size/2,
                    self.cy - self.size/2,
                    self.cx + self.size/2,
                    self.cy + self.size/2)
            
    def relocate(self):
        self.cx = randint(self.size, CANVAS_SIZE['width'] - self.size)
        self.cy = randint(self.size, CANVAS_SIZE['height'] - self.size)
        
    def draw(self):
        self.canvas.coords(self.target, 
                           self.cx - self.size/2,
                           self.cy - self.size/2,
                           self.cx + self.size/2,
                           self.cy + self.size/2)
            
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.c = tk.Canvas(self, 
                           width = CANVAS_SIZE['width'], 
                           height = CANVAS_SIZE['height'])
        self.c.pack(side="top")
        
        self.target = Target(CANVAS_SIZE['width'] - 50, CANVAS_SIZE['height']/4, self.c)
        
        self.robot = Robot(CANVAS_SIZE['width'] / 2, CANVAS_SIZE['height'] /2,
                           self.target, self.c)
        
        # from running testBot_4.py
        best_params ={
           'left': [1.9000949269154073, 1.0074295458792055, -0.3900800362203175],
 'right': [1.2178197012079532, -1.7610000000000006, 1.5000000000000033]}
        
        self.leftPid = PID(*best_params['left'])
        self.rightPid = PID(*best_params['right'])
        
        # We want to drive the robot towards the 0 angle.
        self.leftPid.target = 0
        self.rightPid.target = 0
        
        self.timeStep = 0
        
        self.animate()

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def animate(self):
    
        self.timeStep += 1
        self.robot.updateError()
        
        leftAlpha = self.leftPid(feedback=self.robot.error, curr_tm=self.timeStep)
        rightAlpha = self.rightPid(feedback=self.robot.error, curr_tm=self.timeStep)
        
        #print(step, robot.error, leftAlpha, rightAlpha)
        
        self.robot.setLeftVelocity(leftAlpha)
        self.robot.setRightVelocity(rightAlpha)
        
        self.robot.move()
        self.robot.draw()
        
        if self.timeStep % 200 == 0:
            self.target.relocate()
            self.target.draw()
        
        print(self.timeStep, self.robot.error, leftAlpha, rightAlpha, 
              self.robot.leftWheelVelocity, self.robot.rightWheelVelocity)
        
        self.after(50, self.animate)

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
