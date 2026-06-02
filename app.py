import tkinter as tk
from visualization import VisualizationComponent
from binary import BinaryComponent
from hex  import HexComponent
from terminal import TerminalComponent

class HackerInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("CYBER SYSTEMS MONITOR v4.5.0")
        self.root.configure(bg='black')
        self.root.attributes('-fullscreen', True)
        
        # Set up the main frame with green border
        self.main_frame = tk.Frame(root, bg='#00FF00', bd=5, relief='solid')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create the interior frame for content
        self.content_frame = tk.Frame(self.main_frame, bg='black')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Create the top section (visualization + binary)
        self.top_frame = tk.Frame(self.content_frame, bg='black')
        self.top_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel for network visualization & status dashboard
        self.viz_frame = tk.Frame(self.top_frame, bg='black', bd=2, relief='solid', highlightbackground="#00FF00", highlightthickness=1)
        self.viz_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5), pady=5)

        # Right panel for binary stream
        self.binary_frame = tk.Frame(self.top_frame, bg='black', bd=2, relief='solid', highlightbackground="#00FF00", highlightthickness=1)
        self.binary_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0), pady=5, ipadx=2)
        
        # Instantiate Components (They handle their own contents completely!)
        self.viz = VisualizationComponent(self.viz_frame, self.root)
        self.binary = BinaryComponent(self.binary_frame, self.root)
        
        # Bind ESC key to exit
        root.bind('<Escape>', lambda e: root.destroy())

if __name__ == "__main__":
    root = tk.Tk()
    app = HackerInterface(root)
    root.mainloop()