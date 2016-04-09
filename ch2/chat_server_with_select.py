# -*- coding: utf-8 -*-

import sys
import socket
import signal
import select
import cPickle
import struct
import argparse


SERVER_HOST = 'localhost'
CHAT_SERVER_NAME = 'server'


def send(channel, *args):
    buff = cPickle.dumps(args)
    value = socket.htonl(len(buff))
    size = struct.pack("L", value)
    channel.send(size)
    channel.send(buff)


def receive(channel):
    size = struct.calcsize("L")
    size = channel.recv(size)
    try:
        size = socket.ntohl(struct.unpack("L", size)[0])
    except struct.error as ex:
        return ''

    buf = ""
    while len(buf) < size:
        buf = channel.recv(size - len(buf))

    return cPickle.loads(buf)[0]


class ChatServer(object):
    """ an example chat server using select """

    def __init__(self, port, backlog=5):
        self.clients = 0
        self.clientmap = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsocket(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, port))
        print "server listening to port: %s ..." % port
        self.server.listen(backlog)

        signal.signal(signal.SIGINT, self.sighandler)

    def sighandler(self, signum, frame):
        """ clean up client outputs """
        print "shutting down server ..."

        for output in self.outputs:
            output.close()

        self.server.close()

    def get_client.name(self, client):
        """ return the name of the client"""
        info = self.clientmap[client]
        host, name = info[0][0], info[1]

        return '@'.join((name, host))

    def run(self):
        inputs = [self.server, sys.stdin]
        self.outputs = []
        running = True

        while running:
            try:
                readable, writeable, exceptional = select.select(inputs, self.outputs, [])
            except select.error as e:
                break

            for sock in readable:
                if sock == self.server:
                    client, address = self.server.accept()
                    print "chat server: got connection %d from %s" % (client.fileno(), address)

                    cname = receive(client).split("NAME: ")[1]

                    self.clients += 1
                    send(client, "CLIENT: " + str(address[0]))
                    inputs.append(client)
                    self.clientmap[client] = (address, cname)

                    # send joining info to other client
                    msg = "\n(Connected: New client(%d) from %s)" % (self.clients, self.get_client_name(client))
                    for output in self.outputs:
                        send(output, msg)
                    self.outputs.append(client)

                elif sock == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = False
                else:
                    # handle all other sockets
                    try:
                        data = receive(sock)
                        if data:
                            # send as new client's message...
                            msg = '\n#[' + self.get_client_name(sock) + ']>>' + data
                            for output in self.outputs:
                                if output != sock:
                                    send(output, msg)

                        else:
                            print "chat server: %d hung up" % sock.fileno()
                            self.client -= 1
                            inputs.remove(sock)
                            self.outputs.remove(sock)

                            msg = "\n(now hung up: client from %s)" % self.get_client_name(sock)
                            for output in self.outputs:
                                send(output, msg)

                    except socket.error as ex:
                        inputs.remove(sock)
                        self.outputs.remove(sock)

        self.server.close()


class ChatClient(object):
    """ a command line chat client using select """

    def __init__(self, name, port, host=SERVER_HOST):
        self.name = name
        self.connected = False
        self.host = host
        self.port = port
        self.prompt = '[' + '@'.join((name, socket.gethostname().split('.')[0])) + ']>'

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, self.port))
            print "now connected to chat server@port %d" % self,port
            self.connected = True
            # send my name
            send(self.sock, "NAME: " + self.name)
            data = receive(self.sock)

            addr = data.split("CLIENT: ")[1]
            self.prompt = '[' + '@'.join((self.name, addr)) +  ']>'
        except socket.error as e:
            print "Failed to connect to chat server @ port %d" % self.port
            sys.exit(1)

    def run(self):
        """ chat client main loop """
        while self.connected:
            try:
                sys.stdout.write(self.prompt)
                sys.stdout.flush()

                # wait for input from stdin and socket
                readable, writeable, exceptional = select.select([0, self.sock], [], [])

                for sock in readable:
                    if sock == 0:
                        data = sys.stdin.readline().strip()
                        if data: send(self.sock, data)
                    elif sock == self.sock:
                        data = receive(self.sock)
                        if not data:
                            print "client shutting down"
                            self.connected = False
                            break
                        else:
                            sys.stdout.write(data + "\n")
                            sys.stdout.flush()
            except KeyboardInterrupt:
                print " client interrupted. "
                self.sock.close()
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="socket server example with select")
    parser.add_argument("--name", action="store", dest="name", required=True)
    parser.add_argument("--port", action="store", dest="port",
                        type=int, required=True)

    given_args = parser.parse_args()
    port = given_args.port
    name = given_args.name

    if name == CHAT_SERVER_NAME:
        server = ChatServer(port)
        server.run()
    else:
        client = ChatClient(name=name, port=port)
        client.run()
