from setuptools import setup

setup(
    name="metelTest",
    version="0.1.0",
    py_modules=["main"],         # nebo najděte modul(y), které exportujete
    install_requires=[
        "pandas>=2.2.3",
        "rich>=14.0.0",
        "scapy>=2.6.1"

    ],
    entry_points={
        "console_scripts": [
            "metelTest = main:main",
        ],
    },
)