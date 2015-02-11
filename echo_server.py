from __future__ import unicode_literals
import socket


server_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
    socket.IPPROTO_IP)

buffer_size = 32

server_socket.bind(('127.0.0.1', 50000))
server_socket.listen(1)


try:
    while True:
        msg = 'Echo: "'
        conn, addr = server_socket.accept()

        msg_part = conn.recv(buffer_size).decode('utf-8')
        msg += msg_part
        while len(msg_part) >= buffer_size:
            msg_part = conn.recv(buffer_size).decode('utf-8')
            msg += msg_part

        if msg:
            msg += '"'
            conn.sendall(msg.encode('utf-8'))
            msg, msg_part = ['Echo: ', '']
            conn.close()

except KeyboardInterrupt:
    server_socket.close()
