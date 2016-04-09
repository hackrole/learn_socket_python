# -*- coding: utf-8 -*-

import sys
import socket
import argparse


HOST = "localhost"
DATA_PAYLOAD = 2048
BACKLOG = 5


def echo_server(port):
    """ a simple echo server """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = (HOST, port)
    print "starting up echo server on %s port %s" % server_address
    sock.bind(server_address)

    sock.listen(BACKLOG)

    while True:
        print "waiting to receive message from client"
        client, address = sock.accept()
        data = client.recv(data_payload)
        if data:
            print "Data: %s" % data
            client.send(data)
            print "sent %s bytes back to %s" % (data, address)

        client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="socket server exmaple")
    parser.add_argument("--port", action="store", dest="port",
                        type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    echo_server(port)
