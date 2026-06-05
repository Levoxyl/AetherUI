import random
import time
import tkinter as tk
from tkinter import font as tkfont

from colors import Colors

class HexComponent:
    def __init__(self, frame, root):
        self.frame = frame
        self.root = root
        
        self.title = tk.Label(
            self.frame, 
            text="> SYSTEM HEX DUMP",
            font=('Courier New', 12, 'bold'),
            fg=Colors.NEON_GREEN, bg='black', anchor='w', padx=10
        )
        self.title.pack(fill=tk.X, pady=(5, 0))
        self.custom_font = tkfont.Font(family='Courier New', size=12)

        self.text = tk.Text(
            self.frame, font=self.custom_font, fg=Colors.NEON_GREEN, bg='black', 
            bd=0, highlightthickness=0, padx=0, pady=0, wrap=tk.NONE
        )
        self.text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.text.config(state=tk.DISABLED)
        
        self.update()
            
    def generate_line(self):
        hex_val = ''.join(random.choice('0123456789ABCDEF') for _ in range(8))
        translations = [
            "SYSTEM STABLE", "CORE TEMP: 34°C", "MEM: 67% USED", "CPU: 42% LOAD",
            "NET: 124 MBPS", "ENCRYPTION: AES-256", "SECURITY: LEVEL 5", "THRUST: 42kN",
            "FUEL: 87%", "WARNING! TEMP RISING", "ERROR: SENSOR 12", "ALERT: PRESSURE DROP",
            "CRITICAL: FAN SPEED", "BACKUP SYSTEMS ONLINE", "INTRUSION DETECTED",
            "FIREWALL ACTIVE", "DATA ENCRYPTED", "AUTHENTICATING...", "ACCESS GRANTED",
            "DATA TRANSMISSION COMPLETE", "DECRYPTING FILE...", "ENCRYPTION KEY VERIFIED",
            "UPLOADING PAYLOAD...", "DOWNLOAD COMPLETE", "SYSTEM COMPROMISED"
        ]
        return f"0x{hex_val}  {random.choice(translations)}"

    def update(self):
        self.text.config(state=tk.NORMAL)

        pixel_width = self.text.winfo_width()
        
        if pixel_width > 50:
            target_char_width = pixel_width // 34
            
            # Map char w
            target_font_size = -int(target_char_width * 1.6) 
            
            # Clamp constraints
            if target_font_size < -16: target_font_size = -16
            if target_font_size > -9:  target_font_size = -9
            
            # Update the mutable font object in real-time
            self.custom_font.config(size=target_font_size)

        new_line = self.generate_line()
        if random.random() < 0.1:
            new_line = "!" + new_line
            
        self.text.insert('1.0', (new_line[1:] if new_line.startswith("!") else new_line) + '\n')

        # Read
        current_height = self.text.winfo_height()
        bottom_index = self.text.index(f"@0,{current_height}")
        max_visible_lines = int(bottom_index.split('.')[0])

        if current_height > 10 and max_visible_lines > 15:
            self.text.delete(f"{max_visible_lines + 1}.0", 'end')

        # Warning tag management
        line_count = int(self.text.index('end-1c').split('.')[0])
        if new_line.startswith("!") and line_count > 0:
            tag_id = f"warn_{time.time()}"
            self.text.tag_add(tag_id, '1.0', '1.end')
            self.text.tag_config(tag_id, foreground="red")

        self.text.see(tk.END)
        self.text.config(state=tk.DISABLED)
        self.root.after(150, self.update)