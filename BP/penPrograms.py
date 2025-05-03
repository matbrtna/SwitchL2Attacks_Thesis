import subprocess
import time
import signal
from scapy.all import rdpcap, IP, ARP
import re
from fTester import F_Tester
import netifaces
import sys

def get_ip_address(interface):
    try:
        addresses = netifaces.ifaddresses(interface)
        ip_info = addresses.get(netifaces.AF_INET)
        if ip_info:
            return ip_info[0]['addr']
        else:
            return None
    except ValueError:
        print("Non existing interface selected")
        sys.exit(1)
        return None

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

def runTCPDump(interface):
    own_ip = get_ip_address(interface)
    output_file = "macFloodCapture.pcap"
    process = subprocess.Popen(
        [
            "sudo", "tcpdump", "-i", interface,
            "not", "src", own_ip, "and", "not", "dst", own_ip,
            "-w", output_file
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print(f"Tcpdump started on interface {interface} (PID: {process.pid})")
    return process

def macFlood(interface, client, time_length):
    tcpdump = runTCPDump(interface)
    macof = runMacof(interface)
    time.sleep(10)
    tester = F_Tester(client)
    tester.startTest("tcp100.json")
    time.sleep(time_length)
    print("Terminating processes")
    macof.terminate()
    tcpdump.send_signal(signal.SIGINT)
    time.sleep(10)

def readPcapFiltered(filename):
    packets = rdpcap(filename)
    tcp_packets_info = []
    for pkt in packets:
        if pkt.haslayer("IP") and pkt.haslayer("TCP"):
            ip_layer = pkt["IP"]
            tcp_layer = pkt["TCP"]
            packet_info = {
                "Source IP": ip_layer.src,
                "Destination IP": ip_layer.dst,
                "Source Port": tcp_layer.sport,
                "Destination Port": tcp_layer.dport,
                "Flags": tcp_layer.flags,
                "Seq": tcp_layer.seq,
                "Ack": tcp_layer.ack
            }
            tcp_packets_info.append(packet_info)
    return tcp_packets_info

def getMacFloodResult(interface, client, capture_lenght):
    macFlood(interface, client, capture_lenght)
    try:
        packets = readPcapFiltered("macFloodCapture.pcap")
        print(f"{len(packets)} packets were captured that were not addressed to this device")
        print("The device is not protected")
    except:
        print("Penetration test did not capture any foreign packets")

getMacFloodResult("enx1c860b27ed4b", "192.168.0.202",20)
