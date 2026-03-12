from setuptools import setup

setup(
    name="metelTest",
    version="0.1.0",
    py_modules=["main"],
    python_requires=">=3.8",
    install_requires=[
        "netifaces>=0.11.0",
        "pandas>=2.2.3",
        "requests>=2.31.0",
        "rich>=14.0.0",
        "scapy>=2.6.1",
    ],
    entry_points={
        "console_scripts": [
            "metelTest = main:main",
        ],
    },
)
