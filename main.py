from logo import show_splash_screen
from net_monitor import NetMonitorApp
import tkinter as tk
import psutil
import sys

def close_old_instance():
    """إغلاق النسخة القديمة من التطبيق إذا كانت تعمل."""
    for proc in psutil.process_iter():
        if proc.name() == 'main.exe':
            proc.terminate()  # إنهاء العملية
            proc.wait()  # الانتظار حتى يتم إنهاء العملية

def is_running():
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if proc.info['name'] == 'main.exe':  # اسم ملف التنفيذ
            return True
    return False

def main():
    # if is_running():
    #     # print("NetMonitor is already running. Closing the old instance.")
    #     close_old_instance()
    #     sys.exit(0)

    show_splash_screen()  # عرض النافذة الترحيبية

    root = tk.Tk()
    app = NetMonitorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
