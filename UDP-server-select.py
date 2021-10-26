#! /usr/bin/env python3
# udp demo -- simple select-driven uppercase server

# Eric Freudenthal with mods by Adrian Veliz

import sys
from socket import *
from select import select

UPPERCASE_PORT = 50000
LOWERCASE_PORT = 50001
upperServerAddr = ("", UPPERCASE_PORT)   # any addr, port 50,000
lowerServerAddr = ("", LOWERCASE_PORT)

def change_upper(sock):
  "run this function when sock has rec'd a message"
  message, clientAddrPort = sock.recvfrom(999) #was 2048
  print("from %s: rec'd '%s'" % (repr(clientAddrPort), message))
  modifiedMessage = ''
  modifiedMessage = message.decode().upper().encode()
  sock.sendto(modifiedMessage, clientAddrPort)

def change_lower(sock):
  message, clientAddrPort = sock.recvfrom(999)
  print("from %s: rec'd '%s'" % (repr(clientAddrPort), message))
  modifiedMessage = ''
  modifiedMessage = message.decode().lower().encode()
  sock.sendto(modifiedMessage, clientAddrPort)
  

upperServerSocket = socket(AF_INET, SOCK_DGRAM)
upperServerSocket.bind(upperServerAddr)
upperServerSocket.setblocking(False)

lowerServerSocket = socket(AF_INET, SOCK_DGRAM)
lowerServerSocket.bind(lowerServerAddr)
lowerServerSocket.setblocking(False)

# map socket to function to call when socket is....
readSockFunc = {}               # ready for reading
writeSockFunc = {}              # ready for writing
errorSockFunc = {}              # broken

timeout = 5                     # select delay before giving up, in seconds

# function to call when upperServerSocket is ready for reading
readSockFunc[upperServerSocket] = change_upper
readSockFunc[lowerServerSocket] = change_lower

print("ready to receive")
while 1:
  readRdySet, writeRdySet, errorRdySet = select(list(readSockFunc.keys()),
                                                list(writeSockFunc.keys()), 
                                                list(errorSockFunc.keys()),
                                                timeout)
  if not readRdySet and not writeRdySet and not errorRdySet:
    print("timeout: no events")
  for sock in readRdySet:
    current_port = sock.getsockname()[1]
    readSockFunc[sock](sock)

