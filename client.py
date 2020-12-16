from socket import socket, AF_INET, SOCK_STREAM

serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
file = open("hello_world.py", 'rb')
package = file.read(1024)
while package:
    print("sending")
    clientSocket.send(package)
    package = file.read(1024)
file.close()
print("sent")
# modifiedSentence = clientSocket.recv(1024).decode()
# print('From Server: ', modifiedSentence)
clientSocket.close()
