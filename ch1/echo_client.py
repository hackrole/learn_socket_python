# -*- coding: utf-8 -*-

import sys
import socket
import argparse


HOST = "localhost"


def echo_client(port):
    """ A simple echo client """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (HOST, port)
    print "connecting  to %s port %s" % server_address
    sock.connect(server_address)

    # send data
    try:
        message = "Test mesasge. this will be echoed"
        print "Sending %s" % message
        sock.sendall(message)
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print "Received: %s" % data

    except socket.errno as e:
        print "Socket error: %s" % str(e)
    except Exception as e:
        print "other exception:", str(e)
    finally:
        print "closing connection to the server"
        sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="socket server example")
    parser.add_argument('--port', action='store', dest='port',
                        type=int, required=True)

    given_args = parser.parse_args()
    port = given_args.port
    echo_client(port)
