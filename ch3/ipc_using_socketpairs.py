import os
import socket


BUFSIZE = 1024


def test_socketpair():
    """ test unix socketpair """
    parent, child = socket.socketpair()

    pid = os.fork()
    try:
        if pid:
            print "@parent, sending message..."
            child.close()
            parent.sendall("Hello from parent!")
            response = parent.recv(BUFSIZE)
            print "Response from child:", response
            parent.close()
        else:
            print "@child, waiting for message from parent"
            parent.close()
            message.child.recv(BUFSIZE)
            print "message from parent:", message
            child.sendall("Hello from child!")
            child.close()
    except Exception as ex:
        print "Error:", ex


if __name__ == "__main__":
    test_socketpair()
