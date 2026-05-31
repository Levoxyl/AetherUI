import random

def generate_hex_line(self):
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

def update_hex(self):
self.hex_text.config(state=tk.NORMAL)

current_time = time.time()
updated = False

for i in range(len(self.hex_lines)):
    if current_time - self.hex_update_times[i] > random.uniform(0.5, 2.0):
        self.hex_lines[i] = self.generate_hex_line()
        self.hex_update_times[i] = current_time
        updated = True
        
        if random.random() < 0.1:
            self.hex_lines[i] = "!" + self.hex_lines[i]

if updated:
    self.hex_text.delete('1.0', tk.END)
    for i, line in enumerate(self.hex_lines):
        if line.startswith("!"):
            self.hex_text.insert(tk.END, line[1:] + '\n')
            self.hex_text.tag_add(f'warning_{i}', f'{i+1}.0', f'{i+1}.end')
            self.hex_text.tag_config(f'warning_{i}', foreground="red")
        else:
            self.hex_text.insert(tk.END, line + '\n')

self.hex_text.config(state=tk.DISABLED)
self.root.after(100, self.update_hex)