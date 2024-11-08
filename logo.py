import tkinter as tk
from PIL import Image, ImageTk
import os

def animate_text(canvas, text_id, text):
    def update_text(i=0):
        if i <= len(text):
            canvas.itemconfig(text_id, text=text[:i])
            canvas.update()
            canvas.after(100, update_text, i + 1)  # استخدام after لتحديث النص بدلاً من time.sleep
    update_text()

def show_splash_screen():
    splash = tk.Tk()
    splash.overrideredirect(True)
    width = 500
    height = 300  # ارتفاع النافذة الترحيبية
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    splash.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(base_dir, "NetMonitor.png")

    canvas = tk.Canvas(splash, width=width, height=height)
    canvas.pack()

    logo_image = Image.open(logo_path)
    logo_photo = ImageTk.PhotoImage(logo_image)
    canvas.create_image(width / 2, height / 2, image=logo_photo)

    text_id = canvas.create_text(width / 2, height - 50, text="", font=("Helvetica", 24, "bold"), fill="#FFD700")

    splash.update()
    splash.after(3000, splash.destroy)  # استخدام after لإغلاق النافذة بعد 3 ثواني
    splash.mainloop()
