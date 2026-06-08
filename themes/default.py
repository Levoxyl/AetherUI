import tkinter as tk
import os 
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'components'))

from colors import Colors

from visualization import VisualizationComponent
from binary import BinaryComponent
from hex import HexComponent
from terminal import TerminalComponent

class DefaultTheme:
    def __init__(self, root, screen_w, screen_h):
        self.root = root
        self.screen_w = screen_w
        self.screen_h = screen_h
        
        # --- Root Containers ---
        self.main_frame = tk.Frame(root, bg=Colors.NEON_GREEN, bd=5, relief='solid')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.content_frame = tk.Frame(self.main_frame, bg='black')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        

        # Total Weight = 2 (Row 0) + 1 (Row 1) = 3
        # Top row 2/3 = 66%
        # Bot row 1/3 = 33%

        self.content_frame.columnconfigure(0, weight=1) # Left
        # self.content_frame.columnconfigure(1, weight=1) # Right
        self.content_frame.rowconfigure(0, weight=2)    # Up
        self.content_frame.rowconfigure(1, weight=1)    # Low
        
       # --- Top Panel (Network Map & Dashboard) ---
        self.viz_frame = tk.Frame(self.content_frame, bg='black', bd=2, relief='solid', 
                                  highlightbackground=Colors.NEON_GREEN, highlightthickness=1,
                                  )
        self.viz_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.viz_frame.grid_propagate(False)

        # --- Bottom Panel (Terminal / Bin / Hex View Setup) ---
        self.bottom_frame = tk.Frame(self.content_frame, bg='black', bd=2, relief='solid',
                                     highlightbackground=Colors.NEON_GREEN, highlightthickness=1,
                                    )
        self.bottom_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.bottom_frame.grid_propagate(False)
        
        # Lower window
        self.bottom_frame.columnconfigure(0, weight=1, uniform="lower_deck")
        self.bottom_frame.columnconfigure(1, weight=1, uniform="lower_deck")
        self.bottom_frame.columnconfigure(2, weight=1, uniform="lower_deck")
        self.bottom_frame.rowconfigure(0, weight=1)


        self.term_sub_frame = tk.Frame(self.bottom_frame, bg='black')
        self.term_sub_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        
        self.hex_sub_frame = tk.Frame(self.bottom_frame, bg='black')
        self.hex_sub_frame.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)

        self.binary_sub_frame = tk.Frame(self.bottom_frame, bg='black')
        self.binary_sub_frame.grid(row=0, column=2, sticky="nsew", padx=2, pady=2)

        self.viz = VisualizationComponent(self.viz_frame, self.root)
        self.binary = BinaryComponent(self.binary_sub_frame, self.root)
        self.terminal = TerminalComponent(self.term_sub_frame, self.root)
        self.hex = HexComponent(self.hex_sub_frame, self.root)
        
        root.bind('<Escape>', lambda e: root.destroy())