import time
def gettime():
  return time.strftime("%d.%m.%Y-%H:%M:%S", time.localtime())

def writemess(mess):
  with open('log.txt', 'a') as f:
    f.write(mess+'\n')
