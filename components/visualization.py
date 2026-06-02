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
        self.title = tk.Label(
            self.frame, 
            text="> GLOBAL NETWORK THREAT MAP",
            font=('Courier', 12, 'bold'),
            fg=Colors.NEON_GREEN, bg='black', anchor='w', padx=10
        )
        self.title.pack(fill=tk.X, pady=(5, 0))

        # Internal canvas inside this frame
        self.canvas = tk.Canvas(self.frame, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # State Data
        self.status_values = [34, 2.4, 12500, 380, 28.4, 42, 67, 124]
        self.status_units = ["°C", "MPa", "RPM", "kPa", "V", "%", "%", "Mbps"]
        self.status_names = [
            "CORE TEMPERATURE", "PRESSURE", "ROTATION", "OIL PRESSURE",
            "VOLTAGE", "CPU USAGE", "MEMORY USAGE", "NETWORK"
        ]
        
        self.nodes = []
        for _ in range(12):
            self.nodes.append({
                "x": random.uniform(-0.9, 0.9),
                "y": random.uniform(-0.9, 0.9),
                "z": random.uniform(0.4, 0.9),
                "ip": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                "status": random.choice(["secure", "warning", "critical"]),
                "last_seen": time.time() - random.randint(1, 20)
            })

        # Start background loop sequences
        self.update_radar_and_nodes()
        self.update_status_metrics()
        self.blink_warnings()
            
    def draw_base_ui(self, w, h, center_x, center_y, radius):
        self.canvas.delete("viz")
        
        # Static Rings & Crosshairs
        for i in range(1, 5):
            r = radius * i / 4
            self.canvas.create_oval(
                center_x - r, center_y - r, center_x + r, center_y + r,
                outline=Colors.FILL_GREEN, width=1, tags=("viz", "radar")
            )
        self.canvas.create_line(center_x, center_y - radius, center_x, center_y + radius, fill=Colors.FILL_GREEN, width=1, tags=("viz", "radar"))
        self.canvas.create_line(center_x - radius, center_y, center_x + radius, center_y, fill=Colors.FILL_GREEN, width=1, tags=("viz", "radar"))
        
        self.canvas.create_rectangle(
            w * 0.55, h * 0.02, w * 0.98, h * 0.98,
            outline=Colors.NEON_GREEN, fill='black', width=1, tags=("viz", "status_panel")
        )
        self.canvas.create_text(
            w * 0.55 + 10, h * 0.02 + 10,
            text="> SYSTEM STATUS", anchor="nw", fill=Colors.NEON_GREEN, 
            font=('Courier', 12, 'bold'), tags=("viz", "status_title")
        )
        
        y_offsets = [50, 80, 110, 140, 170, 200, 230, 260]
        for i, (name, y_offset) in enumerate(zip(self.status_names, y_offsets)):
            y = h * 0.02 + y_offset
            bar_x = w * 0.55 + 180
            bar_y = y + 5
            
            self.canvas.create_text(
                w * 0.55 + 20, y, text=name, anchor="nw", 
                fill=Colors.NEON_GREEN, font=('Courier', 10), tags=("viz", f"status_{i}")
            )
            self.canvas.create_rectangle(
                bar_x, bar_y, bar_x + 200, bar_y + 12,
                outline=Colors.NEON_GREEN, fill='black', width=1, tags=("viz", f"bar_bg_{i}")
            )
            # Active indicator value bar
            self.canvas.create_rectangle(
                bar_x, bar_y, bar_x, bar_y + 12,
                outline=Colors.NEON_GREEN, fill=Colors.NEON_GREEN, width=0, tags=("viz", f"bar_{i}")
            )
            # Text metric
            self.canvas.create_text(
                bar_x + 210, bar_y - 2, text="", anchor="nw", 
                fill=Colors.NEON_GREEN, font=('Courier', 9), tags=("viz", f"value_{i}")
            )
            
        # Timestamp
        self.canvas.create_text(
            w * 0.55 + 10, h * 0.98 - 20, text="", anchor="sw", 
            fill=Colors.NEON_GREEN, font=('Courier', 9), tags=("viz", "timestamp")
        )

    def update_radar_and_nodes(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        if w < 10 or h < 10:
            self.root.after(100, self.update_radar_and_nodes)
            return
            
        center_x, center_y = w * 0.35, h * 0.5
        radius = min(w, h) * 0.35
        
        # loop tracker
        if not self.canvas.find_withtag("radar"):
            self.draw_base_ui(w, h, center_x, center_y, radius)

        self.canvas.delete("sweep")
        self.canvas.delete("node")
        self.canvas.delete("connection")
        self.canvas.delete("node_info")
        
        # Radar sweep 
        self.radar_angle = (self.radar_angle + 5) % 360
        rad = math.radians(self.radar_angle)
        x = center_x + radius * math.cos(rad)
        y = center_y + radius * math.sin(rad)
        self.canvas.create_line(center_x, center_y, x, y, fill=Colors.NEON_GREEN, width=2, tags=("viz", "sweep"))
        
        # 3D Perspective Node Mapping
        for node in self.nodes:
            scale = 0.5 + node["z"] * 0.5
            nx = center_x + node["x"] * radius * 0.9 * scale
            ny = center_y + node["y"] * radius * 0.9 * scale
            
            if math.sqrt((nx - center_x)**2 + (ny - center_y)**2) > radius * 0.95:
                continue
                
            color = Colors.NEON_GREEN if node["status"] == "secure" else Colors.YELLOW if node["status"] == "warning" else Colors.RED
            size = 5 + node["z"] * 5
            
            self.canvas.create_oval(nx - size, ny - size, nx + size, ny + size, fill=color, outline=color, tags=("viz", "node"))
            self.canvas.create_line(center_x, center_y, nx, ny, fill=color, width=1 + int(node["z"]), dash=(4, 2), tags=("viz", "connection"))
            self.canvas.create_text(nx + 15, ny, text=node["ip"], anchor="w", fill=color, font=('Courier', 8 + int(node["z"] * 2)), tags=("viz", "node_info"))
        
        if random.random() < 0.1:
            n = random.choice(self.nodes)
            n["status"] = random.choice(["secure", "warning", "critical"])
            
        self.root.after(50, self.update_radar_and_nodes)

    def update_status_metrics(self):
        w = self.canvas.winfo_width()
        if w < 10:
            self.root.after(500, self.update_status_metrics)
            return

        for i in range(8):
            change = random.uniform(-0.5, 0.5)
            self.status_values[i] = max(0, min(self.status_values[i] + change, 100))
            display_value = int(self.status_values[i]) if self.status_units[i] == "RPM" else round(self.status_values[i], 1)

            v_items = self.canvas.find_withtag(f"value_{i}")
            if v_items:
                self.canvas.itemconfig(v_items[0], text=f"{display_value}{self.status_units[i]}")
            
            # Resize calculation
            bar_items = self.canvas.find_withtag(f"bar_{i}")
            if bar_items:
                coords = self.canvas.coords(bar_items[0])
                bar_width = 200
                new_width = bar_width * min(self.status_values[i]/100, 1)
                self.canvas.coords(bar_items[0], coords[0], coords[1], coords[0] + new_width, coords[3])
                
                # Critical Threshold Conditional Fill Settings
                val = self.status_values[i]
                if (i == 0 and val > 40) or (i == 1 and val > 3.0) or (i == 5 and val > 80) or (i == 6 and val > 80):
                    self.canvas.itemconfig(bar_items[0], fill=Colors.RED)
                else:
                    self.canvas.itemconfig(bar_items[0], fill=Colors.NEON_GREEN)
                    
        # Synchronize Timestamp Label
        ts_items = self.canvas.find_withtag("timestamp")
        if ts_items:
            self.canvas.itemconfig(ts_items[0], text=f"LAST UPDATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        self.root.after(500, self.update_status_metrics)

    def blink_warnings(self):
        for i in range(3):
            if random.random() < 0.3:
                bar_items = self.canvas.find_withtag(f"bar_{i}")
                if bar_items:
                    self.canvas.itemconfig(bar_items[0], fill=Colors.RED)
                    self.root.after(200, lambda idx=i: self.restore_bar_color(idx))
        self.root.after(3000, self.blink_warnings)

    def restore_bar_color(self, idx):
        bar_items = self.canvas.find_withtag(f"bar_{idx}")
        if bar_items:
            self.canvas.itemconfig(bar_items[0], fill=Colors.NEON_GREEN)