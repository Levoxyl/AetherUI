import math
import tkinter as tk
import random
import time

from datetime import datetime
from colors import Colors

class VisualizationComponent:
    def __init__(self, frame, root):
        self.frame = frame
        self.root = root
        self.radar_angle = 0
        
        # Header Label
        self.title = tk.Label(
            self.frame, 
            text="> GLOBAL NETWORK THREAT MAP",
            font=('Courier', 12, 'bold'),
            fg=Colors.NEON_GREEN, bg='black', anchor='w', padx=10
        )
        self.title.pack(fill=tk.X, pady=(5, 0))

        # Dedicated Internal Canvas
        self.canvas = tk.Canvas(self.frame, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Isolated State Nodes config
        self.nodes = []
        for _ in range(6):
            self.nodes.append({
                "x": random.uniform(-0.9, 0.9),
                "y": random.uniform(-0.9, 0.9),
                "z": random.uniform(0.4, 0.9),
                "ip": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                "status": random.choice(["secure", "warning", "critical"]),
                "last_seen": time.time() - random.randint(1, 20)
            })

        self.update()
            
    def draw(self, center_x, center_y, radius):
        self.canvas.delete("radar_base")
        
        # Static bg Rings & Crosshairs
        for i in range(1, 5):
            r = radius * i / 4
            self.canvas.create_oval(
                center_x - r, center_y - r, center_x + r, center_y + r,
                outline='#003300', width=1, tags=("radar_base",)
            )
        self.canvas.create_line(center_x, center_y - radius, center_x, center_y + radius, fill='#003300', width=1, tags=("radar_base",))
        self.canvas.create_line(center_x - radius, center_y, center_x + radius, center_y, fill='#003300', width=1, tags=("radar_base",))

    def update(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        if w < 10 or h < 10:
            self.root.after(100, self.update)
            return
            
        center_x, center_y = w * 0.5, h * 0.5
        radius = min(w, h) * 0.45
        
        # static background coordinates update if the frame resizes
        self.draw(center_x, center_y, radius)

        # Clear active foreground objects
        self.canvas.delete("sweep")
        self.canvas.delete("node")
        self.canvas.delete("connection")
        self.canvas.delete("node_info")
        
        # Sweep line
        self.radar_angle = (self.radar_angle + 5) % 360
        rad = math.radians(self.radar_angle)
        x = center_x + radius * math.cos(rad)
        y = center_y + radius * math.sin(rad)
        self.canvas.create_line(center_x, center_y, x, y, fill='#00FF00', width=2, tags=("sweep",))
        
        # Render Nodes
        for node in self.nodes:
            scale = 0.5 + node["z"] * 0.5
            nx = center_x + node["x"] * radius * 0.9 * scale
            ny = center_y + node["y"] * radius * 0.9 * scale
            
            if math.sqrt((nx - center_x)**2 + (ny - center_y)**2) > radius * 0.95:
                continue
                
            color = Colors.NEON_GREEN if node["status"] == "secure" else Colors.YELLOW if node["status"] == "warning" else Colors.RED
            size = 5 + node["z"] * 5
            
            self.canvas.create_oval(nx - size, ny - size, nx + size, ny + size, fill=color, outline=color, tags=("node",))
            self.canvas.create_line(center_x, center_y, nx, ny, fill=color, width=1 + int(node["z"]), dash=(4, 2), tags=("connection",))
            self.canvas.create_text(nx + 15, ny, text=node["ip"], anchor="w", fill=color, font=('Courier', 8 + int(node["z"] * 2)), tags=("node_info",))
        
        if random.random() < 0.1:
            n = random.choice(self.nodes)
            n["status"] = random.choice(["secure", "warning", "critical"])
            
        self.root.after(50, self.update)