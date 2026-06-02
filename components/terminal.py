import random
import tkinter as tk

def setup_terminal(self):
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

def update_terminal(self):
    self.terminal_text.config(state=tk.NORMAL)
    
    if self.sequence_delay > 0:
        self.sequence_delay -= 1
    else:
        sequence = self.command_sequences[self.current_sequence]
        line = sequence[self.current_step]
        
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
