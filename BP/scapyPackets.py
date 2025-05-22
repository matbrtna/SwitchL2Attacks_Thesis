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




# syn_ack=sendSynWithVlan(1)
# syn_ack=sendSynWithoutVlan()
# print(syn_ack)



# 2. TCP ACK
# ack = (
#     Ether(src=my_mac, dst=target_mac) /
#     Dot1Q(vlan=vlan_id) /
#     IP(src=my_ip, dst=target_ip) /
#     TCP(sport=sport, dport=target_port, flags='A',
#         seq=syn[TCP].seq + 1, ack=syn_ack[TCP].seq + 1)
# )
# sendp(ack, iface=iface, verbose=False)

# # 3. HTTP GET Request
# http_payload = (
#     "GET / HTTP/1.1\r\n"
#     f"Host: {target_ip}\r\n"
#     "Connection: close\r\n\r\n"
# )

# get = (
#     Ether(src=my_mac, dst=target_mac) /
#     Dot1Q(vlan=vlan_id) /
#     IP(src=my_ip, dst=target_ip) /
#     TCP(sport=sport, dport=target_port, flags='PA',
#         seq=syn[TCP].seq + 1, ack=syn_ack[TCP].seq + 1) /
#     Raw(load=http_payload)
# )

# # 4. Získání odpovědi
# def filter_response(pkt):
#     return (
#         pkt.haslayer(IP)
#         and pkt[IP].src == target_ip
#         and pkt[IP].dst == my_ip
#         and pkt.haslayer(TCP)
#         and pkt[TCP].sport == target_port
#         and pkt[TCP].dport == sport
#     )

# print("Waiting for HTTP response...")
# response = sniff(iface=iface, lfilter=filter_response, timeout=5)
# sendp(get, iface=iface, verbose=False)


# # Zobrazit odpověď
# for pkt in response:
#     if pkt.haslayer(Raw):
#         print(pkt[Raw].load.decode(errors="ignore"))