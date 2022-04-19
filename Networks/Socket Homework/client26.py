"""EX 2.6 client implementation
   Author: shoham zeharya
   Date: 24.10.21
"""

import socket
import protocol


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol.PORT))

    while True:
        user_input = input("Enter command\n")
        # Check if user entered a valid command as defined in protocol
        valid_cmd = protocol.check_cmd(user_input)
        if valid_cmd:
            message = protocol.create_msg(user_input)
            my_socket.send(message.encode())
            if user_input == "EXIT":
                break
            valid_msg, reply = protocol.get_msg(my_socket)
            if valid_msg:
                print(reply)
            else:
                print("Response not valid\n")
        else:
            print("Not a valid command")
    print("Closing\n")
    my_socket.close()


if __name__ == "__main__":
    main()
