import tkinter as tk
from themes.default import defaultInterface

def main():
    root = tk.Tk()

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    print(f"Screen Size: {screen_w}x{screen_h}")

    root.title("CYBER MANAGMENT SYSTEM v21.4.5")
    root.configure(bg='black')
    root.attributes('-fullscreen', True)

    app = defaultInterface(root, screen_w, screen_h)
    root.mainloop()

    if __name__ == "__main__":  
        main()