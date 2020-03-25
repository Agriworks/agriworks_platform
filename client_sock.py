import socket
import sys

sock = socket.create_connection(('localhost', 4000))

"""
try:
    print("sending")
    message = b"This is a test"
    sock.sendall(message)
    amount_received = 0
    while amount_received < len(message):
        data = sock.recv(16)
        amount_received += len(data)
        print("received %s", data)
"""
sock.close()
