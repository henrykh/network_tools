from __future__ import unicode_literals
import socket
import os
from mimetypes import guess_type

ROOT_DIR = "root"


def resolve_uri(uri):
    path = "{}{}".format(ROOT_DIR, uri)

    if ".." in path:
        raise IOError("Access Denied")

    # if uri is a directory, return HTML listing of that directory as body
    elif os.path.isdir(path):
        directory_html = ["<li>{}</li>".format(item) for item in os.listdir(path)]
        directory_html.insert(0, "<ul>")
        directory_html.insert(len(directory_html), "</ul>")
        return ("\n".join(directory_html), "text/html")

    # if the resources is a file, return the contents of the file

    elif os.path.isfile(path):
        file_type = guess_type(path)[0]
        try:
            f = open(path, 'r')
            return (f.read(), file_type)
        except IOError:
            raise IOError("Access Denied")

    # if the requested resource cannot be found, raise an appropriate error
    else:
        raise IOError("File Not Found")


def response_ok(uri):
    response = []
    try:
        resolved_uri = resolve_uri(uri)
    except IOError as excinfo:
        if "Access Denied" in str(excinfo):
            return response_error(403, 'Access Denied')
        else:
            return response_error(404, 'Resource Not Found')

    response.append("HTTP/1.1 200 OK")
    response.append("Content-Type = {} ; charset=utf-8".format(resolved_uri[1]))
    response.append("Content-Length = {}".format(len(resolved_uri[0])))
    response.append("")
    response.append(resolved_uri[0])

    response = "\r\n".join(response).encode("utf-8")
    return response


def response_error(error, error_msg):
    response = []
    response.append("HTTP/1.1 {} {}".format(error, error_msg))
    response.append("")
    response.append("<div>{} {}</div>".format(error, error_msg))
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
