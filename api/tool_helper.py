#!/usr/bin/env python3
import socket

def tool_port_map(tool):
    mapping = {"amass":30000,
               "subfinder":30001,
               "aiodnsbrute":30002,
               "sublist3r":30003,
               "gobuster":30004,
               "massdns":30005}
    return mapping["{}".format(tool)]

def run_service(tool,host):
    """Run service and copy output from tool's container."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((tool, tool_port_map(tool)))

    # Send host
    payload = bytes(host+"\n", encoding='utf-8')
    s.send(payload)

    output = b''
    while True:
        chunk = s.recv(2048)
        if b"DONE" in chunk:
            break
        elif chunk != b'':
            output += chunk
            #print(str(chunk,encoding="utf-8").rstrip())

    with open("/{}-{}.out".format(tool,host), "wb") as f:
        f.write(output)
    return str(output, encoding="utf-8").rstrip().split()

def get_output(tool,host):
    """Return the given tool's output as a list."""
    output = b''
    with open("/{}-{}.out".format(tool,host), "rb") as f:
        output += f.read()
    return str(output, encoding="utf-8").rstrip().split()

def check_cache(host):
    """Checks if host has already been enumerated. Return boolean."""
    result = False
    # check if file names exists
    return result
