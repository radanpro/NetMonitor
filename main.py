from net_monitor import NetMonitorApp
import tkinter as tk

def main():
    root = tk.Tk()
    app = NetMonitorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
