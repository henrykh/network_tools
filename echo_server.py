from __future__ import unicode_literals
import socket
import os
from mimetypes import guess_type

ROOT_DIR = "{}/root".format(os.curdir())

def resolve_uri(uri):
    response = ""

    if os.path.isdir(uri):
        response = os.listdir(uri)
    elif os.path.isfile(uri):
        file_type = guess_type(uri)
        try:
            f = open(uri, 'r')
            return f.read()
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)


    else:
        return response_error(404, 'Resource Not Found')


    # if uri is a directory, return HTML listing of that directory as body
    # if the resources is a file, return the contents of the file
        #content type value should be related to the type of the file
    # if the requested resource cannot be found, raise an appropriate error

def response_ok(uri):
    response = []
    response.append("HTTP/1.1 200 OK")
    response.append("Content-Type = text/html; charset=utf-8")
    response.append("")
    response.append(resolve_uri(uri))

    response = "\r\n".join(response).encode("utf-8")
    return response


def response_error(error, error_msg):
    response = []
    response.append("HTTP/1.1 {} {}".format(error, error_msg))
    response.append("")
    response.append("{} {}".format(error, error_msg))
    response = "\r\n".join(response).encode("utf-8")

    return response


def parse_request(request):
    first_line = request.splitlines()[0]
    first_line = first_line.split(" ")

    if first_line[0] == "GET":
        if first_line[2] == "HTTP/1.1":
            return response_ok(first_line[1])
        else:
            return response_error(505, "Protocol must be HTTP/1.1")
    else:
        return response_error(405, "Method must be GET")


if __name__ == "__main__":
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)

    buffer_size = 32

    server_socket.bind(('127.0.0.1', 50000))
    server_socket.listen(1)

    try:
        while True:
            request = ''
            conn, addr = server_socket.accept()

            request_part = conn.recv(buffer_size).decode('utf-8')
            request += request_part
            while len(request_part) >= buffer_size:
                request_part = conn.recv(buffer_size).decode('utf-8')
                request += request_part

            if request:
                response = parse_request(request)
                conn.sendall(response)
                conn.close()

    except KeyboardInterrupt:
        server_socket.close()
