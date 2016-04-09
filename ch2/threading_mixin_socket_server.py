# -*- coding: utf-8 -*-

import os
import socket
import threading
import SocketServer


SERVER_HOST = 'localhost'
# pickup a port dynamically
SERVER_PORT = 0
BUF_SIZE = 1024


def client(ip, port, message):
    """ a client to test threading mixin server """
    # Connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, host))
    try:
        sock.sendall(message)
        response = sock.recv(BUF_SIZE)
        print "Client received: %s" % response
    finally:
        sock.close()


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    """ a example of threaded tcp request handler """

    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        response = "%s: %s" % (cur_thread.name, data)
        self.request.sendall(response)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """ nothing here """
    pass


if __name__ == "__main__":
    server = ThreadedTCPRequestHandler((SERVER_HOST, SERVER_PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running on thread: %s" % server_thread.name

    # run client
    client(ip, port, "Hello from client 1")
    client(ip, port, "Hello from client 2")
    client(ip, port, "Hello from client 3")

    # server shutdown
    server.shutdown()
