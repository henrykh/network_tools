# -*- coding: utf-8 -*-

import pytest
from echo_client import client_server


def test_client_receives_response():
    assert client_server('test') == 'Echo: "test"'


def test_unicode():
    assert client_server(u'éclaire') == u'Echo: "éclaire"'


def test_string_over_buffer_size():
    assert client_server('''Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
        Aliquam sed nunc sed tellus volutpat rutrum. Nunc ante nunc, consectetur eu''') == \
        '''Echo: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
        Aliquam sed nunc sed tellus volutpat rutrum. Nunc ante nunc, consectetur eu"'''
