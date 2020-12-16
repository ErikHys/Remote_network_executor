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
        print("sending")
        connectionSocket.send(package)
        package = model_file.read(1024)
    print("sent")
    model_file.close()


while True:
    connectionSocket, addr = serverSocket.accept()
    file = open('train_model.py', 'wb')
    package = connectionSocket.recv(1024)
    print("Receiving program")
    while package:
        print("Receiving")
        if package.decode() == "EOF":
            break
        file.write(package)
        package = connectionSocket.recv(1024)
    print("received")
    file.close()

    exec(open('train_model.py').read())
    print("ran program")
    model_file = open('model.json', 'rb')
    send_data(model_file, connectionSocket, "model")
    connectionSocket.send("EOF".encode())
    connectionSocket.recv(1024)
    model_file = open('model.h5', 'rb')
    send_data(model_file, connectionSocket, "model weight")
    connectionSocket.close()
