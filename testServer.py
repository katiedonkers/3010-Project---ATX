import sys
import socket
import sqlite3

port = 1080
host = '192.168.43.231'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(host)
sock.bind((host,1050))

data, address = sock.recvfrom(1024)  # needs timeouts
print(data)