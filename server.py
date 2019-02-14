import socket
import threading


def acc():
	global sock
	global clients
	while True:
		print("Here")
		conn, addr = sock.accept()
		print(conn, addr)


clients = []

ip = socket.gethostbyname((socket.gethostname()))
port = 9043

sock = socket.socket()
sock.bind((ip, port))
sock.listen(1)

if __name__ == "__main__":
	connecting_thread = threading.Thread(target=acc, daemon=False)
	connecting_thread.start()
	print("[*] Server started")