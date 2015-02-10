import socket


if __name__ == '__main__':
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)

    buffer_size = 4096

    server_socket.bind(('127.0.0.1', 50000))
    server_socket.listen(1)

    while 1:
        conn, addr = server_socket.accept()
        msg = conn.recv(buffer_size)
        if msg:
            conn.send(msg)
        conn.close()
