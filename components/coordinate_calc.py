import tkinter as tk
import random

class CoordinateCalcComponent:
    def __init__(self, parent, root, data_buffer=None):
        self.parent = parent
        self.root = root
        self.data_buffer = data_buffer  # Shared buffer holding active targets
        
        # Title
        self.title_label = tk.Label(
            parent, 
            text="> COORD INTERCEPT TARGETING", 
            font=('Courier New', 12, 'bold'), 
            fg="#00FF00", 
            bg='black', 
            anchor='w', 
            padx=10
        )
        self.title_label.pack(fill=tk.X, pady=5)
        
        # Display Box
        self.text_area = tk.Text(
            parent, 
            font=('Courier New', 10), 
            fg="#00FF00", 
            bg='black', 
            bd=0, 
            highlightthickness=0
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Animation State tracking per IP
        self.animation_states = {} # Form: {ip: {"step": 0, "lat": X, "lon": Y, "city": Z}}
        
        # Fake locations to pick from randomly
        self.locations = [
            {"city": "UK, London, Ave.Street 325", "lat_prefix": "N51°", "lon_prefix": "W0°"},
            {"city": "USA, New York, Broadway 42", "lat_prefix": "N40°", "lon_prefix": "W74°"},
            {"city": "GER, Berlin, Hauptstr. 12", "lat_prefix": "N52°", "lon_prefix": "E13°"},
            {"city": "JPN, Tokyo, Shibuya 3-11", "lat_prefix": "N35°", "lon_prefix": "E139°"}
        ]
        
        self.update_loop()

    def update_loop(self):
        if self.data_buffer and hasattr(self.data_buffer, 'active_targets'):
            current_ips = self.data_buffer.active_targets  # Expects a list of IP strings
            
            # Clean out dropped targets
            self.animation_states = {ip: state for ip, state in self.animation_states.items() if ip in current_ips}
            
            # Add new targets
            for ip in current_ips:
                if ip not in self.animation_states:
                    loc = random.choice(self.locations)
                    self.animation_states[ip] = {
                        "step": 0,
                        "target_lat": f"{loc['lat_prefix']}{random.randint(10,89)}.{random.randint(1000,9999)}",
                        "target_lon": f"{loc['lon_prefix']}{random.randint(10,179)}.{random.randint(1000,9999)}",
                        "city": loc["city"]
                    }

        # Render display output
        self.text_area.delete("1.0", tk.END)
        
        for ip, state in self.animation_states.items():
            step = state["step"]
            self.text_area.insert(tk.END, f"TARGET IP: {ip}\n")
            
            if step < 10:
                # Stage 1: Brute-forcing / scrambling text matrix animation
                scramble_lat = f"N??°??.{random.randint(1000,9999)}"
                scramble_lon = f"E??°??.{random.randint(1000,9999)}"
                self.text_area.insert(tk.END, f" ├─ COORDS: {scramble_lat} {scramble_lon}\n")
                self.text_area.insert(tk.END, f" └─ LOC: [CALCULATING PARALLAX... {step*10}%]\n\n")
                state["step"] += 1
            else:
                # Stage 2: Locked coordinates resolved
                self.text_area.insert(tk.END, f" ├─ COORDS: {state['target_lat']} {state['target_lon']}\n")
                self.text_area.insert(tk.END, f" └─ LOC: {state['city']}\n\n")

        self.root.after(200, self.update_loop)