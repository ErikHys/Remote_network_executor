from socket import socket, AF_INET, SOCK_STREAM

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()
    file = open('current_model.py', 'wb')
    package = connectionSocket.recv(1024)
    while package:
        print("Receiving")
        file.write(package)
        package = connectionSocket.recv(1024)
    print("received")
    file.close()
    connectionSocket.close()
    exec(open('current_model.py').read())
    print("ran?")
    break
