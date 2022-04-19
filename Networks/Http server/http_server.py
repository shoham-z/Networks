# Ex 4.4 - HTTP Server Shell
# Author: Barak Gonen
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants

# TO DO: import modules
import socket
import os


# TO DO: set constants
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 1000
FIXED_RESPONSE = "Sup bitch?"
HTTP_KEY_WORDS = ["GET", "HTTP/1.1"]
DEFAULT_URL = "/index.html"
FILE_TYPES = ["html", "js", "css", "jpg", "ico"]
TEXT_FILES = ["html", "js", "css"]
IMAGE_FILES = ["jpg", "ico"]
FORBIDDEN_FILES = ["C:\\webroot\\Admin only.html"]


def get_file_data(filename):
    """ Get data from file """
    if filename in FORBIDDEN_FILES:
        pass
    else:
        path_list = filename.split('/')
        filetype = path_list[-1].split('.')[-1]
        file = ''
        if filetype in TEXT_FILES:
            file = open(filename, "r")
        if filetype in IMAGE_FILES:
            file = open(filename, "rb")
        data = file.read()
        file.close()
        return data


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response\
    if resource == '/':
        url = DEFAULT_URL
    else:
        url = resource
    path_list = url.split('/')
    http_header = "HTTP/1.0 200 OK\r\n"
    filetype = path_list[-1].split('.')[-1]
    filename = ''
    data = ''
    # TO DO: extract requested file type from URL (html, jpg etc)
    if filetype == FILE_TYPES[0]:
        http_header = http_header + "Content-Type: text/html; charset=UTF-8\r\n"  # TO DO:generate proper HTTPHeader
        filename = 'C:\\webroot\\' + path_list[-1]
    elif filetype == FILE_TYPES[1]:
        http_header = http_header + "Content-Type: text/javascript; charset=UTF-8\r\n"
        filename = 'C:\\webroot\\js\\' + path_list[-1]
    elif filetype == FILE_TYPES[2]:
        http_header = http_header + "Content-Type: text/css\r\n"
        filename = 'C:\\webroot\\css\\' + path_list[-1]
    elif filetype == FILE_TYPES[3]:
        http_header = http_header + "Content-Type: image/jpeg\r\n"  # TO DO: generate proper jpg header
        filename = 'C:\\webroot\\imgs\\' + path_list[-1]
    elif filetype == FILE_TYPES[4]:
        http_header = http_header + "Content-Type: image/x-icon\r\n"
        filename = 'C:\\webroot\\imgs\\' + path_list[-1]
    # TO DO: handle all other headers
    if os.path.isfile(filename):
        if filename == "C:\\webroot\\index.html":
            http_header = "HTTP/1.0 302 Moved Temporarily\r\nLocation: http://127.0.0.1/uploads/index_backup.html\r\n\r\n"
            print(http_header)
            client_socket.send(http_header.encode())
        else:
            if filename in FORBIDDEN_FILES:
                http_header = "HTTP/1.0 403 Forbidden\r\n"
                client_socket.send(http_header.encode())
                print(http_header)
            else:
                data = get_file_data(filename)
                http_header = http_header + "Content-Length: " + str(len(data)) + "\r\n"
                print(http_header)
                if filetype in TEXT_FILES:
                    http_response = http_header + "\r\n" + data
                    client_socket.send(http_response.encode())
                elif filetype in IMAGE_FILES:
                    http_response = http_header + "\r\n"
                    client_socket.send(http_response.encode())
                    client_socket.send(data)
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
        print(client_request)
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
            break
        else:
            print('Error: Not a valid HTTP request')
            http_header = "HTTP/1.0 500 Internal Server Error\r\n"
            break

    print('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()
