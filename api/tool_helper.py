#!/usr/bin/env python3
import socket

def get_output(host):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("amass", 31337))

    # Send host
    #host = "provinnovate.com"
    payload = bytes(host+"\n", encoding='utf-8')
    s.send(payload)

    output = b''
    while True:
        chunk = s.recv(2048)
        if b"DONE" in chunk:
            break
        elif chunk != b'':
            output += chunk
            print(str(chunk,encoding="utf-8").rstrip())

    with open("amass.out", "wb") as f:
        f.write(output)
    return str(output, encoding="utf-8").rstrip()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("\nUsage:\n\t{} <HOST>\n".format(sys.argv[0]))
        sys.exit(1)
    get_output(host)
