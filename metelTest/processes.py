import subprocess
from utils import get_ip_address
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH       = os.path.join(APP_ROOT, "config.json")
CAPTURES_DIR      = os.path.join(APP_ROOT, "captures")
TEST_CONFIGS_DIR  = os.path.join(APP_ROOT, "test_configs")
TEST_RESULTS_DIR  = os.path.join(APP_ROOT, "test_results")


def runMacof(interface):
    try:
        process = subprocess.Popen(
            ["sudo", "macof", "-i", interface],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        print(f"Macof started on interface {interface} (PID: {process.pid})")
        return process
    except Exception as e:
        print(f"Error while starting macof: {e}")

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
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print(f"Tcpdump started on interface {interface} (PID: {process.pid})")
    return process
