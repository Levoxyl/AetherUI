import tkinter as tk
import random
import time
import math
from datetime import datetime

class HackerInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("CYBER SYSTEMS MONITOR v4.5.0")
        self.root.configure(bg='black')
        self.root.attributes('-fullscreen', True)
        
        # Initialize status values
        self.status_values = [34, 2.4, 12500, 380, 28.4, 42, 67, 124]
        self.status_units = ["°C", "MPa", "RPM", "kPa", "V", "%", "%", "Mbps"]
        
        # Set up the main frame with green border
        self.main_frame = tk.Frame(root, bg='#00FF00', bd=5, relief='solid')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create the interior frame for content
        self.content_frame = tk.Frame(self.main_frame, bg='black')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Create the top section (visualization + status)
        self.top_frame = tk.Frame(self.content_frame, bg='black')
        self.top_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel for network visualization
        self.viz_frame = tk.Frame(self.top_frame, bg='black', bd=2, relief='solid', highlightbackground="#00FF00", highlightthickness=1)
        self.viz_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5), pady=5)
        
        # Title for visualization
        self.viz_title = tk.Label(
            self.viz_frame, 
            text="> GLOBAL NETWORK THREAT MAP",
            font=('Courier', 12, 'bold'),
            fg='#00FF00',
            bg='black',
            anchor='w',
            padx=10
        )
        self.viz_title.pack(fill=tk.X, pady=(5, 0))
        
        # Canvas for visualization
        self.viz_canvas = tk.Canvas(self.viz_frame, bg='black', highlightthickness=0)
        self.viz_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Right panel for binary (tighter)
        self.binary_frame = tk.Frame(self.top_frame, bg='black', bd=2, relief='solid', highlightbackground="#00FF00", highlightthickness=1)
        self.binary_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0), pady=5, ipadx=2)
        
        # Binary title
        self.binary_title = tk.Label(
            self.binary_frame, 
            text="> ENCRYPTED DATA STREAM",
            font=('Courier', 10, 'bold'),
            fg='#00FF00',
            bg='black',
            anchor='w',
            padx=5
        )
        self.binary_title.pack(fill=tk.X, pady=(5, 0))
        
        # Binary display with larger font (12 symbols per line)
        self.binary_text = tk.Text(
            self.binary_frame, 
            bg='black', 
            fg='#00FF00',
            font=('Courier New', 14),
            width=12,  # Increased width for 12 symbols
            height=20,
            insertbackground='#00FF00',
            relief='flat',
            padx=5,
            pady=5,
            wrap=tk.NONE
        )
        self.binary_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.binary_text.config(state=tk.DISABLED)
        
        # Create the bottom section (terminal + hex)
        self.bottom_frame = tk.Frame(self.content_frame, bg='black', height=150)
        self.bottom_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Left terminal panel
        self.terminal_frame = tk.Frame(self.bottom_frame, bg='black', bd=2, relief='solid', highlightbackground="#00FF00", highlightthickness=1)
        self.terminal_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5), pady=5)
        
        # Terminal title
        self.terminal_title = tk.Label(
            self.terminal_frame, 
            text="> SYSTEM TERMINAL [ROOT ACCESS]",
            font=('Courier', 12, 'bold'),
            fg='#00FF00',
            bg='black',
            anchor='w',
            padx=10
        )
        self.terminal_title.pack(fill=tk.X, pady=(5, 0))
        
        # Terminal output (increased height)
        self.terminal_text = tk.Text(
            self.terminal_frame, 
            bg='black', 
            fg='#00FF00',
            font=('Courier', 10),
            height=12,
            insertbackground='#00FF00',
            relief='flat'
        )
        self.terminal_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.terminal_text.config(state=tk.DISABLED)
        
        # Right hex panel (increased height)
        self.hex_frame = tk.Frame(self.bottom_frame, bg='black', bd=2, relief='solid', highlightbackground="#00FF00", highlightthickness=1)
        self.hex_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)
        
        # Hex title
        self.hex_title = tk.Label(
            self.hex_frame, 
            text="> HEX TRANSLATION",
            font=('Courier', 10, 'bold'),
            fg='#00FF00',
            bg='black',
            anchor='w',
            padx=10
        )
        self.hex_title.pack(fill=tk.X, pady=(5, 0))
        
        # Hex display with 12 lines
        self.hex_text = tk.Text(
            self.hex_frame, 
            bg='black', 
            fg='#00FF00',
            font=('Courier', 11),  # Slightly smaller font for more lines
            width=20,
            height=12,
            insertbackground='#00FF00',
            relief='flat',
            padx=10,
            pady=5,
            wrap=tk.NONE
        )
        self.hex_text.pack(fill=tk.BOTH, expand=True)
        self.hex_text.config(state=tk.DISABLED)
        
        # Draw visualization
        self.draw_visualization()
        
        # Add status indicators
        self.draw_status_indicators()
        
        # Initialize visualization variables
        self.radar_angle = 0
        
        # Generate random nodes with better distribution
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
        
        # Terminal command sequences
        self.command_sequences = [
            [
                "nmap -sS -T4 -A -v 192.168.1.0/24",
                "Starting Nmap 7.92 ( https://nmap.org )",
                "Nmap scan report for 192.168.1.1",
                "Host is up (0.005s latency).",
                "Not shown: 995 closed tcp ports (reset)",
                "PORT     STATE SERVICE    VERSION",
                "22/tcp   open  ssh        OpenSSH 8.4p1 Debian 5 (protocol 2.0)",
                "80/tcp   open  http       Apache httpd 2.4.51",
                "443/tcp  open  ssl/http   Apache httpd 2.4.51",
                "8080/tcp open  http-proxy",
                "MAC Address: AA:BB:CC:DD:EE:FF (Router Manufacturer)",
                "Nmap done: 256 IP addresses (12 hosts up) scanned in 8.45 seconds"
            ],
            [
                "aircrack-ng -w rockyou.txt capture.cap -b 00:11:22:33:44:55",
                "Opening capture.cap",
                "Read 15232 packets.",
                "   #  BSSID              ESSID                     Encryption",
                "   1  00:11:22:33:44:55  HomeNetwork               WPA (1 handshake)",
                "Index number of target network? 1",
                "Opening wordlist: rockyou.txt",
                "Testing key no. 10000: 'password123'",
                "Testing key no. 20000: 'letmein'",
                "Testing key no. 30000: 'qwerty'",
                "Testing key no. 123456: 'p@ssw0rd'",
                "KEY FOUND! [ securepass123 ]",
                "Master Key     : AA BB CC DD EE FF 00 11 22 33 44 55 66 77 88 99",
                "Transient Key  : 12 34 56 78 90 AB CD EF 12 34 56 78 90 AB CD EF"
            ],
            [
                "msfconsole -q -x 'use exploit/multi/handler; set payload windows/meterpreter/reverse_tcp; set LHOST 10.0.0.5; set LPORT 4444; run'",
                "[-] ***rting the Metasploit Framework console...-",
                "[*] Using configured payload generic/shell_reverse_tcp",
                "payload => windows/meterpreter/reverse_tcp",
                "LHOST => 10.0.0.5",
                "LPORT => 4444",
                "[*] Started reverse TCP handler on 10.0.0.5:4444",
                "[*] Sending stage (200262 bytes) to 192.168.1.55",
                "[*] Meterpreter session 1 opened (10.0.0.5:4444 -> 192.168.1.55:49283) at 2025-06-15 14:30:22 UTC",
                "meterpreter > sysinfo",
                "Computer        : TARGET-PC",
                "OS              : Windows 10 (10.0 Build 19044)",
                "Architecture    : x64",
                "System Language : en_US",
                "meterpreter > download secret_documents.zip"
            ],
            [
                "hydra -l admin -P passwords.txt ssh://192.168.1.1",
                "Hydra v9.3 (c) 2022 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes.",
                "Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-06-15 14:35:00",
                "[DATA] max 16 tasks per 1 server, overall 16 tasks, 100 login tries (l:1/p:100), ~7 tries per task",
                "[DATA] attacking ssh://192.168.1.1:22/",
                "[22][ssh] host: 192.168.1.1   login: admin   password: admin123",
                "1 of 1 target successfully completed, 1 valid password found",
                "Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-06-15 14:35:15"
            ],
            [
                "sqlmap -u 'http://testphp.vulnweb.com/artists.php?artist=1' --dbs",
                "[*] starting @ 14:38:22 /2025-06-15/",
                "[14:38:22] [INFO] testing connection to the target URL",
                "[14:38:23] [INFO] checking if the target is protected by some kind of WAF/IPS",
                "[14:38:24] [INFO] testing if the target URL content is stable",
                "[14:38:25] [INFO] target URL appears to be dynamic",
                "[14:38:26] [INFO] heuristic (basic) test shows that GET parameter 'artist' might be injectable",
                "[14:38:27] [INFO] testing for SQL injection on GET parameter 'artist'",
                "[14:38:28] [INFO] 'artist' appears to be 'MySQL >= 5.0.12 AND time-based blind' injectable",
                "[14:38:30] [INFO] fetching database names",
                "available databases [5]:",
                "[*] acuart",
                "[*] information_schema",
                "[*] mysql",
                "[*] performance_schema",
                "[*] test"
            ],
            [
                "responder -I eth0 -wrf",
                "[+] Listening for events...",
                "[+] Analyzing for: NETBIOS Name Service (NBNS) UDP",
                "[+] Analyzing for: NETBIOS Name Service (NBNS) TCP",
                "[+] Analyzing for: Link-Local Multicast Name Resolution (LLMNR) TCP",
                "[+] Analyzing for: Link-Local Multicast Name Resolution (LLMNR) UDP",
                "[+] Exiting...",
                "[+] Captured credentials:",
                "    Username: ADMINISTRATOR",
                "    Password: P@ssw0rd123",
                "    Hash: 8846F7EAEE8FB117AD06BDD830B7586C",
                "[+] Saved to /usr/share/responder/logs/SMB-NTLMv2-SSP-10.0.0.15.txt"
            ]
        ]
        self.current_sequence = 0
        self.current_step = 0
        self.sequence_delay = 0
        self.hex_lines = []  # Store hex lines for individual updates
        self.hex_update_times = []  # Track when each hex line was last updated
        
        # Initialize hex display with 12 lines
        for _ in range(12):
            self.hex_lines.append(self.generate_hex_line())
            self.hex_update_times.append(time.time() - random.uniform(0, 5))
        
        # Start animations
        self.update_binary()
        self.update_hex()
        self.update_terminal()
        self.update_status()
        self.update_visualization()
        self.blink_warnings()
        
        # Add exit button
        self.exit_btn = tk.Button(
            self.hex_frame, 
            text="[ EXIT SYSTEM ]", 
            command=root.destroy,
            bg='black', 
            fg='#00FF00',
            relief='solid',
            bd=2,
            font=('Courier', 10, 'bold'),
            padx=10,
            pady=2
        )
        self.exit_btn.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        # Bind ESC key to exit
        root.bind('<Escape>', lambda e: root.destroy())
    

    
    def update_hex(self):
        self.hex_text.config(state=tk.NORMAL)
        
        current_time = time.time()
        updated = False
        
        # Update lines that haven't been updated recently
        for i in range(len(self.hex_lines)):
            if current_time - self.hex_update_times[i] > random.uniform(0.5, 2.0):
                self.hex_lines[i] = self.generate_hex_line()
                self.hex_update_times[i] = current_time
                updated = True
                
                # Occasionally mark as important
                if random.random() < 0.1:
                    self.hex_lines[i] = "!" + self.hex_lines[i]
        
        if updated:
            # Rebuild the hex display
            self.hex_text.delete('1.0', tk.END)
            for i, line in enumerate(self.hex_lines):
                if line.startswith("!"):
                    # Important line in red
                    self.hex_text.insert(tk.END, line[1:] + '\n')
                    self.hex_text.tag_add(f'warning_{i}', f'{i+1}.0', f'{i+1}.end')
                    self.hex_text.tag_config(f'warning_{i}', foreground="red")
                else:
                    # Normal line in green
                    self.hex_text.insert(tk.END, line + '\n')
        
        self.hex_text.config(state=tk.DISABLED)
        self.root.after(100, self.update_hex)  # Very frequent updates
    
    def update_terminal(self):
        self.terminal_text.config(state=tk.NORMAL)
        
        if self.sequence_delay > 0:
            self.sequence_delay -= 1
        else:
            # Add next line of current sequence
            sequence = self.command_sequences[self.current_sequence]
            line = sequence[self.current_step]
            
            # Add prompt for new commands
            if self.current_step == 0:
                prefixes = [
                    "[root@kali] # ",
                    "user@debian $ ",
                    "admin@server > ",
                    "C:\\> ",
                    "PS C:\\Hacking> "
                ]
                prompt = random.choice(prefixes)
                self.terminal_text.insert(tk.END, prompt + line + '\n')
            else:
                self.terminal_text.insert(tk.END, line + '\n')
            
            # Move to next step or next sequence
            self.current_step += 1
            if self.current_step >= len(sequence):
                self.current_step = 0
                self.current_sequence = (self.current_sequence + 1) % len(self.command_sequences)
                self.sequence_delay = 3  # Pause before next command sequence
            
            # Scroll to the end
            self.terminal_text.see(tk.END)
            
            # Remove lines if too many
            line_count = int(self.terminal_text.index('end-1c').split('.')[0])
            if line_count > 30:
                self.terminal_text.delete('1.0', f'{line_count-25}.0')
        
        self.terminal_text.config(state=tk.DISABLED)
        self.root.after(300, self.update_terminal)
    
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
        
        # Clear previous sweep
        self.viz_canvas.delete("sweep")
        self.viz_canvas.delete("node")
        self.viz_canvas.delete("connection")
        self.viz_canvas.delete("node_info")
        
        # Update radar angle
        self.radar_angle = (self.radar_angle + 5) % 360
        rad = math.radians(self.radar_angle)
        
        # Draw radar sweep
        center_x, center_y = w * 0.35, h * 0.5
        radius = min(w, h) * 0.35
        x = center_x + radius * math.cos(rad)
        y = center_y + radius * math.sin(rad)
        self.viz_canvas.create_line(center_x, center_y, x, y, fill='#00FF00', width=2, tags=("viz", "sweep"))
        
        # Draw nodes with 3D perspective
        for node in self.nodes:
            # Apply perspective transformation (z-axis depth)
            scale = 0.5 + node["z"] * 0.5
            nx = center_x + node["x"] * radius * 0.9 * scale
            ny = center_y + node["y"] * radius * 0.9 * scale
            
            # Skip nodes outside radar
            distance = math.sqrt((nx - center_x)**2 + (ny - center_y)**2)
            if distance > radius * 0.95:
                continue
            
            # Determine color based on status
            color = "#00FF00" if node["status"] == "secure" else "#FFFF00" if node["status"] == "warning" else "#FF0000"
            
            # Determine size based on z-depth
            size = 5 + node["z"] * 5
            
            # Draw node
            self.viz_canvas.create_oval(
                nx - size, ny - size,
                nx + size, ny + size,
                fill=color,
                outline=color,
                tags=("viz", "node")
            )
            
            # Draw connection to center with depth effect
            self.viz_canvas.create_line(
                center_x, center_y, nx, ny,
                fill=color,
                width=1 + node["z"],
                dash=(4, 2),
                tags=("viz", "connection")
            )
            
            # Draw node info with depth effect
            self.viz_canvas.create_text(
                nx + 15, ny,
                text=node["ip"],
                anchor="w",
                fill=color,
                font=('Courier', 8 + int(node["z"] * 2)),
                tags=("viz", "node_info")
            )
        
        # Occasionally update node status
        if random.random() < 0.1:
            node = random.choice(self.nodes)
            if node["status"] == "secure":
                node["status"] = "warning" if random.random() < 0.7 else "critical"
            elif node["status"] == "warning":
                node["status"] = "critical" if random.random() < 0.5 else "secure"
            else:
                node["status"] = "warning" if random.random() < 0.3 else "secure"
            node["last_seen"] = time.time()
        
        self.root.after(50, self.update_visualization)
    
    def draw_status_indicators(self):
        # Draw status indicators directly on visualization canvas
        w = self.viz_canvas.winfo_width() or 800
        h = self.viz_canvas.winfo_height() or 500
        if w < 10 or h < 10:  # Canvas not ready
            self.root.after(100, self.draw_status_indicators)
            return
        
        # Create status panel on the right
        self.viz_canvas.create_rectangle(
            w * 0.55, h * 0.02,
            w * 0.98, h * 0.98,
            outline='#00FF00',
            fill='black',
            width=1,
            tags=("viz", "status_panel")
        )
        
        # Panel title
        self.viz_canvas.create_text(
            w * 0.55 + 10, h * 0.02 + 10,
            text="> SYSTEM STATUS", 
            anchor="nw", 
            fill="#00FF00", 
            font=('Courier', 12, 'bold'),
            tags=("viz", "status_title")
        )
        
        # Status indicators
        status_names = [
            "CORE TEMPERATURE",
            "PRESSURE",
            "ROTATION",
            "OIL PRESSURE",
            "VOLTAGE",
            "CPU USAGE",
            "MEMORY USAGE",
            "NETWORK"
        ]
        
        y_offsets = [50, 80, 110, 140, 170, 200, 230, 260]
        
        for i, (name, y_offset) in enumerate(zip(status_names, y_offsets)):
            value = self.status_values[i]
            unit = self.status_units[i]
            x_offset = 20
            y = h * 0.02 + y_offset
            
            self.viz_canvas.create_text(
                w * 0.55 + x_offset, y,
                text=name, 
                anchor="nw", 
                fill="#00FF00", 
                font=('Courier', 10),
                tags=("viz", f"status_{i}")
            )
            
            # Create a progress bar
            bar_width = 200
            bar_height = 12
            bar_x = w * 0.55 + 180
            bar_y = y + 5
            
            # Draw progress bar background
            self.viz_canvas.create_rectangle(
                bar_x, bar_y,
                bar_x + bar_width, bar_y + bar_height,
                outline='#00FF00',
                fill='black',
                width=1,
                tags=("viz", f"bar_bg_{i}")
            )
            
            # Draw progress bar value
            bar_fill_width = bar_width * min(value/100, 1)
            self.viz_canvas.create_rectangle(
                bar_x, bar_y,
                bar_x + bar_fill_width, bar_y + bar_height,
                outline='#00FF00',
                fill='#00FF00',
                width=0,
                tags=("viz", f"bar_{i}")
            )
            
            # Draw value text
            self.viz_canvas.create_text(
                bar_x + bar_width + 10, bar_y - 2,
                text=f"{value}{unit}", 
                anchor="nw", 
                fill="#00FF00", 
                font=('Courier', 9),
                tags=("viz", f"value_{i}")
            )
        
        # Add timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.viz_canvas.create_text(
            w * 0.55 + 10, h * 0.98 - 20,
            text=f"LAST UPDATE: {timestamp}", 
            anchor="sw", 
            fill="#00FF00", 
            font=('Courier', 9),
            tags=("viz", "timestamp")
        )
    
    def update_status(self):
        # Update values with small random fluctuations
        for i in range(8):
            # Apply small random change
            change = random.uniform(-0.5, 0.5)
            self.status_values[i] = max(0, min(self.status_values[i] + change, 100))
            
            # Format value appropriately
            if self.status_units[i] == "RPM":
                display_value = int(self.status_values[i])
            else:
                display_value = round(self.status_values[i], 1)
            
            # Update text display
            tags = f"value_{i}"
            items = self.viz_canvas.find_withtag(tags)
            if items:
                self.viz_canvas.itemconfig(items[0], text=f"{display_value}{self.status_units[i]}")
            
            # Update progress bar
            bar_tags = f"bar_{i}"
            bar_items = self.viz_canvas.find_withtag(bar_tags)
            if bar_items:
                coords = self.viz_canvas.coords(bar_items[0])
                bar_width = 200
                new_width = bar_width * min(self.status_values[i]/100, 1)
                self.viz_canvas.coords(bar_items[0], coords[0], coords[1], coords[0] + new_width, coords[3])
                
                # Change color if needed
                if i == 0 and self.status_values[i] > 40:  # Core temperature
                    self.viz_canvas.itemconfig(bar_items[0], fill="red", outline="red")
                elif i == 1 and self.status_values[i] > 3.0:  # Pressure
                    self.viz_canvas.itemconfig(bar_items[0], fill="red", outline="red")
                elif i == 5 and self.status_values[i] > 80:  # CPU
                    self.viz_canvas.itemconfig(bar_items[0], fill="red", outline="red")
                elif i == 6 and self.status_values[i] > 80:  # Memory
                    self.viz_canvas.itemconfig(bar_items[0], fill="red", outline="red")
                else:
                    self.viz_canvas.itemconfig(bar_items[0], fill="#00FF00", outline="#00FF00")
        
        # Update timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        items = self.viz_canvas.find_withtag("timestamp")
        if items:
            self.viz_canvas.itemconfig(items[0], text=f"LAST UPDATE: {timestamp}")
        
        self.root.after(500, self.update_status)
    
    def blink_warnings(self):
        # Make a random warning blink red
        for i in range(3):
            if random.random() < 0.3:
                bar_items = self.viz_canvas.find_withtag(f"bar_{i}")
                if bar_items:
                    self.viz_canvas.itemconfig(bar_items[0], fill="red", outline="red")
                    self.root.after(200, lambda i=i: self.viz_canvas.itemconfig(
                        self.viz_canvas.find_withtag(f"bar_{i}"), 
                        fill="#00FF00", 
                        outline="#00FF00"
                    ))
        
        self.root.after(3000, self.blink_warnings)

if __name__ == "__main__":
    root = tk.Tk()
    app = HackerInterface(root)
    root.mainloop()