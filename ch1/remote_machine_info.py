# -*- coding: utf-8 -*-

import socket


def get_remote_machine_info(remote_host):
    try:
        print "IP address of %s: %s" % (remote_host,
                                        socket.gethostbyname(remote_host))
    except socket.error as err_msg:
        print "%s: %s" % (remote_host, err_msg)


if __name__ == "__main__":
    get_remote_machine_info("www.python.org")
    get_remote_machine_info("www.pygtofuckmeandyou.org")
    get_remote_machine_info("meyou")
