import subprocess
import os
import signal

from utils import get_ip_address

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH       = os.path.join(APP_ROOT, "config.json")
CAPTURES_DIR      = os.path.join(APP_ROOT, "captures")
TEST_CONFIGS_DIR  = os.path.join(APP_ROOT, "test_configs")
TEST_RESULTS_DIR  = os.path.join(APP_ROOT, "test_results")


def runMacof(interface):
    try:
        process = subprocess.Popen(
            ["sudo", "macof", "-i", interface],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid,
        )
        print(f"Macof started on interface {interface} (PID: {process.pid})")
        return process
    except Exception as e:
        print(f"Error while starting macof: {e}")
        return None


def runTCPDump(interface, output_file):
    own_ip = get_ip_address(interface)
    output_path = os.path.join(CAPTURES_DIR, output_file)

    process = subprocess.Popen(
        [
            "sudo", "tcpdump", "-i", interface,
            "ip", "and",
            "not", "src", own_ip, "and", "not", "dst", own_ip,
            "-w", output_path
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid,
    )
    print(f"Tcpdump started on interface {interface} (PID: {process.pid})")
    return process


def terminate_process(proc, name="process"):
    """Terminate a subprocess and its entire process group."""
    if proc is None:
        return
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        proc.wait()
    except ProcessLookupError:
        pass
    print(f"{name} ended")
