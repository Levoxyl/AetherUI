import tkinter as tk
from themes.default import DefaultTheme

def main():
    root = tk.Tk()

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    print(f"Screen Size: {screen_w}x{screen_h}")

    root.title("CYBER MANAGMENT SYSTEM v21.4.5")
    root.configure(bg='black')
    root.attributes('-fullscreen', True)

    app = DefaultTheme(root, screen_w, screen_h)
    root.mainloop()

    def log_resize(event):
        if event.widget.__class__.__name__ == "Tk":
            print(f"Live App Window Size: {event.width}x{event.height}")

    def main():
        root = tk.Tk()
        root.attributes('-fullscreen', True)
        
        root.bind('<Configure>', log_resize)
        
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        
        app = DefaultTheme(root, screen_w, screen_h)
        root.mainloop()

    if __name__ == "__main__":  
        main()