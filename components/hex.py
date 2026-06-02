import random
import time
import tkinter as tk

class HexComponent:
    def __init__(self, frame, root):
        self.frame = frame
        self.root = root
        
        self.lines = [self.generate_line() for _ in range(20)]
        self.update_times = [time.time() for _ in range(20)]
        
        self.title = tk.Label(
            self.frame, 
            text="> SYSTEM HEX DUMP",
            font=('Courier', 12, 'bold'),
            fg='#00FF00', bg='black', anchor='w', padx=10
        )
        self.title.pack(fill=tk.X, pady=(5, 0))
        
        self.text = tk.Text(self.frame, font=('Courier', 10), fg='#00FF00', bg='black', bd=0, highlightthickness=0)
        self.text.pack(fill=tk.BOTH, expand=True)
        self.text.config(state=tk.DISABLED)
        
        self.update()
            
    def generate_line(self):
            hex_val = ''.join(random.choice('0123456789ABCDEF') for _ in range(8))
            translations = [
                "SYSTEM STABLE",
                "CORE TEMP: 34°C",
                "MEM: 67% USED",
                "CPU: 42% LOAD",
                "NET: 124 MBPS",
                "ENCRYPTION: AES-256",
                "SECURITY: LEVEL 5",
                "THRUST: 42kN",
                "FUEL: 87%",
                "WARNING! TEMP RISING",
                "ERROR: SENSOR 12",
                "ALERT: PRESSURE DROP",
                "CRITICAL: FAN SPEED",
                "BACKUP SYSTEMS ONLINE",
                "INTRUSION DETECTED",
                "FIREWALL ACTIVE",
                "DATA ENCRYPTED",
                "AUTHENTICATING...",
                "ACCESS GRANTED",
                "DATA TRANSMISSION COMPLETE",
                "DECRYPTING FILE...",
                "ENCRYPTION KEY VERIFIED",
                "UPLOADING PAYLOAD...",
                "DOWNLOAD COMPLETE",
                "SYSTEM COMPROMISED"
            ]
            return f"0x{hex_val}  {random.choice(translations)}"

    def update(self):
        self.text.config(state=tk.NORMAL)

    current_time = time.time()
    updated = False

    for i in range(len(self.lines)):
        if current_time - self.update_times[i] > random.uniform(0.5, 2.0):
            self.lines[i] = self.generate_line()
            self.update_times[i] = current_time
            updated = True
            
            if random.random() < 0.1:
                self.lines[i] = "!" + self.lines[i]

    if updated:
        self.text.delete('1.0', tk.END)
        for i, line in enumerate(self.lines):
            if line.startswith("!"):
                self.text.insert(tk.END, line[1:] + '\n')
                self.text.tag_add(f'warning_{i}', f'{i+1}.0', f'{i+1}.end')
                self.text.tag_config(f'warning_{i}', foreground="red")
            else:
                self.text.insert(tk.END, line + '\n')

    self.text.config(state=tk.DISABLED)
    self.root.after(100, self.update)