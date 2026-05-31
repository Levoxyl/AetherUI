import math

def draw_visualization(self):
    # Draw a network visualization
    w = self.viz_canvas.winfo_width() or 800
    h = self.viz_canvas.winfo_height() or 500
    if w < 10 or h < 10:  # Canvas not ready
        self.root.after(100, self.draw_visualization)
        return
    
    # Clear previous drawings
    self.viz_canvas.delete("viz")
    
    # Draw radar background
    center_x, center_y = w * 0.35, h * 0.5
    radius = min(w, h) * 0.35
    
    # Draw concentric circles
    for i in range(1, 5):
        r = radius * i / 4
        self.viz_canvas.create_oval(
            center_x - r, center_y - r,
            center_x + r, center_y + r,
            outline='#003300',
            width=1,
            tags=("viz", "radar")
        )
    
    # Draw crosshairs
    self.viz_canvas.create_line(center_x, center_y - radius, center_x, center_y + radius, 
                                fill='#003300', width=1, tags=("viz", "radar"))
    self.viz_canvas.create_line(center_x - radius, center_y, center_x + radius, center_y, 
                                fill='#003300', width=1, tags=("viz", "radar"))
    
    # Draw radar sweep
    rad = math.radians(self.radar_angle)
    x = center_x + radius * math.cos(rad)
    y = center_y + radius * math.sin(rad)
    self.viz_canvas.create_line(center_x, center_y, x, y, fill='#00FF00', width=2, tags=("viz", "sweep"))

def update_visualization(self):
    w = self.viz_canvas.winfo_width() or 800
    h = self.viz_canvas.winfo_height() or 500
    if w < 10 or h < 10:  # Canvas not ready
        self.root.after(100, self.update_visualization)
        return