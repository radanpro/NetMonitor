import psutil
import tkinter as tk


def get_network_usage():
    net_io = psutil.net_io_counters()
    return net_io.bytes_sent, net_io.bytes_recv


class NetMonitorApp:
    def __init__(self, master):
        self.master = master
        master.title("NetMonitor")

        self.sent_label = tk.Label(master, text="Upload: 0.00 MB")
        self.sent_label.pack()

        self.recv_label = tk.Label(master, text="Download: 0.00 MB")
        self.recv_label.pack()

        self.update_label()

    def update_label(self):
        sent, recv = get_network_usage()
        self.sent_label.config(text=f"Upload: {sent / 1024 / 1024:.2f} MB")
        self.recv_label.config(text=f"Download: {recv / 1024 / 1024:.2f} MB")
        self.master.after(1000, self.update_label)  # تحديث كل ثانية


if __name__ == "__main__":
    root = tk.Tk()
    app = NetMonitorApp(root)
    root.mainloop()
