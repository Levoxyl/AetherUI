import tkinter as tk
from themes.default import DefaultTheme

def log_resize(event):
    if event.widget.__class__.__name__ == "Tk":
        print(f"Live App Window Size: {event.width}x{event.height}")

def main():
    root = tk.Tk()

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    print(f"Monitor Screen Size: {screen_w}x{screen_h}")

    root.title("CYBER MANAGEMENT SYSTEM v21.4.5")
    root.configure(bg='black')
    
    root.attributes('-fullscreen', False)
    
    window_w = 1200
    window_w = min(1200, int(screen_w * 0.8))
    window_h = min(800, int(screen_h * 0.8))
    
    # Math to center it perfectly on your screen
    center_x = int((screen_w - window_w) / 2)
    center_y = int((screen_h - window_h) / 2)
    
    root.geometry(f"{window_w}x{window_h}+{center_x}+{center_y}")
    
    root.bind('<Configure>', log_resize)

    app = DefaultTheme(root, window_w, window_h)
    root.mainloop()

if __name__ == "__main__":  
    main()