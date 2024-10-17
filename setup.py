from setuptools import setup, find_packages

setup(
    name='NetMonitor',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'psutil',
        'tkinter',
    ],
    entry_points={
        'console_scripts': [
            'netmonitor = net_monitor:main',
        ],
    },
)
