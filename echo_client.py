from __future__ import unicode_literals
import socket
import sys


def client_server(msg):
    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)

    client_socket.connect(('127.0.0.1', 50000))
    client_socket.sendall(msg.encode('utf-8'))
    client_socket.shutdown(socket.SHUT_WR)

    return_msg = ""
    buffer_size = 32
    complete = False

    while not complete:
        msg_part = client_socket.recv(buffer_size).decode('utf-8')
        if len(msg_part) < buffer_size:
            complete = True
            client_socket.close()
        return_msg = "{}{}".format(return_msg, msg_part)

    return return_msg

if __name__ == "__main__":
    print client_server(sys.argv[1])
