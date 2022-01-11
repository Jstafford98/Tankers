from tkinter import Tk, Canvas, Frame, BOTH, NW, ARC
from tkinter.constants import BASELINE
from PIL import Image,ImageTk
from math import * 
import os

HORIZONTAL_MARGIN = 10
VERTICAL_MARGIN = 10
GROUND_LEVEL = 399 + VERTICAL_MARGIN
INITIAL_X_VALUE = HORIZONTAL_MARGIN + 25
INITIAL_Y_VALUE = GROUND_LEVEL
FORWARD_SPEED = 11
REVERSE_SPEED = -11
MAX_POWER = 10
HANG_TIME = 3 #in seconds
GRAVITY = 9.81 #m per second squared
MINIMUM_ELEVATION = 0.0

class Game(Frame):
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        
        '''
            Consider perlin noise map for terrain generation
        '''
        self.image_directory = os.path.join(os.getcwd(),'Tankers','images')

        self.master.title("Welcome to Tankers!")
        self.pack(fill=BOTH,expand=1)

        self.img = Image.open(os.path.join(self.image_directory,'gamebackground.png'))
        self.backdrop = ImageTk.PhotoImage(self.img)
        self.canvas_width = self.img.size[0]
        self.canvas_height = self.img.size[1]

        self.img1 = Image.open(os.path.join(self.image_directory,'tank_sprite.png'))
        self.tank1 = ImageTk.PhotoImage(self.img1)
        self.tank1_width = self.tank1.width()
        self.tank1_height = self.tank1.height()

        self.img2 = Image.open(os.path.join(self.image_directory,'tank_sprite_flipped.png'))
        self.tank2 = ImageTk.PhotoImage(self.img2)

        self.canvas = Canvas(self, width=self.canvas_width,height=self.canvas_height)

        self.background = self.canvas.create_image(HORIZONTAL_MARGIN, VERTICAL_MARGIN, anchor=NW, image=self.backdrop)
        self.player_one = self.canvas.create_image(INITIAL_X_VALUE,INITIAL_Y_VALUE,anchor=NW,image=self.tank1)
        self.ball = self.canvas.create_oval(INITIAL_X_VALUE,INITIAL_Y_VALUE,INITIAL_X_VALUE+10,INITIAL_Y_VALUE+10,fill='red')

        self.player_one_pos = [INITIAL_X_VALUE,INITIAL_Y_VALUE]
        
        #self.player_two = self.canvas.create_image(2213-25,409,anchor=NW,image=self.tank2)

        self.canvas.pack(fill=BOTH, expand=1)
    
    '''
        Determines distance of shot in a parabolic arc given power, angle, and height (0 for testing)
        https://www.daniweb.com/programming/software-development/code/450564/projectile-motion-python
        https://en.wikipedia.org/wiki/Range_of_a_projectile
        https://github.com/techwithtim/Projectile-Motion-Physics-Engine
        power is the distance from tank to aim point 
        angle is angle from shoot point to aim point in radians
        height is tank shoot point - ground level * -1 

        eventually will be able to simply refer to a height map and see what min y is at that current x point and adjust from there once terrain is generated 

    '''
    def calculate_arc(self,x,y,power,angle):
        time = 0.0
        points = []
        iters = 0
        canon_ball_x = x
        canon_ball_y = y
        while True:

            

            vx = cos(angle) * power
            vy = sin(angle) * power

            dx = vx * time
            dy = (vy * time) + ((-4.9 * (time ** 2)) / 2)

            hitx = round(dx + canon_ball_x)
            hity = round(canon_ball_y - dy)

            points.append((hitx, hity))
            canon_ball_x = hitx
            canon_ball_y = hity
            time += 0.09

            if points[-1][1] > GROUND_LEVEL + self.tank1_height:
                points.append((hitx, hity))
                break


        return points

    def calculate_angle(self,aim_point):

        x,y = self.player_x,self.player_y
        aim_x,aim_y = aim_point

        try:
            angle = atan((y - aim_y) / (x - aim_x))
        except:
            angle = pi / 2

        if aim_y < y and aim_x > x:
            angle = abs(angle)
        elif aim_y < y and aim_x < x:
            angle = pi - angle
        elif aim_y > y and aim_x < x:
            angle = pi + abs(angle)
        elif aim_y > y and aim_x > x:
            angle = (pi * 2) - angle

        return angle

    def calculate_velocity(self,player_position,aim_point):
        return sqrt(
            (aim_point[1]-player_position[1])**2 +
            (aim_point[0]-player_position[0])**2
            )/8

    def forward(self,event):
        if self.player_one_pos[0] + self.tank1_width < self.canvas_width:
            self.canvas.move(self.player_one,FORWARD_SPEED,0)
            self.player_one_pos[0] += FORWARD_SPEED
        elif self.player_one_pos[0] + self.tank1_width >= self.canvas_width:
            move_interval = self.canvas_width - (self.player_one_pos[0] + self.tank1_width)
            self.canvas.move(self.player_one,move_interval,0)
            self.player_one_pos[0] += move_interval

    def reverse(self,event):
        if self.player_one_pos[0]+REVERSE_SPEED > HORIZONTAL_MARGIN:
            self.canvas.move(self.player_one,REVERSE_SPEED,0)
            self.player_one_pos[0] += REVERSE_SPEED
        elif self.player_one_pos[0]+REVERSE_SPEED <= HORIZONTAL_MARGIN:
            move_interval = (self.player_one_pos[0] * -1) + HORIZONTAL_MARGIN
            self.canvas.move(self.player_one,move_interval,0)
            self.player_one_pos[0] += move_interval

    def aim(self,event):

        self.aimpoint = [event.x,event.y]
        self.player_x,self.player_y = self.player_one_pos[0]+self.tank1_width, \
                                      (GROUND_LEVEL + self.tank1_height)

        self.angle = self.calculate_angle(self.aimpoint)
        self.velocity = self.calculate_velocity([self.player_x,self.player_y],self.aimpoint)

        
    def fire(self,event):
        self.path = self.calculate_arc(x=self.player_x,y=self.player_y,power=self.velocity,angle=self.angle)
        for point in self.path[:-1]:
            self.canvas.create_oval(point[0],point[1],point[0]+10,point[1]+10,fill='red')
        #self.arc = self.canvas.create_arc(coord,style=ARC,width=5)
        self.canvas.pack(fill=BOTH, expand=1)

    def move_ball(self):
        self.canvas.move(self.ball,FORWARD_SPEED,0)