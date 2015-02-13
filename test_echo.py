# -*- coding: utf-8 -*-

import pytest
from echo_client import client_server
import echo_server


def test_HTTP_200():
    response_first_line = client_server('''GET /index.html HTTP/1.1\r\n
            Host: henryhowes.com\r\n
            Content-Type: text/xml; charset=utf-8\r\n
            ''').splitlines()[0].split()

    assert response_first_line[1] == '200' and response_first_line[2] == 'OK'


def test_HTTP_not_GET():
    response_first_line = client_server('test').splitlines()[0].split()
    assert response_first_line[1] == '405'


def test_wrong_protocol():
    response_first_line = client_server('''GET /index.html HTTP/1.0\r\n
            Host: henryhowes.com\r\n
            Content-Type: text/xml; charset=utf-8\r\n
            ''').splitlines()[0].split()
    assert response_first_line[1] == '505'


def test_returns_file_content():
    response = client_server('''GET /test.html HTTP/1.1\r\n
            Host: henryhowes.com\r\n
            Content-Type: text/xml; charset=utf-8\r\n
            ''').splitlines()

    assert " ".join(response[1].split()[:3]) == "Content-Type = text/html"
    assert response[2] == "Content-Length = 23"
    assert response[4] == "<div>Hello World!</div>"


def test_returns_directory_listing():
    response = client_server('''GET / HTTP/1.1\r\n
            Host: henryhowes.com\r\n
            Content-Type: text/xml; charset=utf-8\r\n
            ''').splitlines()
    assert " ".join(response[1].split()[:3]) == "Content-Type = text/html"
    assert response[2] == "Content-Length = 29"
    assert "\n".join(response[4:]) == "<ul>\n<li>test.html</li>\n</ul>"
