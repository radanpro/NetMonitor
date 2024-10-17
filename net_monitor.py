import psutil
import tkinter as tk
from tkinter import ttk
import sqlite3
import datetime

class NetMonitorApp:
    def __init__(self, master):
        self.master = master
        master.title("NetMonitor")

        # Header
        self.header_frame = tk.Frame(master, bg="#007ACC", pady=10)
        self.header_frame.pack(fill=tk.X)

        self.sent_label = tk.Label(self.header_frame, text="Upload: 0.00", bg="#007ACC", fg="white", font=("Helvetica", 14))
        self.sent_label.pack(side=tk.LEFT, padx=20)

        self.recv_label = tk.Label(self.header_frame, text="Download: 0.00", bg="#007ACC", fg="white", font=("Helvetica", 14))
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

        self.update_label()
        self.display_usage()

        # Update Button
        self.update_button = tk.Button(master, text="Update Data", command=self.display_usage, bg="#007ACC", fg="white", font=("Helvetica", 12, "bold"))
        self.update_button.pack(pady=10)

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
        return net_io.bytes_sent, net_io.bytes_recv

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
        sent, recv = self.get_network_usage()
        self.store_network_usage(sent, recv)
        self.sent_label.config(text=f"Upload: {self.format_size(sent)}")
        self.recv_label.config(text=f"Download: {self.format_size(recv)}")
        self.master.after(1000, self.update_label)

    def format_size(self, size):
        """Helper function to format size in KB, MB, or GB."""
        for unit in ['b', 'B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024

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

if __name__ == "__main__":
    root = tk.Tk()
    app = NetMonitorApp(root)
    root.mainloop()
