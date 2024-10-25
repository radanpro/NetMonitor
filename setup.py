from setuptools import setup, find_packages

setup(
    name='NetMonitor',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[
        'Pillow==11.0.0',
        'psutil==6.1.0',
        'pystray==0.19.5',
        'setuptools==74.1.1'
    ],
    entry_points={
        'console_scripts': [
            'netmonitor = net_monitor:main',
        ],
    },
)
