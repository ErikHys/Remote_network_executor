from socket import socket, AF_INET, SOCK_STREAM

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()
    file = open('train_model.py', 'wb')
    package = connectionSocket.recv(1024)
    while package:
        print("Receiving")
        file.write(package)
        package = connectionSocket.recv(1024)
    print("received")
    file.close()

    exec(open('train_model.py').read())
    print("ran?")
    model_file = open('model.json', 'rb')
    package = model_file.read(1024)
    while package:
        print("sending")
        connectionSocket.send(package)
        package = model_file.read(1024)
    print("sent")
    connectionSocket.close()
