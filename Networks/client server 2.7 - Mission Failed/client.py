#   Ex. 2.7 template - client side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020


import socket
import protocol


IP = "127.0.0.1"
SAVED_PHOTO_LOCATION = r"C:\networks\Screenshot_from_server.jpg"  # The path + filename where the copy of the screenshot at the client should be saved


def handle_server_response(my_socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note- special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    # (8) treat all responses except SEND_PHOTO
    if cmd is not protocol.Commands[4]:
        response = protocol.get_msg(my_socket).decode()
        print(response)
    # (10) treat SEND_PHOTO
    else:
        response = protocol.get_msg(my_socket)
        response.save(SAVED_PHOTO_LOCATION)


def main():
    # open socket with the server
    my_socket = socket.socket()
    my_socket.connect((IP, 8820))
    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')
    keep_going = True
    # loop until user requested to exit
    while keep_going:
        cmd = input("Please enter command:\n")
        if protocol.check_cmd(cmd):
            if cmd == protocol.Commands[6]:
                print("Closing...")
                keep_going = False
            else:
                packet = protocol.create_msg(cmd)
                my_socket.send(packet.encode())
                handle_server_response(my_socket, cmd)
        else:
            print("Not a valid command, or missing parameters\n")
    my_socket.close()


if __name__ == '__main__':
    main()
