
from tkinter import Tk, Canvas, Frame, BOTH, NW
from PIL import Image,ImageTk
import os

#Canon fire location for now is going to be 
#   x = bottom left of image plus 40 pixels
#   y = bottom left of image plus 45 pixels

class MainMenu(Frame):
    pass

class SettingsMenu(Frame):
    pass

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
        
        self.img1 = Image.open(os.path.join(self.image_directory,'tank_sprite.png'))
        self.tank1 = ImageTk.PhotoImage(self.img1)

        self.img2 = Image.open(os.path.join(self.image_directory,'tank_sprite_flipped.png'))
        self.tank2 = ImageTk.PhotoImage(self.img2)

        self.canvas = Canvas(self, width=self.img.size[0]+20,height=self.img.size[1]+20)

        self.background = self.canvas.create_image(10, 10, anchor=NW, image=self.backdrop)
        self.player_one = self.canvas.create_image(10+25,409,anchor=NW,image=self.tank1)
        #self.player_two = self.canvas.create_image(2213-25,409,anchor=NW,image=self.tank2)

        self.canvas.pack(fill=BOTH, expand=1)
    
    def forward(self,event):
        self.canvas.move(self.player_one,3,0)

    def reverse(self,event):
        self.canvas.move(self.player_one,-3,0)
    
    #def left_click(self,event):
    #    print('Click at X: {} Y: {}'.format(event.x,event.y))

    def right_click(self,event):
        print("fire")
    
    def aim(self,event):
        self.aimpoint = (event.x,event.y)
        print("Aim at X: {} Y: {}".format(event.x,event.y))
    
    def fire(self,event):
        print("Firing based on trajectory of {}".format(self.aimpoint))

class App(Tk):
    
    def __init__(self):
        super().__init__()
        self.launch_game()
        
    def launch_game(self):
        self.game_screen = Game()
        self.bind("<d>",self.game_screen.forward)
        self.bind("<a>",self.game_screen.reverse)
        self.bind("<Button-1>",self.game_screen.aim)
        self.bind("<Button-3>",self.game_screen.fire)
        self.bind("<B1-Motion>",self.game_screen.aim)

def main():
    root = App()
    root.mainloop()

main()
    

