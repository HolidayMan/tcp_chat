import socket
import threading
import sys
import time

def gettime():
    """gets and unpacks time"""
    return time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())

def sendmessage():
    """checks if your message is empty and sends it to server"""
    while True:
        message = input('You: ')
        if message in '\n ':
            continue
        SOCK.sendall(message.encode('utf-8'))

if len(sys.argv) != 2:
    print('[!] Incorrect use. Correct use is "python3 file.py ip:port"')
else:
    try:
        IP = sys.argv[1].split(':')[0]
        PORT = int(sys.argv[1].split(':')[1])
    except SyntaxError:
        print('[!] Incorrect use. Correct use is "python3 file.py ip:port"')
try:
    SOCK = socket.socket()
    while True:
        USERNAME = input('Username: ')
        if ''.join(USERNAME.split()) in '\n ':
            continue
        else:
            USERNAME = USERNAME.encode('utf-8')
            break
    HOWMUCH = input('Number of last messages: ').encode('utf-8')
    SOCK.connect((IP, PORT))
    SOCK.sendall(USERNAME)
    time.sleep(0.5)
    SOCK.sendall(HOWMUCH)
    print()
    HISTORY = SOCK.recv(2048).decode('utf-8')
    print(HISTORY, end='')
    print('You connected [{}]'.format(gettime()))
    threading.Thread(target=sendmessage, daemon=True).start()
except ConnectionRefusedError:
    print('[!] Incorrect ip or port')
    exit()
while True:
    try:
        try:
            MESSAGE = SOCK.recv(1024).decode('utf-8')
        except OSError:
            SOCK.close()
            break
        if MESSAGE == '/turnoff':
            print('\b'*5, 'Server turned off')
            break
        elif MESSAGE == '/disconnect':
            break
        elif MESSAGE == '/kick':
            print('\b'*5, 'You was kicked')
            break
        print('\b'*5, '{}\nYou: '.format(MESSAGE), sep='', end='')
    except KeyboardInterrupt:
        SOCK.sendall('/disconnect'.encode('utf-8'))
        break
SOCK.close()
