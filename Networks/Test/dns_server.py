from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, UDP
from scapy.all import *

# TO DO: set constants
SERVER_IP = '0.0.0.0'
PORT = 8153
SOCKET_TIMEOUT = 100
FIXED_RESPONSE = "SERVER TIMEOUT"
HTTP_KEY_WORDS = ["GET", "HTTP/1.1"]
DEFAULT_URL = "/index.html"


def create_packet(ip_addr, dns_type):
    if dns_type is None:
        dns_type = 'A'
    dns_packet = IP(dst='8.8.8.8') / UDP(sport=24601, dport=53)
    dns_packet = dns_packet / DNS(qdcount=1, rd=1) / DNSQR(qname=ip_addr, qtype=dns_type)
    return dns_packet


def extract_type_a(ip_addr, pkt):
    responses = []
    for p in pkt:
        if p.haslayer(DNSRR):
            for index in range(p[1][DNS].ancount):
                responses.append(p[DNSRR][index].rdata)
    try:
        reply = '\r\n            '.join(responses)
    except TypeError:
        for response in responses:
            if isinstance(response, bytes):
                responses.remove(response)
        reply = '\r\n            '.join(responses)
    return "Name:       " + ip_addr + "\nAddresses:  " + reply


def extract_type_ptr(ip_addr, pkt):
    lst = ip_addr.split('.')
    lst.remove('in-addr')
    lst.remove('arpa')
    lst.reverse()
    ip_addr = '.'.join(lst)
    domain_name = ''
    try:
        domain_name = pkt[1].ns.rname
    except AttributeError:
        try:
            domain_name = pkt[1][DNSRR].rdata
        except TypeError:
            pass
    if isinstance(domain_name, bytes):
        domain_name = domain_name.decode("utf-8")
    if domain_name.endswith('.'):
        domain_name = domain_name[:-1]
    return "Name:       " + domain_name + "\nAddresses:  " + ip_addr


def handle_packet(ip_addr, dns_type):
    response_packets, unanswered_packets = sr(create_packet(ip_addr, dns_type), verbose=0)
    response = ''
    if dns_type == 'A':
        for pkt in response_packets:
            response = response + extract_type_a(ip_addr, pkt)
    else:
        for pkt in response_packets:
            response = response + extract_type_ptr(ip_addr, pkt)
    return response


def handle_client_request(request, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response\
    http_header = "HTTP/1.0 200 OK\r\n"
    response = ''
    if request.startswith('/reverse'):
        ip = request[9:].split('.')
        ip.reverse()
        ip_address = '.'.join(ip) + ".in-addr.arpa"
        response = handle_packet(ip_address, "PTR")
    else:
        url = request[1:]
        response = handle_packet(url, "A")

    # TO DO: get the url/ip address by dns query
    http_header = http_header + "Content-Length: " + str(len(response)) + "\r\n\r\n" + response
    client_socket.send(http_header.encode())
    return


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    """
    # TO DO: write function
    words = request.split()
    if words[0] == HTTP_KEY_WORDS[0] and words[2] == HTTP_KEY_WORDS[1]:
        return True, words[1]

    else:
        return False, None


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')

    while True:
        # TO DO: insert code that receives client request
        # ...
        client_request = client_socket.recv(1024).decode()
        valid_http, request = validate_http_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(request, client_socket)
            break
        else:
            print('Error: Not a valid HTTP request')
            http_header = "HTTP/1.0 500 Internal Server Error\r\n"
            client_socket.send(http_header.encode())
            break

    print('Closing connection')
    client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    main()
