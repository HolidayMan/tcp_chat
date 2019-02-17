import socket
import threading
import sys
import time

def gettime():
	return time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())

def sendmessage():
	global sock
	while True:
		message = input('You: ')
		if message in '\n ':
			continue
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
	howmuch = input('Number of last messages: ').encode('utf-8')
	print()
	sock.connect((ip, port))
	sock.sendall(username)
	sock.sendall(howmuch)
	history = sock.recv(2048).decode('utf-8')
	print(history, end='')
	print('You connected [{}]'.format(gettime()))
	threading.Thread(target=sendmessage, daemon=True).start()
except ConnectionRefusedError:
	print('[!] Incorrect ip or port')
	exit()
while True:
	try:
		try:
			message = sock.recv(1024).decode('utf-8')
		except OSError:
			sock.close()
			break
		if message == '/turnoff':
			print('\b'*5, 'Server turned off')
			break
		elif message == '/disconnect':
			break
		elif message == '/kick':
			print('\b'*5, 'You was kicked')
			break
		print('\b'*5, '{}\nYou: '.format(message), sep='', end='')
	except:
		sock.sendall('/disconnect'.encode('utf-8'))
		break
sock.close()
