#!/usr/bin/env python
import socket


class Behavior:
    LOCAL = "LOCAL"
    MASTER = "MASTER"


def get_capability(actor, behavior):
    lcladdr = socket.getaddrinfo(socket.getfqdn(), 0, socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, 0)
    capabilities = {}
    if behavior == Behavior.LOCAL:
        ip = "127.0.0.1"
        if actor == "node_a":
            capabilities = {
                'Convention Address.IPv4': (ip, 1900),
                'System Address.IPv4': lcladdr,
                'Admin Port': 1900,
                'LEADER': 'yes',
            }
        elif actor == "node_b":
            capabilities = {
                'Convention Address.IPv4': (ip, 1900),
                'Admin Port': 10001,
                'node_type': 'service_node',
            }
        elif actor == "node_c":
            capabilities = {
                'Convention Address.IPv4': (ip, 1900),
                'Admin Port': 10002,
                'node_type': 'compute_node',
            }
        else:
            raise Exception("Invalid actor")
    elif behavior == Behavior.MASTER:
        ip = "172.28.0.69"
        if actor == "node_a":
            capabilities = {
                'Convention Address.IPv4': ('', 1900),
                'System Address.IPv4': lcladdr,
                'Admin Port': 1900,
                'LEADER': 'yes',
            }
        elif actor == "node_b":
            capabilities = {
                'Convention Address.IPv4': (ip, 1900),
                'Admin Port': 10001,
                'node_type': 'service_node',
            }
        elif actor == "node_c":
            capabilities = {
                'Convention Address.IPv4': (ip, 1900),
                'Admin Port': 10001,
                'node_type': 'compute_node',
            }
    else:
        raise Exception("Invalid actor")
    return capabilities
