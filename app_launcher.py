import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import json

class AppLauncher:
    def __init__(self, width=70, height=600):
        # Initialize the app launcher window
        self.root = tk.Tk()
        self.root.title('App Launcher')
        self.root.geometry(f'{width}x{height}')  # Set window size
        self.root.configure(bg="#000000")  # Set background color

        # Remove window title bar and borders
        self.root.overrideredirect(True)

        # Set minimum width and height
        self.root.minsize(width=70, height=height)

        # Bind mouse events to make the window draggable
        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.do_move)

        # Variables to track the window position
        self._offsetx = 0
        self._offsety = 0

        # Create a canvas for the glowing border effect
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg="#202124", highlightthickness=0)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # Create multiple borders with decreasing sizes and transparency
        self.create_borders(width, height)

        # Start the glowing animation
        self.glow_color_index = 0
        self.glow_colors = ["#BB86FC", "#3700B3", "#03DAC6"]  # Colors to cycle through
        self.animate_glow()

        # Load the apps from the JSON file
        self.load_apps()

    def create_borders(self, width, height):
        """Create multiple transparent borders with decreasing size and rounded corners."""
        border_colors = ["#BB86FC", "#3700B3", "#03DAC6", "#FFFFFF"]  # Example colors

        # Create the outermost border and assign it to self.rect for animation
        self.rect = self.create_rounded_rectangle(5, 5, width - 5, height - 5, radius=20, outline=border_colors[0], width=4)

        # Create 3 more borders inside the outermost one
        self.create_rounded_rectangle(12, 12, width - 12, height - 12, radius=15, outline=border_colors[1], width=3)
        self.create_rounded_rectangle(18, 18, width - 18, height - 18, radius=10, outline=border_colors[2], width=2)
        self.create_rounded_rectangle(24, 24, width - 24, height - 24, radius=5, outline=border_colors[3], width=1)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        """Create a rounded rectangle using a combination of lines and arcs."""
        points = [x1+radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1]

        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def animate_glow(self):
        """Animate the border glow effect by changing the rectangle's outline color."""
        # Change the outline color of the outermost border
        current_color = self.glow_colors[self.glow_color_index]
        self.canvas.itemconfig(self.rect, outline=current_color)

        # Update the color index for the next cycle
        self.glow_color_index = (self.glow_color_index + 1) % len(self.glow_colors)

        # Repeat the animation every 500 milliseconds (0.5 second)
        self.root.after(500, self.animate_glow)

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
            image = image.resize((30, 30), Image.Resampling.LANCZOS)
            icon = ImageTk.PhotoImage(image)

            # Create a button with the icon
            icon_button = tk.Button(
                self.canvas,  # Placed inside the canvas
                image=icon,
                command=lambda: self.launch_app(command),
                bg="#202124",
                bd=0
            )

            # Add hover effect to make icon enlarge on hover
            def on_hover(e):
                icon_button.config(width=40, height=40)

            def on_leave(e):
                icon_button.config(width=30, height=30)

            icon_button.bind("<Enter>", on_hover)
            icon_button.bind("<Leave>", on_leave)

            icon_button.image = icon

            # Place the icon button inside the canvas
            self.canvas.create_window(35, 50 + (index * 60), window=icon_button)  # Adjust position

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
        """Start moving the window."""
        self._offsetx = event.x
        self._offsety = event.y

    def do_move(self, event):
        """Handle window dragging."""
        x = event.x_root - self._offsetx
        y = event.y_root - self._offsety
        self.root.geometry(f'+{x}+{y}')

    def run(self):
        self.root.mainloop()  # Start the tkinter main loop


if __name__ == '__main__':
    launcher = AppLauncher()
    launcher.run()
