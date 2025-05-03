import subprocess

def sniff_packets(client, server):
    process = subprocess.Popen(
        [
            "sudo", "tcpdump", "-i", "wlp59s0", "-n", "-l",
            "src", client, "and", "dst", server
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        universal_newlines=True
    )
    for line in process.stdout:
        print(line)

sniff_packets("192.168.0.202","192.168.0.204")