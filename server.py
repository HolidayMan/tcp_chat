import socket
import threading
import time

import configparser

import functions
import commands
class TCPServer:

  def __init__(self, ip, port):
    self.clients = []
    self.SOCK = socket.socket()
    self.SOCK = socket.socket()
    self.SOCK.bind((ip, port))
    self.ip = ip
    self.port = port


  def send_message_to_everybody(self, mess, addr, username):
    for i in self.clients:
      if i[1][1] == addr:
        continue
      i[0].send('[{}] {}({}): {}'.format(functions.gettime(), username, addr, mess).encode('utf-8'))


  def receiving(self, conn, addr, username):
    while True:
      try:
        mess = conn.recv(1024).decode('utf-8')
      except OSError:
        del self.clients[self.clients.index((conn, addr, username))]
      self.send_message_to_everybody(mess, addr[1], username)
      functions.writemess('[{}] {}({}): {}'.format(functions.gettime(), username, addr, mess))



  def entering(self, conn, addr):
    while True:
      conn.send('Username: '.encode('utf-8'))
      username = conn.recv(1024).decode('utf-8')
      if ''.join(username.split()) == '':
        continue
      else:
        break
    self.clients.append((conn, addr, username))
    threading.Thread(target=self.receiving, args=(conn, addr, username), daemon=True)
    functions.writemess('[{}] {}: {}({}) {}'.format(functions.gettime(), 'Server', username, addr[1], 'connected'))
    while True:
      time.sleep(5)
      if (conn, addr, username) in self.clients:
        continue
      else:
        break


  def accepting(self):
    while True:
      conn, addr = self.SOCK.accept()
      threading.Thread(target=self.entering, args=(conn, addr), daemon=True).start()


  def run(self):
    log =  open('log.txt', 'w')
    log.close()
    self.SOCK.listen(3)
    accepting_thread = threading.Thread(target=self.accepting, daemon=True)
    accepting_thread.start()
    print('[*] Server started on {}:{}'.format(self.ip, self.port))
    functions.writemess('[{}] Server: server started on {}:{}'.format(functions.gettime(), self.ip, self.port))
    while True:
      try:
        command = input('>>> ')
        if ''.join(command.split()) == '':
          continue


        elif command == 'exit':
          print('[!] Server stopped')
          functions.writemess('[{}] Server: server stopped.'.format(functions.gettime()))
          self.send_message_to_everybody('server stopped.', 00000, 'Server')
          break


        elif command == 'kick':
          if len(command)>1:
            try:
              address = int(adress)

            except ValueError:
              print('kick: address must be a number')
              return 0

            for i in self.clients:
                if i[1][1] == address:
                  i[0].send('Server: you was kicked'.encode('utf-8'))
                  i[0].close()
                  del self.clients[self.clients.index(i)]
                  print('{} was kicked'.format(i[2]))
                  functions.writemess('[{}] Server: {} ({}) was kicked'.format(functions.gettime(), i[2], i[1][1]))
                  break

            else:
              print('kick: user not found')

          else:
            print('kick: Incorrect use. Specify the address. Type "showclients" to see connected users.')

        else:
          commands.do_command(command, self.clients)


      except KeyboardInterrupt:
        print('[!] Server stopped')
        functions.writemess('[{}] Server: server stopped.'.format(functions.gettime()))
        break

if __name__ == "__main__":
  config = configparser.ConfigParser()
  config.read('config.ini')
  server = TCPServer(config['server']['ip'], int(config['server']['port']))
  server.run()
