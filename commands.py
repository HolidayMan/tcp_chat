import functions

commands = ['sclients', 'slogs']

def do_command(command, clients):
  if command[0] not in commands:
    print('server: command', command[0], 'not found')
    return 0
  if command[0] == 'sclients':
    showclients(clients)
  elif command[0] == 'slogs':
    showlogs()

def showclients(clients):
  if len(clients) > 0:
    for i in range(len(clients)):
      if i == len(clients)-1:
        print('{}: {}'.format(clients[i][2], clients[i][1][1]))
        continue
      print('{}: {}'.format(clients[i][2], clients[i][1][1])+', ', end='')
  else:
    print('no clients connected')

def showlogs():
  with open('log.txt', 'r') as f:
      print(f.read())
