#   Ex. 2.7 template - protocol


LENGTH_FIELD_SIZE = 4
PORT = 8820
Commands = ['DIR', 'DELETE', 'COPY', 'EXECUTE', 'TAKE_SCREENSHOT', 'SEND_SCREENSHOT', 'EXIT']


def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not
    """
    cmd = data.split()
    if len(cmd) > 1:
        if cmd[0] in Commands and cmd[1] != '\0':
            return True
        else:
            return False
    if cmd[0] == Commands[5] or cmd[0] == Commands[6]:
        return True
    return False


def create_msg(data):
    """
    Create a valid protocol message, with length field
    """
    message = data
    if data.isnumeric():
        message = str(len(data) + data)
    else:
        while len(data) >= 10000:
            message = str(len(message)).zfill(LENGTH_FIELD_SIZE) + data
        message = str(len(message)).zfill(LENGTH_FIELD_SIZE) + data
    return message


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """
    length = my_socket.recv(LENGTH_FIELD_SIZE).decode()
    if length.isnumeric():
        while len(length) >= LENGTH_FIELD_SIZE:
            my_socket.recv(int(length)).decode()
        return True, my_socket.recv(int(length)).decode()
    else:
        return False, "Error"
