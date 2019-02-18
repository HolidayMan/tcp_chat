import socket
import threading
import sys
import time

f = open('log.txt', 'w')
f.close()

def gettime():
    return time.strftime("%d.%m.%Y-%H:%M:%S", time.localtime())

def writemess(mess):
    with open('log.txt', 'a') as f:
        f.write(mess)


def send_history(conn, num):
    with open('log.txt', 'r') as f:
        messages = f.readlines()
    if ''.join(num.split()) == 'all':
        mess = ''
        for i in messages:
            mess+=i
        conn.send(mess.encode('utf-8'))
    else:
        try:
            num = int(num)
        except ValueError:
            conn.send('It must be a positive number or "all"'.encode('utf-8'))
            return 0
        if num > len(messages):
            mess = ''
            for i in messages:
                mess+=i
                print(messages)
            conn.send(mess.encode('utf-8'))
        elif num > 0:
            messages = messages[::-1][:num][::-1]
            mess = ''
            for i in messages:
                mess+=i
            conn.send(mess.encode('utf-8'))


def getip():
    import http.client
    conn = http.client.HTTPConnection("ifconfig.me")
    conn.request("GET", "/ip")
    return conn.getresponse().read().decode('utf-8')


def send_to_everybody(mess, addr, user):
    global file_messages
    message = '{}[{}]: {}'.format(user, gettime(), mess)
    for i in clients:
        if i[1] == addr:
            continue
        i[0].send(message.encode('utf-8'))
    writemess('{}[{}]=[{}]: {}\n'.format(user, gettime(), addr[1], mess))


def recieving(connection, address, username):
    global clients
    while True:
        try:
            mess = connection.recv(1024).decode('utf-8')
        except OSError:
            break
        try:
            if mess == '/disconnect':
                send_to_everybody('{} disconnected'.format(username), address, 'Server')
                connection.send('/disconnect'.encode('utf-8'))
                print('\b'*4, '{} disconnected [{}]'.format(username, gettime())+'\n>>> ', sep='', end='')
                del clients[clients.index((connection, address, username))]
                for i in clients:
                    if i[0] == connection:
                        i[0].close()
                        break
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
        howmuch = conn.recv(1024).decode('utf-8')
        send_history(conn, howmuch)
        mess = '{} connected [{}]\n>>> '.format(username, gettime())
        print('\b'*4, mess, sep='', end='')
        send_to_everybody('{} connected'.format(username), addr, 'Server')
        clients.append((conn, addr, username))
        threading.Thread(target=recieving, args=(conn, addr, username), daemon=True).start()

clients = []


if __name__ == "__main__":
    ip = '192.168.0.107' #socket.gethostbyname((socket.gethostname()))
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    else:
        print('Incorrect use. Specify the port.')
        exit()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, port))


    connecting_thread = threading.Thread(target=acc, daemon=True)
    connecting_thread.start()
    print('[*] Server started on {}:{}'.format(getip(), port))
    writemess('Server[{}]: Server started on {}:{}'.format(gettime(), getip(), port)+'\n')


    commands = ['exit', 'showclients', 'kick']
    while True:
        command = input('>>> ').split()
        if command[0] in commands:
            com = command[0]
            if com == 'exit':
                print('[*] Stopping server')
                for i in clients:
                    i[0].send('/turnoff'.encode('utf-8'))
                    i[0].close()
                writemess('{}[{}]: {}\n'.format('Server', gettime(), 'Server turned off'))
                sock.close()
                exit()

            elif com == 'showclients':
                if len(clients) > 0:
                    for i in range(len(clients)):
                        if i == len(clients)-1:
                            print('{}: {}'.format(clients[i][2], clients[i][1][1]))
                            continue
                        print('{}: {}'.format(clients[i][2], clients[i][1][1])+', ', end='')
                else:
                    print('No clients connected')

            elif com == 'kick':
                if len(command)>1:
                    for i in clients:
                        if i[1][1] == int(command[1]):
                            i[0].send('/kick'.encode('utf-8'))
                            i[0].close()
                            del clients[clients.index(i)]
                            print('{} was kicked'.format(i[2]))
                            send_to_everybody('{} was kicked'.format(i[2]), None, 'Server')
                            break
                    else:
                        print('User not found')
                else:
                    print('kick: Incorrect use. Specify the address. Type "showclients" to see connected users.')

        elif ''.join(command) in '\n ':
            pass
        else:
            print('Unknown command')
