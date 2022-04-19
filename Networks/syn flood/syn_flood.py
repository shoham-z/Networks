from scapy.layers.inet import IP, TCP
from scapy.all import *

# flags hex values
SYN = 0x02
ACK = 0x10
# the attacked ip
ATTACKED_IP = "69.90.200.90"

# file to write suspects ips
SUSPECTS_FILE = open("Dangerous_ips.txt", "w")

# open the sniffing file
pcapFile = rdpcap("SynFloodSample.pcap")

SUSPECTS = {}

# who sends SYNs too fast
MAX_DELTA = 0.0005
SYN_PACKETS = {}
for pkt in pcapFile:
    if TCP in pkt:
        if pkt[TCP].flags == SYN:
            if pkt[IP].src in SYN_PACKETS:
                delta = float(pkt.time) - float(SYN_PACKETS[pkt[IP].src])
                if delta <= MAX_DELTA:
                    SUSPECTS[pkt[IP].src] = pkt.time
                else:
                    SYN_PACKETS[pkt[IP].src] = pkt.time
            else:
                SYN_PACKETS[pkt[IP].src] = float(pkt.time)

# who got SYN ACK but didn't answer ACK
SYN_ACK_PACKETS = {}
for pkt in pcapFile:
    if TCP in pkt:
        pkt_ip = pkt[IP].src
        if pkt[TCP].flags == SYN + ACK:
            if pkt_ip in SYN_ACK_PACKETS:
                if pkt_ip in SUSPECTS:
                    pass  # what do I do in that case
                else:
                    SUSPECTS[pkt_ip] = pkt.time
            else:
                SYN_ACK_PACKETS[pkt_ip] = pkt.time

# write suspect ips to file
for ip in SUSPECTS:
    SUSPECTS_FILE.write(ip + '\n')
