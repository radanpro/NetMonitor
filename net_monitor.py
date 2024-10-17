import psutil
import tkinter as tk
from tkinter import ttk
import sqlite3
import datetime
from PIL import Image, ImageDraw  # لتوليد أيقونة شريط المهام
import pystray  # مكتبة لعرض الأيقونة في شريط المهام

class NetMonitorApp:
    def __init__(self, master):
        self.master = master
        master.title("NetMonitor")
        # زر لتحديث البيانات
        self.update_button = tk.Button(master, text="Update Data", command=self.display_usage, bg="#007ACC", fg="white", font=("Helvetica", 12, "bold"))
        self.update_button.pack(pady=10)

        # تخزين القيم السابقة للرفع والتنزيل
        self.previous_sent = 0
        self.previous_recv = 0

        # Header
        self.header_frame = tk.Frame(master, bg="#007ACC", pady=10)
        self.header_frame.pack(fill=tk.X)

        self.sent_label = tk.Label(self.header_frame, text="Upload: 0.00 KB", bg="#007ACC", fg="white", font=("Helvetica", 14))
        self.sent_label.pack(side=tk.LEFT, padx=20)

        self.recv_label = tk.Label(self.header_frame, text="Download: 0.00 KB", bg="#007ACC", fg="white", font=("Helvetica", 14))
        self.recv_label.pack(side=tk.LEFT, padx=20)

        # Body
        self.body_frame = tk.Frame(master)
        self.body_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(self.body_frame, columns=("date", "upload", "download", "total"), show='headings')
        self.tree.heading("date", text="Date")
        self.tree.heading("upload", text="Upload")
        self.tree.heading("download", text="Download")
        self.tree.heading("total", text="Total")

        self.tree.column("date", anchor=tk.CENTER)
        self.tree.column("upload", anchor=tk.CENTER)
        self.tree.column("download", anchor=tk.CENTER)
        self.tree.column("total", anchor=tk.CENTER)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.body_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.conn = sqlite3.connect("net_monitor.db")
        self.create_table()

        # إضافة أيقونة شريط المهام
        self.tray_icon = None  # نبدأ بدون أيقونة

        # عرض القيم الأولية
        self.update_label()

        # Update Button
        self.update_button = tk.Button(master, text="Update Data", command=self.display_usage, bg="#007ACC", fg="white", font=("Helvetica", 12, "bold"))
        self.update_button.pack(pady=10)
        # زر لإغلاق البرنامج
        self.close_button = tk.Button(master, text="Close", command=self.close_app, bg="red", fg="white", font=("Helvetica", 12, "bold"))
        self.close_button.pack(pady=10)

    def close_app(self):
        """دالة لإغلاق البرنامج بالكامل مع إزالة رمز شريط النظام."""
        if hasattr(self, 'tray_icon'):
            self.tray_icon.stop()  # إزالة رمز شريط النظام

        self.master.quit()  # إغلاق نافذة التطبيق

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
        net_io = psutil.net_io_counters()
        sent = net_io.bytes_sent
        recv = net_io.bytes_recv
        return sent, recv

    def store_network_usage(self, sent, recv):
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO daily_network_usage (date, sent, recv) 
                VALUES (?, ?, ?)
                ON CONFLICT(date) DO UPDATE SET
                sent = sent + excluded.sent,
                recv = recv + excluded.recv
            """, (today_date, sent, recv))

    def update_label(self):
        # احصل على القيم الحالية
        sent, recv = self.get_network_usage()

        # حساب الفروقات مع القيم السابقة
        delta_sent = sent - self.previous_sent
        delta_recv = recv - self.previous_recv

        # تحديث القيم السابقة
        self.previous_sent = sent
        self.previous_recv = recv

        # إذا كان الفرق سالب أو الشبكة متوقفة، نظهر 0
        sent_display = self.format_size(delta_sent) if delta_sent > 0 else "0.00 KB"
        recv_display = self.format_size(delta_recv) if delta_recv > 0 else "0.00 KB"

        # تحديث القيم في الواجهة (Upload و Download)
        self.sent_label.config(text=f"Upload: {sent_display}")
        self.recv_label.config(text=f"Download: {recv_display}")

        # أضف القيم إلى قاعدة البيانات
        self.store_network_usage(delta_sent, delta_recv)

        # تأكد من وجود أيقونة شريط المهام قبل محاولة التحديث
        if self.tray_icon is None:
            self.create_tray_icon(sent_display, recv_display)
        else:
            self.update_tray_icon(sent_display, recv_display)

        # حدث البيانات كل 3 ثوانٍ
        self.master.after(1000, self.update_label)

    def format_size(self, size):
        """تحويل البيانات إلى الوحدات المناسبة (كيلوبايت، ميغابايت، غيغابايت)."""
        for unit in ['KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} GB"

    def display_usage(self):
        with self.conn:
            thirty_days_ago = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT date, sent, recv FROM daily_network_usage WHERE date >= ?
            """, (thirty_days_ago,))
            rows = cursor.fetchall()

            # Clear previous data
            for i in self.tree.get_children():
                self.tree.delete(i)

            week_ago = (datetime.datetime.now() - datetime.timedelta(weeks=1)).strftime("%Y-%m-%d")
            total_last_week = self.calculate_total(week_ago)
            total_this_month = self.calculate_total(thirty_days_ago)
            total_last_30_days = sum(row[1] + row[2] for row in rows)

            for row in rows:
                date, sent, recv = row
                total = sent + recv
                self.tree.insert("", "end", values=(date, self.format_size(sent), self.format_size(recv), self.format_size(total)))

            self.tree.insert("", "end", values=("", "Total last week", self.format_size(total_last_week), ""))
            self.tree.insert("", "end", values=("", "Total this month", self.format_size(total_this_month), ""))
            self.tree.insert("", "end", values=("", "Total last 30 days", self.format_size(total_last_30_days), ""))

    def calculate_total(self, since_date):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT SUM(sent) + SUM(recv) FROM daily_network_usage WHERE date >= ?
        """, (since_date,))
        return cursor.fetchone()[0] or 0

    def create_tray_icon(self, sent_display, recv_display):
        """إنشاء أيقونة شريط المهام."""
        # توليد أيقونة فارغة
        image = Image.new('RGB', (64, 64), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, 64, 64), fill="blue")

        # إنشاء الأيقونة
        self.tray_icon = pystray.Icon("NetMonitor", image, "NetMonitor", menu=None)
        self.update_tray_icon(sent_display, recv_display)
        self.tray_icon.run_detached()

    def update_tray_icon(self, sent_display, recv_display):
        """تحديث أيقونة شريط المهام لعرض الرفع والتنزيل."""
        self.tray_icon.title = f"Upload: {sent_display} | Download: {recv_display}"

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = NetMonitorApp(root)
#     root.mainloop()
