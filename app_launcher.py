import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import json

class AppLauncher:
    def __init__(self, width=50, height=600):
        # Initialize the app launcher window
        self.root = tk.Tk()
        self.root.title('App Launcher')
        self.root.geometry(f'{width}x{height}')  # Set window size
        self.root.configure(bg="#202124")  # Set background color

        # Remove window title bar and borders
        self.root.overrideredirect(True)

        # Set minimum width and height
        self.root.minsize(width=50, height=height)

        # Bind mouse events to make the window draggable
        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.do_move)

        # Variables to track the window position
        self._offsetx = 0
        self._offsety = 0

        # Load the apps from the JSON file
        self.load_apps()

    def load_apps(self):
        """Load apps from the JSON configuration file."""
        try:
            with open('app.json', 'r') as file:
                apps = json.load(file)

                for index, app in enumerate(apps):
                    self.create_icon(app['icon'], app['command'], index)

        except Exception as e:
            print(f"Failed to load apps: {e}")

    def create_icon(self, image_path, command, index):
        """Create and place an icon button."""
        try:
            image = Image.open(image_path)
            image = image.resize((24, 24), Image.Resampling.LANCZOS)
            icon = ImageTk.PhotoImage(image)

            # Create a button with the icon
            icon_button = tk.Button(
                self.root,
                image=icon,
                command=lambda: self.launch_app(command),
                bg="#202124",
                bd=0
            )

            # Add hover effect
            icon_button.bind("<Enter>", lambda e: icon_button.config(bg="#333333"))
            icon_button.bind("<Leave>", lambda e: icon_button.config(bg="#202124"))

            icon_button.image = icon
            icon_button.pack(pady=10)

        except Exception as e:
            print(f"Error loading icon from {image_path}: {e}")

    def launch_app(self, command):
        """Launch the application when the icon is clicked."""
        try:
            subprocess.Popen(command)
            print(f"Launching app: {command}")
        except Exception as e:
            print(f"Failed to launch app: {e}")

    def start_move(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def do_move(self, event):
        x = event.x_root - self._offsetx
        y = event.y_root - self._offsety
        self.root.geometry(f'+{x}+{y}')

    def run(self):
        self.root.mainloop()  # Start the tkinter main loop

if __name__ == '__main__':
    launcher = AppLauncher()
    launcher.run()
