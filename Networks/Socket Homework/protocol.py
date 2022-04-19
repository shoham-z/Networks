"""EX 2.6 protocol implementation
   Author: shoham zeharya
   Date: 24.10.21
"""
import random
from _datetime import datetime
LENGTH_FIELD_SIZE = 2
PORT = 8820


def check_cmd(data):
    """Check if the command is defined in the protocol (e.g RAND, NAME, TIME, EXIT)"""
    if data != "RAND" and data != "WHORU" and data != "TIME" and data != "EXIT":
        return False
    return True


def create_msg(data):
    """Create a valid protocol message, with length field"""
    if len(data) < 100:
        return str(len(data)).zfill(2) + data


def get_msg(my_socket):
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """
    length = my_socket.recv(LENGTH_FIELD_SIZE).decode()
    if int(length) < 100:
        return True, my_socket.recv(int(length)).decode()
    else:
        return False, "Error"


def create_server_rsp(cmd):
    """Based on the command, create a proper response"""
    if cmd == "TIME":
        now = datetime.now()
        return now.strftime("%a %b %d %H:%M:%S %Y")
    if cmd == "WHORU":
        return "YOU"
    if cmd == "RAND":
        return str(random.randint(1, 10))
    return "Server response"
