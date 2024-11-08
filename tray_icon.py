# tray_icon.py

import os
from PIL import Image
import pystray

class TrayIconHandler:
    def __init__(self, icon_path, show_callback):
        self.icon_path = icon_path
        self.tray_icon = None
        self.show_callback = show_callback

    def create_tray_icon(self, title="NetMonitor running in background"):
        image = Image.open(self.icon_path)
        menu = pystray.Menu(pystray.MenuItem('Open NetMonitor', self.show_callback))
        self.tray_icon = pystray.Icon("NetMonitor", image, title, menu)
        self.tray_icon.run_detached()

    def update_tray_icon(self, sent_display, recv_display):
        if self.tray_icon:
            self.tray_icon.title = f"Upload: {sent_display} | Download: {recv_display}"

    def stop_tray_icon(self):
        if self.tray_icon:
            self.tray_icon.stop()
            self.tray_icon = None
