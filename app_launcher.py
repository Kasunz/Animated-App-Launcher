import tkinter as tk
# from PIL import Image, ImageTk
# import subprocess

class AppLauncher:
    def __init__(self, width=50, height=600):
        # initialize the app launcher window
        self.root = tk.Tk()
        self.root.title('Hi')
        self.root.geometry(f'{width}x{height}') # set window size
        self.root.configure(bg="#202124")

        # Remove window title bar and borders
        self.root.overrideredirect(True)

        self.root.minsize(width=50, height=height) # Set minimum width to 10 and minimum height to 100

        # Bind mouse events to make the window draggable
        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.do_move)

        # Variables to track the window position
        self._offsetx = 0
        self._offsety = 0

    def start_move(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def do_move(self, event):
        x = event.x_root -  self._offsetx
        y = event.y_root - self._offsety
        self.root.geometry(f'+{x}+{y}')



    def run(self):
        self.root.mainloop()    # start the tkinter main loop

if __name__ == '__main__':
    launcher = AppLauncher()
    launcher.run()
