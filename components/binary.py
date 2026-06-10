import tkinter as tk
import random
from tkinter import font as tkfont

class BinaryComponent:
    def __init__(self, frame, root, title_text="", title_style=None, text_style=None):
        self.frame = frame
        self.root = root

        if title_style is None: title_style = {}
        if text_style is None:  text_style = {}

        self.title = tk.Label(self.frame, text=title_text, **title_style)
        self.title.pack(fill=tk.X, pady=(5, 0))
        
        chosen_family = text_style.pop('font_family', 'Courier New')
        self.custom_font = tkfont.Font(family=chosen_family, size=12)

        self.text = tk.Text(
            self.frame, 
            font=self.custom_font,
            bd=0, 
            highlightthickness=0, 
            padx=0, 
            pady=0, 
            wrap=tk.NONE,
            **text_style
        )
        self.text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.text.config(state=tk.DISABLED)
        
        self.text.bind('<Configure>', self.resize_font)
        self.update()

    def resize_font(self, event=None):
        pixel_width = self.text.winfo_width()
        if pixel_width > 50:
            target_char_width = pixel_width // 32
            target_font_size = -int(target_char_width * 1.6)
            
            if target_font_size < -16: target_font_size = -16
            if target_font_size > -9:  target_font_size = -9

            self.custom_font.config(size=target_font_size)

    def generate_line(self):
        pixel_width = self.text.winfo_width()
        chars_needed = pixel_width // 10 if pixel_width > 10 else 30
        return ''.join(random.choice('01') for _ in range(chars_needed))

    def update(self):
        self.text.config(state=tk.NORMAL)
            
        # Insert at END to see movement immediately
        self.text.insert(tk.END, self.generate_line() + '\n')

        total_lines = int(self.text.index('end-1c').split('.')[0])
        
        # Delete from the TOP (1.0 to 2.0) once buffer exceeds 25 lines
        if total_lines > 25:
            self.text.delete('1.0', '2.0')
            total_lines -= 1

        # Red Flash Simulation
        if random.random() < 0.05 and total_lines > 0:
            line_num = random.randint(1, total_lines)
            tag_name = f'err_{random.randint(1,1000)}'
            self.text.tag_add(tag_name, f'{line_num}.0', f'{line_num}.end')
            self.text.tag_config(tag_name, foreground='red')
            self.root.after(500, lambda t=tag_name: self.text.tag_delete(t))
        
        self.text.see(tk.END)
        self.text.config(state=tk.DISABLED)
        self.root.after(150, self.update)