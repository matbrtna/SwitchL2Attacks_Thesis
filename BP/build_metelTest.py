#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
from pathlib import Path
import venv
import json

# --- KONFIGURACE ---
PROJECT_DIR = Path(__file__).resolve().parent
VENV_DIR     = PROJECT_DIR / ".venv"
ENTRY_SCRIPT = PROJECT_DIR / "main.py"
BINARY_NAME  = "metelTest"
INSTALL_PATH = Path("/usr/local/bin") / BINARY_NAME
# --------------------



def run(cmd, **kwargs):
    """Spustí příkaz, vyhodí výjimku při chybě."""
    print(f">>> {' '.join(cmd)}")
    subprocess.run(cmd, check=True, **kwargs)

def main():
   
    if VENV_DIR.exists():
        print(f"Deleting old venv: {VENV_DIR}")
        shutil.rmtree(VENV_DIR)


    print(f"Creating new {VENV_DIR} …")
    venv.EnvBuilder(with_pip=True).create(VENV_DIR)


    py_venv  = str(VENV_DIR / "bin" / "python")
    pip_venv = str(VENV_DIR / "bin" / "pip")

   
    print("Updating pip, setuptools a wheel …")
    run([py_venv, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])


    req_file = PROJECT_DIR / "requirements.txt"
    print("Genereting requirements.txt pomocí pip freeze …")
    with req_file.open("w") as f:
   
        run([pip_venv, "install", "scapy", "netifaces","pandas","requests"])


    print("Installing packeges from requirements.txt …")
    run([pip_venv, "install", "-r", str(req_file)])


    print("Insatlling PyInstalleru …")
    run([pip_venv, "install", "pyinstaller"])

 
    print(f"Creating binary file '{BINARY_NAME}' …")
    run([
    py_venv, "-m", "PyInstaller",
    "--onefile",
    "--name", BINARY_NAME,
    "--add-data", "config.json:.",
    "--add-data", "captures:captures",
    "--add-data", "test_configs:test_configs",
    "--add-data", "test_results:test_results",
    str(ENTRY_SCRIPT)
    ])



    src_bin = PROJECT_DIR / "dist" / BINARY_NAME
    print(f"Moving binary to: {INSTALL_PATH} (requires sudo)…")
    run(["sudo", "mv", str(src_bin), str(INSTALL_PATH)])

    print("\n Done! You can now run aplication by:")
    print(f"   {BINARY_NAME} ")
    print("\n If you want to unistall aplication, remove:")
    print(f"   sudo rm {INSTALL_PATH}")
    print("you can delete articats:")
    print("   rm -rf .venv build dist __pycache__ requirements.txt")

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"\n Error while running build: {e}", file=sys.stderr)
        sys.exit(1)