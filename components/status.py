import tkinter as tk
import random
from datetime import datetime

class StatusComponent:
    def __init__(self, frame, root):
        self.frame = frame
        self.root = root

        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.title = tk.Label(
            self.frame, text="> SYSTEM STATUS DIAGNOSTICS",
            font=('Courier', 12, 'bold'), fg='#00FF00', bg='black', anchor='w', padx=10
        )
        self.title.grid(row=0, column=0, sticky="ew")

        # Dedicated Status Canvas
        self.canvas = tk.Canvas(self.frame, bg='black', highlightthickness=0)
        self.canvas.grid(row=1, column=0, sticky="nsew")

        self.canvas.bind('<Configure>', self.on_resize)

        # State Telemetry Values
        self.status_values = [34, 2.4, 12500, 380, 28.4, 42, 67, 124]
        self.status_units = ["°C", "MPa", "RPM", "kPa", "V", "%", "%", "Mbps"]
        self.status_names = [
            "TEMPERATURE", "PRESSURE", "ROTATION", "OIL PRESSURE",
            "VOLTAGE", "CPU USAGE", "MEMORY USAGE", "NETWORK"
        ]

        self.update()
        self.blink_warnings()

    def on_resize(self, event):
        self.draw(event.width, event.height)

    def draw(self, w, h):
        self.canvas.delete("all")

        # 1. Collision Fix: Relocate Log Tracker to the top margin space
        timestamp_y = 6
        padding_top = 24       # Metrics rows start safely down below the log string
        padding_bottom = 6
        
        # 2. Dynamic vertical slot assignment to handle minimized window scales without text piling
        available_h = max(40, h - padding_top - padding_bottom)
        slot_h = available_h / 8

        # Adaptive text font sizes and bar heights based on available vertical deck height
        if slot_h >= 18:
            font_size = 10
            bar_h = 10
            bar_y_pad = 2
        elif slot_h >= 14:
            font_size = 9
            bar_h = 8
            bar_y_pad = 2
        elif slot_h >= 10:
            font_size = 8
            bar_h = 6
            bar_y_pad = 1
        else:
            font_size = 7
            bar_h = 4
            bar_y_pad = 1

        # 3. Responsive horizontal boundaries
        self.bar_start_x = max(130, w * 0.35)
        self.bar_max_width = max(40, w - self.bar_start_x - 75)
        self.text_x_offset = self.bar_max_width + 8

        # 4. Render Log Tracker at the top allocation gap
        self.canvas.create_text(
            20, timestamp_y, text=f"LOG REFRESH: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
            anchor="nw", fill="#00FF00", font=('Courier', max(8, font_size)), tags=("timestamp", "element")
        )

        # 5. Render Dynamic Metrics Track List
        for i, name in enumerate(self.status_names):
            y_offset = padding_top + i * slot_h
            
            # System Item Name
            self.canvas.create_text(
                20, y_offset, text=name, anchor="nw", 
                fill="#00FF00", font=('Courier', font_size), tags=("element",)
            )
            
            # Progress Track Background Outline
            self.canvas.create_rectangle(
                self.bar_start_x, y_offset + bar_y_pad,
                self.bar_start_x + self.bar_max_width, y_offset + bar_y_pad + bar_h,
                outline='#00FF00', fill='black', width=1, tags=("element",)
            )
            
            # Active Data Meter Fill
            self.canvas.create_rectangle(
                self.bar_start_x, y_offset + bar_y_pad,
                self.bar_start_x, y_offset + bar_y_pad + bar_h,
                outline='#00FF00', fill='#00FF00', width=0, tags=(f"bar_{i}", "element")
            )
            
            # Metric Value String Data
            self.canvas.create_text(
                self.bar_start_x + self.text_x_offset, y_offset, text="", anchor="nw", 
                fill="#00FF00", font=('Courier', font_size), tags=(f"value_{i}", "element")
            )

    def update(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        if w < 10 or h < 10:
            self.root.after(500, self.update)
            return

        if not hasattr(self, 'bar_start_x'):
            self.draw(w, h)

        for i in range(8):
            change = random.uniform(-0.5, 0.5)
            self.status_values[i] = max(0, min(self.status_values[i] + change, 100))
            
            display_value = int(self.status_values[i]) if self.status_units[i] == "RPM" else round(self.status_values[i], 1)
            
            # Update Value Text
            v_items = self.canvas.find_withtag(f"value_{i}")
            if v_items:
                self.canvas.itemconfig(v_items[0], text=f"{display_value}{self.status_units[i]}")
            
            # Update Bar Core Positions while maintaining adaptive dynamic Y metrics
            bar_items = self.canvas.find_withtag(f"bar_{i}")
            if bar_items:
                new_width = self.bar_max_width * min(self.status_values[i]/100, 1)
                coords = self.canvas.coords(bar_items[0])
                self.canvas.coords(bar_items[0], self.bar_start_x, coords[1], self.bar_start_x + new_width, coords[3])
                
                # Dynamic warning alerts coloring thresholds
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