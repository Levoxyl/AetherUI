import tkinter as tk
import random

from tkinter import font as tkfont
from colors import Colors

class BinaryComponent:
    def __init__(self, frame, root):
        self.frame = frame
        self.root = root
        self.custom_font = tkfont.Font(family='Courier New', size=12)
        self.text = tk.Text(
            self.frame, bg='black', fg=Colors.NEON_GREEN,
            font=('Courier New', 12),
            insertbackground=Colors.NEON_GREEN, relief='flat',
            padx=0, pady=0, wrap=tk.NONE
        )
        self.text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.text.config(state=tk.DISABLED)
        
        self.update()

    def generate_line(self):

        pixel_width = self.text.winfo_width()
        chars_needed = pixel_width // 10 if pixel_width > 10 else 15

        return ''.join(random.choice('01') for _ in range(chars_needed))

    def update(self):
        self.text.config(state=tk.NORMAL)
          
        pixel_width = self.text.winfo_width()
        if pixel_width > 50:
            target_char_width = pixel_width // 32
            target_font_size = -int(target_char_width * 1.6)
            
            if target_font_size < -16: target_font_size = -16
            if target_font_size > -9:  target_font_size = -9

            self.custom_font.config(size=target_font_size)
            
        self.text.insert('1.0', self.generate_line() + '\n')

        total_lines = int(self.text.index('end-1c').split('.')[0])
        if total_lines > 25:
            self.text.delete('26.0', tk.END)

        # Red Flash Simulation
        if random.random() < 0.05 and total_lines > 0:
            line_num = random.randint(1, min(25, total_lines))
            tag_name = f'err_{random.randint(1,1000)}'
            self.text.tag_add(tag_name, f'{line_num}.0', f'{line_num}.end')
            self.text.tag_config(tag_name, foreground='red')
            self.root.after(500, lambda: self.text.tag_delete(tag_name))
        
        self.text.see(tk.END)
        self.text.config(state=tk.DISABLED)
        self.root.after(150, self.update)