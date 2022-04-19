#   Ex. 2.7 template - server side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020

import socket
import protocol
import pyautogui
import os
import subprocess
import shutil


IP = "0.0.0.0"
PHOTO_PATH = r"C:\networks\screenshot.jpg"  # The path + filename where the screenshot at the server should be saved


def check_client_request(cmd):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
    # Use protocol.check_cmd first

    # Then make sure the params are valid
    cmd = cmd.split()
    cmd_length = len(cmd)
    params = []
    is_valid = True
    index = 1
    while index < cmd_length:
        if not cmd[index].exists():
            is_valid = False
        params.append(cmd[index])
        index += 1
    if cmd[0] not in protocol.Commands and not cmd[1].exists():
        is_valid = False
    # (6)
    return is_valid, cmd[0], params


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data

    """
    response = ""
    if command == protocol.Commands[0]:
        cmd = "r'" + params[0] + "'"
        response = os.listdir(cmd)
    if command == protocol.Commands[1]:
        cmd = "r'" + params[0] + "'"
        os.remove(cmd)
        response = "File removed"
    if command == protocol.Commands[2]:
        param1 = "r'" + params[0] + "' "
        param2 = "r'" + params[1] + "'"
        shutil.copy(param1, param2)
        response = "File copied"
    if command == protocol.Commands[3]:
        cmd = "r'" + params[0] + "'"
        subprocess.call(cmd)
        response = "Executing program"
    if command == protocol.Commands[4]:
        image = pyautogui.screenshot()
        image.save(PHOTO_PATH)
        response = "Photo saved"
    if command == protocol.Commands[5]:
        pass
    if command == protocol.Commands[6]:
        return
    return response


def main():
    # open socket with client
    server_socket = socket.socket()
    server_socket.bind((IP, 8820))
    server_socket.listen()
    print("Server is up and running")
    client_socket, client_address = server_socket.accept()
    print("Client connected")
    # handle requests until user asks to exit
    while True:
        # Check if protocol is OK, e.g. length field OK
        valid_protocol, cmd = protocol.get_msg(client_socket)
        if valid_protocol:
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:

                # (6)
                response = handle_client_request(command, params)
                # prepare a response using "handle_client_request"
                packet = protocol.create_msg(response)
                # add length field using "create_msg"
                if command != protocol.Commands[4] and command != protocol.Commands[5] and command != protocol.Commands[6]:
                    client_socket.send(packet.encode())
                # send to client

                if command == protocol.Commands[5]:
                    pass
                    # Send the data itself to the client
                    length = len(response)
                    packet = protocol.create_msg(length)
                    client_socket.send(packet.encode() + response)
                
                if command == protocol.Commands[6]:
                    break
            else:
                # prepare proper error to client
                response = 'Bad command or parameters'
                client_socket.send(protocol.create_msg(response).encode())
                # send to client

        else:
            # prepare proper error to client
            response = 'Packet not according to protocol'
            client_socket.send(protocol.create_msg(response).encode())
            # send to client

            # Attempt to clean garbage from socket
            client_socket.recv(1024)

    # close sockets
    print("Closing connection")
    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()
