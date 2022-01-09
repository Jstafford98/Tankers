from tkinter import Tk, Canvas, Frame, BOTH, NW
from Game import Game
import time

#Canon fire location for now is going to be 
#   x = bottom left of image plus 40 pixels
#   y = bottom left of image plus 45 pixels

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

    def launch_menu(self):
        pass

    def launch_settings(self):
        pass

    def timed_event(self):
        self.game_screen.move_ball()


def main():
    root = App()
    last_update = time.time()

    while True:
        
        if time.time() - last_update > .016:
            last_update = time.time()
            root.update()
            #root.timed_event()

main()