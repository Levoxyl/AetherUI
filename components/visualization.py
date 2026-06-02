import math
import tkinter as tk

class VisualizationComponent:
    def __init__(self, frame, canvas):
        self.frame = frame
        self.canvas = canvas
        self.radar_angle = 0
        
        self.title = tk.Label(
            self.frame, 
            text="> GLOBAL NETWORK THREAT MAP",
            font=('Courier', 12, 'bold'),
            fg='#00FF00', bg='black', anchor='w', padx=10
        )
        self.title.pack(fill=tk.X, pady=(5, 0))

        self.update()
            
    def draw(self):
        w = self.canvas.winfo_width() or 800
        h = self.canvas.winfo_height() or 500
        if w < 10 or h < 10:  # Canvas not ready
            self.frame.after(100, self.draw)
            return

        self.canvas.delete("viz")
    
        # radar   
        center_x, center_y = w * 0.35, h * 0.5
        radius = min(w, h) * 0.35
    
        for i in range(1, 5):
            r = radius * i / 4
            self.canvas.create_oval(
                center_x - r, center_y - r,
                center_x + r, center_y + r,
                outline='#003300',
                width=1,
                tags=("viz", "radar")
            )
        
        # Crosshairs
        self.canvas.create_line(center_x, center_y - radius, center_x, center_y + radius, 
                                    fill='#003300', width=1, tags=("viz", "radar"))
        self.canvas.create_line(center_x - radius, center_y, center_x + radius, center_y, 
                                    fill='#003300', width=1, tags=("viz", "radar"))
        
        # Radar sweep
        rad = math.radians(self.radar_angle)
        x = center_x + radius * math.cos(rad)
        y = center_y + radius * math.sin(rad)
        self.canvas.create_line(center_x, center_y, x, y, fill='#00FF00', width=2, tags=("viz", "sweep"))

    def update(self):
        w = self.canvas.winfo_width() or 800
        h = self.canvas.winfo_height() or 500
        if w < 10 or h < 10:  # Canvas not ready
            self.frame.after(100, self.update)
            return