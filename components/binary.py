import tkinter as tk
import random

from colors import Colors

class BinaryComponent:
    def __init__(self, frame, root):
        self.frame = frame
        self.root = root

        self.text = tk.Text(
            self.frame, bg='black', fg=Colors.NEON_GREEN,
            font=('Courier New', 12), width=32, height=32,
            insertbackground=Colors.NEON_GREEN, relief='flat',
            padx=0, pady=0, wrap=tk.NONE
        )
        self.text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.text.config(state=tk.DISABLED)
        
        self.update()

    def generate_line(self):

        pixel_width = self.text.winfo_width()
        chars_needed = pixel_width // 10 if pixel_width > 10 else 30

        return ''.join(random.choice('01') for _ in range(chars_needed))

    def update(self):
        self.text.config(state=tk.NORMAL)
        
        self.text.insert('1.0', self.generate_line() + '\n')

        #Read channel
        current_height = self.text.winfo_height()
        bottom_index = self.text.index(f"@0,{current_height}")
        max_visible_lines = int(bottom_index.split('.')[0])

        if current_height > 10 and max_visible_lines > 15:
            self.text.delete(f"{max_visible_lines + 1}.0", 'end')

        line_count = int(self.text.index('end-1c').split('.')[0])

        # red flash
        if random.random() < 0.05 and line_count > 0:
            line_num = random.randint(1, min(max_visible_lines, line_count))
            tag_name = f'err_{random.randint(1,1000)}'
            self.text.tag_add(tag_name, f'{line_num}.0', f'{line_num}.end')
            self.text.tag_config(tag_name, foreground='red')
            # Schedule tag removal
            self.root.after(500, lambda: self.text.tag_delete(tag_name))
        
        self.text.config(state=tk.DISABLED)
        self.root.after(150, self.update)