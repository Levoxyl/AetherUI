import math
import tkinter as tk

def setup_visualization(parent):
    parent.viz_title = tk.Label(
        parent.viz_frame, 
        text="> GLOBAL NETWORK THREAT MAP",
        font=('Courier', 12, 'bold'),
        fg='#00FF00',
        bg='black',
        anchor='w',
        padx=10
    )
    parent.viz_title.pack(fill=tk.X, pady=(5, 0))

def draw_visualization(parent):
    w = parent.viz_canvas.winfo_width() or 800
    h = parent.viz_canvas.winfo_height() or 500
    if w < 10 or h < 10:  # Canvas not ready
        parent.root.after(100, parent.draw_visualization)
        return

    parent.viz_canvas.delete("viz")
   
    # radar   
    center_x, center_y = w * 0.35, h * 0.5
    radius = min(w, h) * 0.35
 
    for i in range(1, 5):
        r = radius * i / 4
        parent.viz_canvas.create_oval(
            center_x - r, center_y - r,
            center_x + r, center_y + r,
            outline='#003300',
            width=1,
            tags=("viz", "radar")
        )
    
    # Crosshairs
    parent.viz_canvas.create_line(center_x, center_y - radius, center_x, center_y + radius, 
                                  fill='#003300', width=1, tags=("viz", "radar"))
    parent.viz_canvas.create_line(center_x - radius, center_y, center_x + radius, center_y, 
                                   fill='#003300', width=1, tags=("viz", "radar"))
    
    # Radar sweep
    rad = math.radians(parent.radar_angle)
    x = center_x + radius * math.cos(rad)
    y = center_y + radius * math.sin(rad)
    parent.viz_canvas.create_line(center_x, center_y, x, y, fill='#00FF00', width=2, tags=("viz", "sweep"))

def update_visualization(parent):
    w = parent.viz_canvas.winfo_width() or 800
    h = parent.viz_canvas.winfo_height() or 500
    if w < 10 or h < 10:  # Canvas not ready
        parent.root.after(100, parent.update_visualization)
        return