import socket
import threading
import sys

def sendmessage():
	global sock
	while True:
		message = input('>>> ').encode('utf-8')
		sock.sendall(message)

if len(sys.argv) != 2:
	print('[!] Incorrect use. Correct use is "python3 file.py ip:port"')
else:
	try:
		ip = sys.argv[1].split(':')[0]
		port = int(sys.argv[1].split(':')[1])
	except SyntaxError:
		print('[!] Incorrect use. Correct use is "python3 file.py ip:port"')

sock = socket.socket()
username = input('Username: ').encode('utf-8')
sock.connect((ip, port))
sock.sendall(username)
threading.Thread(target=sendmessage, daemon=True).start()
while True:
	try:
		message = sock.recv(1024).decode('utf-8')
		print('\b'*4, '{}\n>>> '.format(message), sep='', end='')
		if message == 'Server turned off':
			break
	except:
		sock.sendall('{} disconnected'.format(username.decode('utf-8')).encode('utf-8'))
		break
sock.close()
