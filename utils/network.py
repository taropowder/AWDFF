import socket
import random


def is_port_used(port, ip='127.0.0.1'):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        return True
    except Exception:
        return False
    finally:
        s.close()


def get_no_port_being_used():
    l_port = random.randint(10000, 65535)
    while is_port_used(l_port):
        l_port = random.randint(10000, 65535)

    return l_port
