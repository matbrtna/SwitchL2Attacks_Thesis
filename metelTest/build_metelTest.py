#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
from pathlib import Path
import venv

# --- Configuration ---
PROJECT_DIR = Path(__file__).resolve().parent
VENV_DIR = PROJECT_DIR / ".venv"
ENTRY_SCRIPT = PROJECT_DIR / "main.py"
BINARY_NAME = "metelTest"
INSTALL_PATH = Path("/usr/local/bin") / BINARY_NAME
REQ_FILE = PROJECT_DIR / "requirements.txt"
# ---------------------


def run(cmd, **kwargs):
    """Run a command and raise an exception on failure."""
    print(f">>> {' '.join(cmd)}")
    subprocess.run(cmd, check=True, **kwargs)


def main():
    if VENV_DIR.exists():
        print(f"Deleting old venv: {VENV_DIR}")
        shutil.rmtree(VENV_DIR)

    print(f"Creating new virtual environment at {VENV_DIR} ...")
    venv.EnvBuilder(with_pip=True).create(VENV_DIR)

    py_venv = str(VENV_DIR / "bin" / "python")
    pip_venv = str(VENV_DIR / "bin" / "pip")

    print("Updating pip, setuptools and wheel ...")
    run([py_venv, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])

    print("Installing packages from requirements.txt ...")
    run([pip_venv, "install", "-r", str(REQ_FILE)])

    print("Installing PyInstaller ...")
    run([pip_venv, "install", "pyinstaller"])

    print(f"Creating binary '{BINARY_NAME}' ...")
    run([
        py_venv, "-m", "PyInstaller",
        "--onefile",
        "--name", BINARY_NAME,
        "--add-data", "config.json:.",
        "--add-data", "captures:captures",
        "--add-data", "test_configs:test_configs",
        "--add-data", "test_results:test_results",
        str(ENTRY_SCRIPT),
    ])

    src_bin = PROJECT_DIR / "dist" / BINARY_NAME
    print(f"Moving binary to {INSTALL_PATH} (requires sudo) ...")
    run(["sudo", "mv", str(src_bin), str(INSTALL_PATH)])

    print(f"\nDone! You can now run the application with: {BINARY_NAME}")
    print(f"\nTo uninstall, run: sudo rm {INSTALL_PATH}")
    print("To delete build artifacts: rm -rf .venv build dist __pycache__")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"\nBuild error: {e}", file=sys.stderr)
        sys.exit(1)
