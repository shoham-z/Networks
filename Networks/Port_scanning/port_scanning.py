from scapy.layers.inet import IP, TCP
from scapy.all import *


def handle_packet(ip_addr, first_port, last_port):
    response, not_answered = sr(IP(dst=ip_addr)/TCP(sport=666, dport=(first_port, last_port), flags="S"))
    response.summary(lambda s, r: r.sprintf("%TCP.sport% \t %TCP.flags%"))
    return


def bain():
    ip_addr = input("Enter the IPv4 address you want to scan: ")
    first_port = input("Enter the first you want to scan: ")
    last_port = input("Enter the last you want to scan: ")
    handle_packet(ip_addr, first_port, last_port)


def main():
    dst_ip = input("Enter the IPv4 address you want to scan: ")
    src_port = RandShort()
    dst_ports = []
    first_port = int(input("Enter the first you want to scan: "))
    last_port = int(input("Enter the last you want to scan: "))
    port = first_port
    open_ports = []
    while port <= last_port:
        dst_ports.append(port)
        port = port + 1
    for dst_port in dst_ports:
        tcp_connect_scan_resp = sr1(IP(dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags="S"), timeout=10)
        if tcp_connect_scan_resp is None:
            print("Port {} closed".format(dst_port))
        elif tcp_connect_scan_resp.haslayer(TCP):
            if tcp_connect_scan_resp.getlayer(TCP).flags == 0x12:
                send_rst = sr(IP(dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags="AR"), timeout=10)
                print("Port {} open".format(dst_port))
                open_ports.append(dst_port)
            elif tcp_connect_scan_resp.getlayer(TCP).flags == 0x14:
                print("Port {} closed".format(dst_port))
        print("\n")
    print("\nThe open ports at {} are {}".format(dst_ip, open_ports))


if __name__ == "__main__":
    main()
