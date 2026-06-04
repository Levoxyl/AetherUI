import tkinter as tk
import random
from datetime import datetime

class StatusComponent:
    def __init__(self, frame, root):
        self.frame = frame
        self.root = root

        self.title = tk.Label(
            self.frame, text="> SYSTEM STATUS DIAGNOSTICS",
            font=('Courier', 12, 'bold'), fg='#00FF00', bg='black', anchor='w', padx=10
        )
        self.title.pack(fill=tk.X, pady=(5, 0))

        # Dedicated Status Canvas
        self.canvas = tk.Canvas(self.frame, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # State Telemetry Values
        self.status_values = [34, 2.4, 12500, 380, 28.4, 42, 67, 124]
        self.status_units = ["°C", "MPa", "RPM", "kPa", "V", "%", "%", "Mbps"]
        self.status_names = [
            "CORE TEMPERATURE", "PRESSURE", "ROTATION", "OIL PRESSURE",
            "VOLTAGE", "CPU USAGE", "MEMORY USAGE", "NETWORK"
        ]

        self.update()
        self.blink_warnings()

    def draw(self, w, h):
        self.canvas.delete("status_base")
        y_offsets = [40, 70, 100, 130, 160, 190, 220, 250]
        
        for i, (name, y_offset) in enumerate(zip(self.status_names, y_offsets)):
            bar_x = 180
            
            # Name
            self.canvas.create_text(
                20, y_offset, text=name, anchor="nw", 
                fill="#00FF00", font=('Courier', 10), tags=("status_base",))
            # Outline
            self.canvas.create_rectangle(
                bar_x, y_offset + 5, bar_x + 180, y_offset + 15,
                outline='#00FF00', fill='black', width=1, tags=("status_base",))
            # Active Bar
            self.canvas.create_rectangle(
                bar_x, y_offset + 5, bar_x, y_offset + 15,
                outline='#00FF00', fill='#00FF00', width=0, tags=(f"bar_{i}",))
            # Metric Text
            self.canvas.create_text(
                bar_x + 190, y_offset + 2, text="", anchor="nw", 
                fill="#00FF00", font=('Courier', 9), tags=(f"value_{i}",))
            
        # Live Time Tracker
        self.canvas.create_text(
            20, h - 20, text="", anchor="sw", 
            fill="#00FF00", font=('Courier', 9), tags=("timestamp",))

    def update(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10:
            self.root.after(500, self.update)
            return

        if not self.canvas.find_withtag("status_base"):
            self.draw(w, h)

        for i in range(8):
            change = random.uniform(-0.5, 0.5)
            self.status_values[i] = max(0, min(self.status_values[i] + change, 100))
            display_value = int(self.status_values[i]) if self.status_units[i] == "RPM" else round(self.status_values[i], 1)
            
            v_items = self.canvas.find_withtag(f"value_{i}")
            if v_items:
                self.canvas.itemconfig(v_items[0], text=f"{display_value}{self.status_units[i]}")
            
            bar_items = self.canvas.find_withtag(f"bar_{i}")
            if bar_items:
                coords = self.canvas.coords(bar_items[0])
                new_width = 180 * min(self.status_values[i]/100, 1)
                self.canvas.coords(bar_items[0], coords[0], coords[1], coords[0] + new_width, coords[3])
                
                val = self.status_values[i]
                if (i == 0 and val > 40) or (i == 1 and val > 3.0) or (i == 5 and val > 80) or (i == 6 and val > 80):
                    self.canvas.itemconfig(bar_items[0], fill="red")
                else:
                    self.canvas.itemconfig(bar_items[0], fill="#00FF00")
                    
        ts_items = self.canvas.find_withtag("timestamp")
        if ts_items:
            self.canvas.itemconfig(ts_items[0], text=f"LOG REFRESH: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        self.root.after(500, self.update)

    def blink_warnings(self):
        for i in range(3):
            if random.random() < 0.3:
                bar_items = self.canvas.find_withtag(f"bar_{i}")
                if bar_items:
                    self.canvas.itemconfig(bar_items[0], fill="red")
                    self.root.after(200, lambda idx=i: self.restore_bar_color(idx))
        self.root.after(3000, self.blink_warnings)

    def restore_bar_color(self, idx):
        bar_items = self.canvas.find_withtag(f"bar_{idx}")
        if bar_items:
            self.canvas.itemconfig(bar_items[0], fill="#00FF00")