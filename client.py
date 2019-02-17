import socket
import threading
import sys

def sendmessage():
	global sock
	while True:
		message = input('You: ')
		if message in '\n ':
			continue
		elif message == '/disconnect':
			sock.sendall(message.encode('utf-8'))
			sock.close()
			break
		sock.sendall(message.encode('utf-8'))

if len(sys.argv) != 2:
	print('[!] Incorrect use. Correct use is "python3 file.py ip:port"')
else:
	try:
		ip = sys.argv[1].split(':')[0]
		port = int(sys.argv[1].split(':')[1])
	except SyntaxError:
		print('[!] Incorrect use. Correct use is "python3 file.py ip:port"')
try:
	sock = socket.socket()
	username = input('Username: ').encode('utf-8')
	sock.connect((ip, port))
	sock.sendall(username)
	threading.Thread(target=sendmessage, daemon=True).start()
except ConnectionRefusedError:
	print('[!] Incorrect ip or port')
	exit()
while True:
	try:
		try:
			message = sock.recv(1024).decode('utf-8')
		except OSError:
			break
		if message == '/disconnect':
			print('\b'*5, 'Server turned off')
			break
		elif message == '/kick':
			print('\b'*5, 'You was kicked')
			break
		print('\b'*5, '{}\nYou: '.format(message), sep='', end='')
	except:
		sock.sendall('/disconnect'.encode('utf-8'))
		break
sock.close()
