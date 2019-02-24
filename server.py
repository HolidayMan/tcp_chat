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
      try:
        i[0].send('[{}] {}({}): {}'.format(functions.gettime(), username, addr, mess).encode('utf-8'))
      except OSError:
        del self.clients[self.clients.index((conn, addr, username))]


  def kick(self, command):
    if len(command)>1:
      address = command[1]
      try:
        address = int(address)

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
      print('kick: Incorrect use. Specify the address. Type "sclients" to see connected users.')

  def receiving(self, conn, addr, username):
    empty_message_count = 0 
    while True:
      try:
        mess = conn.recv(1024).decode('utf-8')
      except OSError:
        try:
          del self.clients[self.clients.index((conn, addr, username))]
        except ValueError:
          break
        functions.writemess('[{}] {}: {}({}) {}'.format(functions.gettime(), 'Server', username, addr[1], 'disconnected'))
        conn.close()
        break

      if mess == '':
        empty_message_count += 1
        if empty_message_count >= 20:
          try:
            del self.clients[self.clients.index((conn, addr, username))]
          except ValueError:
            break
          functions.writemess('[{}] {}: {}({}) {}'.format(functions.gettime(), 'Server', username, addr[1], 'disconnected'))
          try:
            conn.send('You have sended too many empty messages'.encode('utf-8'))
          except OSError:
            pass
          conn.close()
          break
        continue
      else:
        empty_message_count = 0
      if (conn, addr, username) in self.clients:
        self.send_message_to_everybody(mess, addr[1], username)
        functions.writemess('[{}] {}({}): {}'.format(functions.gettime(), username, addr[1], mess))

  def entering(self, conn, addr):
    while True:
      conn.send('Username: '.encode('utf-8'))
      username = conn.recv(1024).decode('utf-8')
      if ''.join(username.split()) == '':
        continue
      else:
        break
    self.clients.append((conn, addr, username))
    threading.Thread(target=self.receiving, args=(conn, addr, username), daemon=True).start()
    self.send_message_to_everybody('{}({}) connected'.format(username, addr[1]), 0, 'Server')
    functions.writemess('[{}] {}: {}({}) {}'.format(functions.gettime(), 'Server', username, addr[1], 'connected'))
    


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
        command = command.split()
        if command[0] == '':
          continue


        elif command[0] == 'exit':
          print('[!] Server stopped')
          functions.writemess('[{}] Server: server stopped.'.format(functions.gettime()))
          self.send_message_to_everybody('server stopped.', 0, 'Server')
          break


        elif command[0] == 'kick':
          self.kick(command)

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
