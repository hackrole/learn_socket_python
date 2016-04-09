# -*- coding: utf-8 -*-

import os
import socket
import threading
import SocketServer


SERVER_HOST = "localhost"
# the the kernel to pickup a port dynamically
SERVER_PORT = 0
BUF_SIZE = 1024
ECHO_MSG = "Hello echo server!"


class ForkedClient():
    """ a client to test forking server """

    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))

    def run(self):
        """ client playing with the server"""
        current_process_id = os.getpid()
        print "PID %s Sending echo message to the server: %s" % (current_process_id, ECHO_MSG)
        sent_data_length = self.sock.send(ECHO_MSG)
        print "Sent: %d characters, so far..." % sent_data_length

        # display server response
        response = self.sock.recv(BUF_SIZE)
        print "PID %s receive: %s" % (current_process_id, response[5:])

    def shutdown(self):
        """ cleanup the client socket """
        self.socket.close()


class ForkingServerRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(BUF_SIZE)
        current_process_id = os.getpid()
        response = "%s: %s" % (current_process_id, data)
        print "Server sending response [current_process_id: data] = [%s]" % response
        self.request.send(response)
        return


class ForkingServer(SocketServer.ForkingMixIn,
                    SocketServer.TCPServer):
    """nothing to add here. """


def main():
    # launch the server
    server = ForkingServer((SERVER_HOST, SERVER_PORT), ForkingServerRequestHandler)
    # retrieve the port number
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()
    print "server loop running PID: %s" % os.getpid()

    # launch the client(s)
    client1 = ForkedClient(ip, port)
    client1.run()

    client2 = ForkedClient(ip, port)
    client2.run()

    # clean then up
    server.shutdown()
    client1.shutdown()
    client2.shutdown()
    server.socket.close()


if __name__ == "__main__":
    main()
