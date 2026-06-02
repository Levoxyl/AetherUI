import tkinter as tk
import random

from colors import Colors

class BinaryComponent:
    def __init__(self, frame, root):
        self.frame = frame
        self.root = root

        self.text = tk.Text(
            self.frame, bg='black', fg=Colors.NEON_GREEN,
            font=('Courier New', 14), width=12, height=20,
            insertbackground=Colors.NEON_GREEN, relief='flat',
            padx=5, pady=5, wrap=tk.NONE
        )
        self.text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.text.config(state=tk.DISABLED)
        
        self.update()

    def generate_line(self):
        return ''.join(random.choice('01') for _ in range(12))

    def update(self):
        self.text.config(state=tk.NORMAL)
        self.text.insert('1.0', self.generate_line() + '\n')

        line_count = int(self.text.index('end-1c').split('.')[0])
        if line_count > 20:
            self.text.delete('20.0', 'end')
        
        # red flash
        if random.random() < 0.05:
            line_num = random.randint(1, min(20, line_count))
            tag_name = f'err_{random.randint(1,1000)}'
            self.text.tag_add(tag_name, f'{line_num}.0', f'{line_num}.end')
            self.text.tag_config(tag_name, foreground='red')
            # Schedule tag removal
            self.root.after(500, lambda: self.text.tag_delete(tag_name))
        
        self.text.config(state=tk.DISABLED)
        self.root.after(150, self.update)