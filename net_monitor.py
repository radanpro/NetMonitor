import os
import psutil
import tkinter as tk
from tkinter import ttk
import sqlite3
import datetime
from PIL import Image, ImageDraw, ImageTk
import pystray
import stat
import sys

class NetMonitorApp:
    def __init__(self, master):
        self.master = master
        master.title("NetMonitor")

        # الحصول على مسار دليل البيانات المحلي للمستخدم
        base_dir = os.path.join(os.getenv('APPDATA'), "NetMonitor")  # استخدام دليل APPDATA
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        self.db_path = os.path.join(base_dir, "net_monitor.db")

        # تحديث مسار الأيقونة
        self.icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "NetMonitor.ico")
        
        # تحقق من وجود قاعدة البيانات أو إنشائها إذا لم تكن موجودة
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

        self.previous_sent, self.previous_recv = self.get_network_usage()
        self.previous_update_time = datetime.datetime.now()

        self.header_frame = tk.Frame(master, bg="#007ACC", pady=10)
        self.header_frame.pack(fill=tk.X)
        self.sent_label = tk.Label(self.header_frame, text="Upload: 0.00 KB", bg="#007ACC", fg="white", font=("Helvetica", 14))
        self.sent_label.pack(side=tk.LEFT, padx=20)
        self.recv_label = tk.Label(self.header_frame, text="Download: 0.00 KB", bg="#007ACC", fg="white", font=("Helvetica", 14))
        self.recv_label.pack(side=tk.LEFT, padx=20)

        self.body_frame = tk.Frame(master)
        self.body_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), foreground="#007ACC")
        style.configure("Treeview", rowheight=25, font=("Helvetica", 10))
        self.tree = ttk.Treeview(self.body_frame, columns=("date", "upload", "download", "total"), show='headings', style="Treeview")
        self.tree.heading("date", text="Date")
        self.tree.heading("upload", text="Upload")
        self.tree.heading("download", text="Download")
        self.tree.heading("total", text="Total")
        self.tree.column("date", anchor=tk.CENTER, width=150)
        self.tree.column("upload", anchor=tk.CENTER, width=150)
        self.tree.column("download", anchor=tk.CENTER, width=150)
        self.tree.column("total", anchor=tk.CENTER, width=150)
        self.scrollbar = ttk.Scrollbar(self.body_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tray_icon = None
        self.update_label()
        self.close_button = tk.Button(master, text="Close", command=self.close_app, bg="red", fg="white", font=("Helvetica", 12, "bold"))
        self.close_button.pack(pady=10)
        self.schedule_auto_update()

        self.master.iconbitmap(self.icon_path)
        self.master.protocol("WM_DELETE_WINDOW", self.hide_window) # التعامل مع إغلاق النافذة الأساسية
        


    def close_app(self):
        if self.tray_icon:
            self.tray_icon.stop()
        sent, recv = self.get_network_usage()
        delta_sent = sent - self.previous_sent
        delta_recv = recv - self.previous_recv
        if delta_sent > 0 and delta_recv > 0:
            self.store_network_usage(delta_sent, delta_recv)
        self.conn.commit()
        self.master.destroy()  # استخدام destroy لإغلاق التطبيق تمامًا

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS daily_network_usage (
                    date TEXT PRIMARY KEY,
                    sent INTEGER,
                    recv INTEGER
                )
            """)

    def get_network_usage(self):
        net_io = psutil.net_io_counters(pernic=True)
        wifi_iface = None
        for iface_name in net_io:
            if "Wi-Fi" in iface_name or "wlan" in iface_name:
                wifi_iface = iface_name
                break
        if wifi_iface and wifi_iface in net_io:
            sent = net_io[wifi_iface].bytes_sent
            recv = net_io[wifi_iface].bytes_recv
            return sent, recv
        else:
            return 0, 0

    def store_network_usage(self, sent, recv):
        current_time = datetime.datetime.now()
        today_date = current_time.strftime("%Y-%m-%d")
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO daily_network_usage (date, sent, recv)
                VALUES (?, ?, ?)
                ON CONFLICT(date) DO UPDATE SET
                sent = sent + excluded.sent,
                recv = recv + excluded.recv
            """, (today_date, sent, recv))
            self.conn.commit()

    def update_label(self):
        sent, recv = self.get_network_usage()
        delta_sent = sent - self.previous_sent
        delta_recv = recv - self.previous_recv
        self.previous_sent = sent
        self.previous_recv = recv
        sent_display = self.format_size(delta_sent) if delta_sent > 0 else "0.00 KB"
        recv_display = self.format_size(delta_recv) if delta_recv > 0 else "0.00 KB"
        self.sent_label.config(text=f"Upload: {sent_display}")
        self.recv_label.config(text=f"Download: {recv_display}")
        if delta_sent > 0 and delta_recv > 0:
            self.store_network_usage(delta_sent, delta_recv)
        # if self.tray_icon is None:
        #     self.create_tray_icon(sent_display, recv_display)
        else:
            self.update_tray_icon(sent_display, recv_display)
        self.master.after(1000, self.update_label)

    def format_size(self, size):
        for unit in ['KB', 'MB', 'GB']:
            size = size / 1024.0
            if size < 1024:
                return f"{size:.2f} {unit}"
        return f"{size:.2f} GB"

    def display_usage(self):
        with self.conn:
            thirty_days_ago = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
            cursor = self.conn.cursor()
            cursor.execute("SELECT date, sent, recv FROM daily_network_usage WHERE date >= ?", (thirty_days_ago,))
            rows = cursor.fetchall()
            for i in self.tree.get_children():
                self.tree.delete(i)
            week_ago = (datetime.datetime.now() - datetime.timedelta(weeks=1)).strftime("%Y-%m-%d")
            total_last_week = self.calculate_total(week_ago)
            total_this_month = self.calculate_total(thirty_days_ago)
            total_last_30_days = sum(row[1] + row[2] for row in rows)
            for row in reversed(rows):
                date, sent, recv = row
                total = sent + recv
                self.tree.insert("", "end", values=(date, self.format_size(sent), self.format_size(recv), self.format_size(total)))
            self.tree.insert("", "end", values=("", "Total last week", self.format_size(total_last_week), ""))
            self.tree.insert("", "end", values=("", "Total this month", self.format_size(total_this_month), ""))
            self.tree.insert("", "end", values=("", "Total last 30 days", self.format_size(total_last_30_days), ""))

    def calculate_total(self, since_date):
        cursor = self.conn.cursor()
        cursor.execute("SELECT SUM(sent) + SUM(recv) FROM daily_network_usage WHERE date >= ?", (since_date,))
        return cursor.fetchone()[0] or 0
    
    def create_tray_icon(self, title):
        image = Image.open(self.icon_path)
        menu = pystray.Menu(pystray.MenuItem('Open NetMonitor', self.show_window))
        self.tray_icon = pystray.Icon("NetMonitor", image, title, menu)
        self.tray_icon.run_detached()

    def update_tray_icon(self, sent_display, recv_display):
        if self.tray_icon:
            self.tray_icon.title = f"Upload: {sent_display} | Download: {recv_display}"

    def schedule_auto_update(self):
        self.display_usage()
        self.master.after(15 * 1000, self.schedule_auto_update)

    def hide_window(self):
        self.master.withdraw()
        if self.tray_icon is None:
            self.create_tray_icon("NetMonitor running in background")
    
    def show_window(self, icon, item):
        self.master.deiconify()
        if self.tray_icon:
            self.tray_icon.stop()
            self.tray_icon = None


