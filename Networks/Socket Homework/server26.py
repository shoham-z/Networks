"""EX 2.6 server implementation
   Author: shoham zeharya
   Date: 24.10.21
"""

import socket
import protocol


def asserts():
    assert protocol.check_cmd("RAND") == 1
    assert protocol.check_cmd("TIME") == 1
    assert protocol.check_cmd("WHORU") == 1
    assert protocol.check_cmd("EXIT") == 1
    assert protocol.check_cmd("rand") == 0
    assert protocol.check_cmd("BANANA") == 0
    assert protocol.check_cmd("12") == 0
    assert protocol.create_msg("shoham") == "06shoham"
    assert protocol.create_msg("04banana") != "080banana"


def main():
    asserts()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")

    while True:
        valid_msg, cmd = protocol.get_msg(client_socket)
        if valid_msg:
            print(cmd)
            if protocol.check_cmd(cmd):
                if cmd == "EXIT":
                    break
                else:
                    response = protocol.create_server_rsp(cmd)
            else:
                response = "Wrong command"
        else:
            response = "Wrong protocol"
            client_socket.recv(1024)  # Attempt to empty the socket from possible garbage
        client_socket.send(protocol.create_msg(response).encode())
    print("Closing\n")
    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    main()
