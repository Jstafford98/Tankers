from tkinter import Tk, Canvas, Frame, BOTH, NW
from PIL import Image,ImageTk
import os

HORIZONTAL_MARGIN = 0
VERTICAL_MARGIN = 0
GROUND_LEVEL = 399
INITIAL_X_VALUE = HORIZONTAL_MARGIN + 25
INITIAL_Y_VALUE = VERTICAL_MARGIN + 399
FORWARD_SPEED = 11
REVERSE_SPEED = -11

class Game(Frame):
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        
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
    
    def calculate_arc():
        pass

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
        elif self.player_one_pos[0]+REVERSE_SPEED < HORIZONTAL_MARGIN:
            move_interval = self.player_one_pos[0] * -1
            self.canvas.move(self.player_one,move_interval,0)
            self.player_one_pos[0] += move_interval

    def move_sprite_img(self,sprite,distance):
        pass

    def aim(self,event):
        self.aimpoint = (event.x,event.y)
        print("Aim at X: {} Y: {}".format(event.x,event.y))
    
    def fire(self,event):
        print("Firing based on trajectory of {}".format(self.aimpoint))

    def move_ball(self):
        self.canvas.move(self.ball,FORWARD_SPEED,0)