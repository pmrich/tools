#!/usr/bin/env python
import sys
import socket
socket.setdefaulttimeout(4)

if __name__ == "__main__":
    try:    
        print("socket.gethostname() -> {%s}" % socket.gethostname())
        print("socket.getfqdn() -> {%s}" % socket.getfqdn())
    except:
        print("Failed to get current hostname/fqdn.")
    host = sys.argv[1]
    port = int(sys.argv[2])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = s.connect((host, port))
        #result = s.connect_ex((host, port))
    except Exception as err:
        print("Error connecting to {%s}:{%s}" % (host, port))
        raise err
    else:
        print("Connected to {%s}:{%s}" % (host, port))
    finally:
        #print(f"result:{result}")
        s.close()

    
