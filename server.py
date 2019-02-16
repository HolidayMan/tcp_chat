import socket
import threading
import sys


def send_to_everybody(mess, addr, user):
	for i in clients:
		if i[1] == addr:
			continue
		message = '{}: {}'.format(user, mess).encode('utf-8')
		i[0].send(message)


def recieving(connection, address, username):
	while True:
		mess = connection.recv(1024).decode('utf-8')
		try:
			if mess == '/disconnect':
				send_to_everybody('{} disconnected'.format(username), address, 'Server')
				print('\b'*4, '{} disconnected'.format(username)+'\n>>> ', sep='', end='')
				del clients[clients.index((connection, address, username))]
				connection.close()
				break
		except IndexError:
			pass
		send_to_everybody(mess, address, username)



def acc():
	global sock
	global clients
	sock.listen(3)
	while True:
		conn, addr = sock.accept()
		username = conn.recv(1024).decode('utf-8')
		mess = '{} connected\n>>> '.format(username)
		print('\b'*4, mess, sep='', end='')
		send_to_everybody('{} connected'.format(username), addr, 'Server')
		clients.append((conn, addr, username))
		threading.Thread(target=recieving, args=(conn, addr, username), daemon=True).start()

clients = []

ip = '192.168.0.107' #socket.gethostbyname((socket.gethostname()))
if len(sys.argv) == 2:
	port = int(sys.argv[1])
else:
	print('Incorrect use. Specify the port.')
	exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((ip, port))

if __name__ == "__main__":
	connecting_thread = threading.Thread(target=acc, daemon=True)
	connecting_thread.start()
	print('[*] Server started on {}:{}'.format(ip, port))
	commands = ['exit', 'showclients']
	while True:
		command = input('>>> ')
		if command in commands:
			if command == 'exit':
				print('[*] Stopping server')
				for i in clients:
					i[0].send('Server turned off'.encode('utf-8'))
					i[0].close()
				sock.close()
				exit()
			if command == 'showclients':
				if len(clients) > 0:
					for i in range(len(clients)):
						if i == len(clients)-1:
							print(clients[i][2])
							continue
						print(clients[i][2]+', ', end='')
				else:
					print('No clients connected')
		elif command in '\n ':
			pass
		else:
			print('Unknown command')
