import socket
import threading

sock = socket.socket()
sock.connect(('localhost', 9043))
input()