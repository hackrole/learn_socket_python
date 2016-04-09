# -*- coding: utf-8 -*-

import socket


def test_socket_timeout():
    print "Default global timeout: ", socket.getdefaulttimeout()
    socket.setdefaulttimeout(200)
    print "current Default global timeout: ", socket.getdefaulttimeout()

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Default socket timeout: %s" % conn.gettimeout()
    conn.settimeout(100)
    print "current socket timeout: %s" % conn.gettimeout()


if __name__ == "__main__":
    test_socket_timeout()
