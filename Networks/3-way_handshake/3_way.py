from scapy.all import *
from scapy.layers.inet import IP, TCP

syn_pac = IP(dst="instagram.com")/TCP(dport=80, sport=44444, seq=123, flags='S')
syn_pac.show()
syn_ack_pac = sr1(syn_pac)
syn_ack_pac.show()
ack_pac = IP(dst="instagram.com")/TCP(dport=80, sport=44444, seq=124, ack=syn_ack_pac[TCP].seq+1, flags='A')
send(ack_pac)
