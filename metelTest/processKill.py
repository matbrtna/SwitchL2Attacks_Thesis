import subprocess

def kill_process_by_name(name):
    try:
        result = subprocess.run(["pgrep", "-x", name], capture_output=True, text=True)
        pids = result.stdout.strip().splitlines()

        if not pids:
            print(f"No processes with name: {name} were found.")
            return

  
        subprocess.run(["sudo", "pkill", "-x", name], check=True)

    except Exception as e:
        print(f"Exception during killing {name}: {e}")

def kill_tcpdump():
    try:
        result = subprocess.run(["sudo", "pkill", "-x", "tcpdump"])
        if result.returncode == 0:
            print("tcpdump processes killed.")
        else:
            print("tcpdump was not running.")
    except Exception as e:
        print(f"Error killing tcpdump: {e}")


def kill_macof():
    try:
        subprocess.run(["sudo", "pkill", "-x", "macof"], check=True)
        print("macof processes killed.")
    except subprocess.CalledProcessError:
        print("macof was not running.")
    except Exception as e:
        print(f"Error killing macof: {e}")

def kill_processes():
    kill_macof()
    kill_tcpdump()

