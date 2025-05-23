from scapy.all import sniff
from scapy.all import *
from scapy.layers.l2 import getmacbyip
from scapy.layers.l2 import Ether, Dot1Q
from scapy.layers.inet import IP, TCP
import random

target_ip = "192.168.0.202"
target_port = 80
iface = "enx1c860b27ed4b"  
my_ip = get_if_addr(iface)
my_mac = get_if_hwaddr(iface)
target_mac = getmacbyip(target_ip)

sport = random.randint(1024, 65535)



def sendSynWithVlan(vlanID):
    syn=createSynWithVlan(vlanID)
    syn_ack = srp1(syn, iface=iface, timeout=2, verbose=False)

    if not syn_ack or not syn_ack.haslayer(TCP) or syn_ack[TCP].flags != 'SA':
        print(syn_ack)
        return False
    else:
        return syn_ack


def sendSynWithoutVlan():
    syn=createSynWithoutVlan()
    syn_ack = srp1(syn, iface=iface, timeout=2, verbose=False)
    if not syn_ack or not syn_ack.haslayer(TCP) or syn_ack[TCP].flags != 'SA':
        return False
    else:
        return syn_ack


def createSynWithoutVlan():
    syn = (
    Ether(src=my_mac, dst=target_mac) /
    IP(src=my_ip, dst=target_ip) /
    TCP(sport=sport, dport=target_port, flags='S', seq=1000)
    )   
    return syn

def createSynWithVlan(vlanID):
    syn = (
    Ether(src=my_mac, dst=target_mac) /
    Dot1Q(vlan=vlanID) /
    IP(src=my_ip, dst=target_ip) /
    TCP(sport=sport, dport=target_port, flags='S', seq=1000)
    )   
    return syn




def tryVlan(vlanID):
    print(f"Started vlan test with vlan tag: {vlanID}")

    print("Testing communication with the wanted server without vlan tag")
    syn_ack=sendSynWithoutVlan()
    if syn_ack!=False:
        print(f"Communication without vlan tag is working")
    else: 
        print("Communication without vlan tag is not working, check your connection to the device")
    
    print("Testing communication with the wanted server with vlan tag")
    syn_ack=sendSynWithVlan(vlanID)
    if syn_ack!=False:
        print(f"Communication without vlan tag is working")
    else: 
        print("Communication without vlan tag is not working, check your connection to the device")

