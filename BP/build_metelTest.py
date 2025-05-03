#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
from pathlib import Path
import venv

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
    # 1) Smažeme existující venv, pokud je
    if VENV_DIR.exists():
        print(f"🗑️  Mažu staré venv: {VENV_DIR}")
        shutil.rmtree(VENV_DIR)

    # 2) Vytvoříme nové virtuální prostředí
    print(f"🔨 Vytvářím venv v {VENV_DIR} …")
    venv.EnvBuilder(with_pip=True).create(VENV_DIR)

    # Cesty na python a pip v rámci venv
    py_venv  = str(VENV_DIR / "bin" / "python")
    pip_venv = str(VENV_DIR / "bin" / "pip")

    # 3) Upgrade pip, setuptools, wheel
    print("⚙️  Aktualizuji pip, setuptools a wheel …")
    run([py_venv, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])

    # 4) Generování requirements.txt
    req_file = PROJECT_DIR / "requirements.txt"
    print("📝 Generuji requirements.txt pomocí pip freeze …")
    with req_file.open("w") as f:
        subprocess.run([pip_venv, "freeze"], check=True, stdout=f)

    # 5) Instalace závislostí
    print("📥 Instaluji závislosti z requirements.txt …")
    run([pip_venv, "install", "-r", str(req_file)])

    # 6) Instalace PyInstaller
    print("⚙️  Instalace PyInstalleru …")
    run([pip_venv, "install", "pyinstaller"])

    # 7) Vytvoření binárky
    print(f"🏗️  Sestavuji jednorázovou binárku '{BINARY_NAME}' …")
    run([py_venv, "-m", "PyInstaller", "--onefile", "--name", BINARY_NAME, str(ENTRY_SCRIPT)])

    # 8) Přesun binárky do /usr/local/bin
    src_bin = PROJECT_DIR / "dist" / BINARY_NAME
    print(f"🚚 Přesunu binárku do {INSTALL_PATH} (vyžaduje sudo)…")
    run(["sudo", "mv", str(src_bin), str(INSTALL_PATH)])

    print("\n✅ Hotovo! Nyní můžeš spustit:")
    print(f"   {BINARY_NAME} -t")
    print("\nPokud chceš odinstalovat, smaž:")
    print(f"   sudo rm {INSTALL_PATH}")
    print("a můžeš odstranit venv a artefakty:")
    print("   rm -rf .venv build dist __pycache__ requirements.txt")

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Chyba při spouštění: {e}", file=sys.stderr)
        sys.exit(1)