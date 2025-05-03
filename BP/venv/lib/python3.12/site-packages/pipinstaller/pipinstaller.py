# my_package/installer.py

import requests
import subprocess

def search_package(package_name):
    url = f"https://pypi.org/project/{package_name}/"
    response = requests.get(url)
    return response.status_code == 200

def install_package(package_name):
    subprocess.run(["pip", "install", package_name])

def install_from_requirements(file_path):
    with open(file_path, "r") as file:
        packages = file.readlines()
    
    for package in packages:
        package = package.strip()
        if search_package(package):
            print(f"Installing {package}...")
            install_package(package)
        else:
            print(f"{package} not found on PyPI.")
