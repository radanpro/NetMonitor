# NetMonitor

![NetMonitor](https://github.com/user-attachments/assets/6f3e8f20-996b-4f62-b351-bb54868e1031)

NetMonitor is a simple program for monitoring upload and download data on the internet, developed using Python and the `tkinter` library. It provides real-time insights into your network's performance, allowing users to easily track data usage and active connections.

### this is the link in sourceforge.net

<a href="https://sourceforge.net/projects/netmonitor24/" target="_blank">NetMonitor</a>

## What is NetMonitor?

NetMonitor is a straightforward tool designed to help you monitor your internet activity. With this tool, you can keep an eye on your data usage and network performance in real-time.

## Why NetMonitor?

NetMonitor helps you understand your internet activity better, enabling you to manage your data usage and spot any unusual patterns that might indicate issues or unauthorized usage.

## Installation

### Download the Latest Release

1. Visit the [Releases](https://github.com/abdulrahmanRadan/NetMonitor/releases) page on GitHub.
2. Download the latest `.exe` installer for Windows.
3. Run the installer and follow the on-screen instructions to complete the installation.

## Usage

After installation, you can run the program by double-clicking the NetMonitor icon on your desktop

## Features

- Real-time monitoring of network connections and bandwidth usage.
- Alerts for unusual activity or connection spikes.
- A clean, modern interface for easy navigation.
- Support for multiple network interfaces.

## How to Use NetMonitor

### Running the Program

Launch NetMonitor by double-clicking the icon on your desktop. The main window will display your current upload and download data.

### Viewing Data

- **Upload**: Shows the amount of data uploaded.
- **Download**: Shows the amount of data downloaded.
- **Total**: Displays the total of uploaded and downloaded data.

### Background Operation

If you close the main window normally, NetMonitor will continue running in the background. You can access it again by clicking on the system tray icon.

### Closing the Program Completely

To completely shut down NetMonitor, click the Close button within the application. This will stop all background processes and exit the application fully.

---

## تعريف NetMonitor

NetMonitor هو برنامج بسيط لمراقبة بيانات التحميل والرفع على الإنترنت، تم تطويره باستخدام لغة Python ومكتبة `tkinter`. يقدم هذا البرنامج نظرة شاملة وفورية عن أداء الشبكة لديك، مما يتيح لك تتبع استهلاك البيانات والاتصالات النشطة بسهولة.

## ما هو NetMonitor؟

NetMonitor هو أداة بسيطة مصممة لمساعدتك في مراقبة نشاط الإنترنت لديك. باستخدام هذه الأداة، يمكنك مراقبة استخدامك للبيانات وأداء الشبكة بشكل لحظي.

## لماذا تستخدم NetMonitor؟

يساعدك NetMonitor على فهم نشاطك على الإنترنت بشكل أفضل، مما يتيح لك إدارة استهلاك البيانات ورصد أي أنماط غير عادية قد تشير إلى مشاكل أو استخدام غير مصرح به.

## طريقة التنصيب

### تحميل أحدث إصدار

1. انتقل إلى صفحة [الإصدارات](https://github.com/abdulrahmanRadan/NetMonitor/releases) على GitHub.
2. قم بتنزيل ملف التثبيت `.exe` الأحدث الخاص بنظام Windows.
3. شغّل ملف التثبيت واتبع التعليمات الظاهرة على الشاشة لإكمال عملية التنصيب.

---

## Cloning the Project (For Developers)

If you want to build the project from source, you can clone it using Git:

```bash
git clone https://github.com/abdulrahmanRadan/NetMonitor.git
cd NetMonitor
```

### Installing Requirements

After cloning, install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### Running the Project

To start the program, run the `main.py` file:

```bash
python main.py
```

### Project Structure

Here’s a quick overview of the main files and folders in the project:

- `main.py`: The entry point of the application, responsible for launching NetMonitor.
- `logo.py`: This file manages the program's logo and may include functions to display or customize the NetMonitor icon in the UI. This is primarily used to handle visual branding elements within the application.

- `setup.py`: This is the setup script used for packaging and installing NetMonitor. Running this script allows developers to install the application as a package on their system, making it easier to manage dependencies and run the program across different environments. To install NetMonitor as a package, use:
- `netmonitor.py`: Contains core components of the application, such as network monitoring and UI modules.
- `requirements.txt`: Lists all Python libraries required to run the project.
- `README.md`: Documentation file with installation instructions, usage guidelines, and contribution information.

### Configuration Options

In `config.json`, you can adjust some settings to customize the application's behavior:

- `update_interval`: Specifies how frequently (in seconds) the network data updates.
- `alert_threshold`: Sets a limit for data spikes, triggering alerts for unusual activity.

### Contributing

We welcome contributions to enhance NetMonitor! If you’d like to contribute, please:

1. Fork the repository and create a new branch for your changes.
2. Make your modifications, ensuring they align with the project's style and structure.
3. Submit a pull request with a description of the changes and their purpose.

### Troubleshooting

If you encounter any issues during setup or while running the application:

- Make sure all dependencies are installed as listed in `requirements.txt`.
- Check if your Python version is compatible (the project supports Python 3.6 and above).
- Review the `logs/` folder for error logs that might provide additional information.

For further assistance, please open an issue in the GitHub repository.
