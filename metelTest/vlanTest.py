from scapy.all import Ether, Dot1Q, IP, ICMP, sendp,srp1


iface = "enx1c860b27ed4b"     
vlan_id = 12               
src_ip = "192.168.0.54"        
dst_ip = "192.168.0.204"        


frame = (
    Ether(dst="ff:ff:ff:ff:ff:ff") /  
    Dot1Q(vlan=vlan_id) /
    IP(src=src_ip, dst=dst_ip) /
    ICMP()
)
response = srp1(frame, iface=iface, timeout=2, verbose=True)


if response:
    print("Odpověď přijata od:", response[IP].src)
    print("Paket obsahuje:", response.summary())
else:
    print("Žádná odpověď (timeout)")