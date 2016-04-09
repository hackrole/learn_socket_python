# -*- coding: utf-8 -*-

import sys
import socket
import argparse


def main(argv=None):
    if not argv:
        argv = sys.argv

    # setup argument parsing
    parser = argparse.ArgumentParser(description="Socket Error Example")
    parser.add_argument("--host", action="store", dest="host", required=False)
    parser.add_argument("--port", action="store", dest="port",
                        type=int, required="False")
    parser.add_argument("--file", action="store", dest="file", required=False)

    given_args = parser.parse_args(argv)
    host = given_args.host
    port = given_args.port
    filename = given_args.file

    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as excp:
        print "Error creating socket: %s" % excp
        sys.exit(1)

    try:
        conn.connect((host, port))
    except socket.gaierror as excp:
        print "address-related error connecting to server: %s" % e
        sys.exit(1)
    except socket.error as e:
        print "Connection error: %s" % e
        sys.exit(1)

    try:
        conn.sendall("GET %s HTTP/1.0\r\n\r\n" % filename)
    except socket.error as e:
        print "Error sending data: %s" % e
        sys.exit(1)

    while 1:
        try:
            buf = conn.recv(2048)
        except socket.error as e:
            print "Error receiving data: %s" % e
            sys.exit(1)
        if not len(buf):
            break
        # write the data
        sys.stdout.write(buf)


if __name__ == "__main__":
    main(["--host=www.pytgo.org", "--port=8080", "--file=socket_errors.py"])
