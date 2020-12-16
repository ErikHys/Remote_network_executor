from socket import socket, AF_INET, SOCK_STREAM

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')


def send_data(model_file, connectionSocket, name):
    package = model_file.read(1024)
    print("Sending ", name)
    while package:
        connectionSocket.send(package)
        package = model_file.read(1024)
    print("sent")
    model_file.close()


def receive_data(file, connectionSocket, name):
    package = connectionSocket.recv(1024)
    print("Receiving ", name)
    while package:
        if package.decode() == "EOF":
            break
        file.write(package)
        package = connectionSocket.recv(1024)
    print("received", name)
    file.close()


while True:
    connectionSocket, addr = serverSocket.accept()
    file = open('train_model.py', 'wb')
    receive_data(file, connectionSocket, "program")
    file = open('dataX.csv', 'wb')
    receive_data(file, connectionSocket, 'values')
    file = open('dataY.csv', 'wb')
    receive_data(file, connectionSocket, 'labels')
    exec(open('train_model.py').read())
    print("ran program")
    model_file = open('model.json', 'rb')
    send_data(model_file, connectionSocket, "model")
    connectionSocket.send("EOF".encode())
    connectionSocket.recv(1024)
    model_file = open('model.h5', 'rb')
    send_data(model_file, connectionSocket, "model weight")
    connectionSocket.close()
