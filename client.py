from socket import socket, AF_INET, SOCK_STREAM
import pandas as pd
from sklearn import model_selection
from tensorflow.python.keras.utils.np_utils import to_categorical
from tensorflow.keras.models import model_from_json
import tensorflow as tf


def receive_data(new_model_file, clientSocket, name):
    package = clientSocket.recv(1024)
    print("Receiving ", name)
    while package:
        if name == "model" and package.decode() == "EOF":
            break
        new_model_file.write(package)
        package = clientSocket.recv(1024)
    print('Received')
    new_model_file.close()
    clientSocket.send("EOF".encode())


def send_data(file, clientSocket, name):
    package = file.read(1024)
    while package:
        clientSocket.send(package)
        package = file.read(1024)
    file.close()
    print("sent ", name)
    clientSocket.send("EOF".encode())


serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
file_name = input("Enter filename(use hello_world.py for testing):")
file = open(file_name, 'rb')
send_data(file, clientSocket, "program")
file = open("handwritten_digits_images.csv", 'rb')
send_data(file, clientSocket, "values")
file = open("handwritten_digits_labels.csv", 'rb')
send_data(file, clientSocket, 'labels')
new_model_file = open("new_model.json", 'wb')
receive_data(new_model_file, clientSocket, "model")
new_model_file = open("new_model.h5", 'wb')
receive_data(new_model_file, clientSocket, "model weights")
clientSocket.close()

json_model = open("new_model.json", 'r')
loaded_model = json_model.read()
json_model.close()
loaded_model = model_from_json(loaded_model)
loaded_model.load_weights("new_model.h5")
loaded_model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9),
                     loss=tf.keras.losses.categorical_crossentropy,
                     metrics=['accuracy'])
model = loaded_model
dataX = pd.read_csv("handwritten_digits_images.csv")
dataY = pd.read_csv("handwritten_digits_labels.csv")
X = dataX.to_numpy()
Y = dataY.to_numpy()
x_train, x_test, y_train, y_test = model_selection.train_test_split(X, Y, shuffle=True, test_size=0.2, random_state=27)
x_train, x_val = x_train.reshape(x_train.shape[0], 28, 28, 1), x_test.reshape(x_test.shape[0], 28, 28, 1)
y_train, y_val = to_categorical(y_train, num_classes=10), to_categorical(y_test, num_classes=10)
val_acc = model.evaluate(x_val, y_val)[1]
print(val_acc)
