import tkinter as tk
import random

def update_binary(self):
        self.binary_text.config(state=tk.NORMAL)
        self.binary_text.insert('1.0', self.generate_binary_line() + '\n')
        
        # Remove last ln if too many
        line_count = int(self.binary_text.index('end-1c').split('.')[0])
        if line_count > 20:
            self.binary_text.delete('20.0', 'end')
        
        # Occasionally make a line red
        if random.random() < 0.05:
            line_num = random.randint(1, min(20, line_count))
            self.binary_text.tag_add('error', f'{line_num}.0', f'{line_num}.end')
            self.binary_text.tag_config('error', foreground='red')
            self.root.after(500, lambda: self.binary_text.tag_remove('error', f'{line_num}.0', f'{line_num}.end'))
        
        self.binary_text.config(state=tk.DISABLED)
        self.root.after(150, self.update_binary)

        def generate_binary_line(self):
    return ''.join(random.choice('01') for _ in range(12))
