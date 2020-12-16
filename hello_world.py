import tensorflow as tf
import pandas as pd
from sklearn import model_selection
from tensorflow.python.keras.utils.np_utils import to_categorical


def get_model():
    """ Convolutional neural network, SDG optimizer, relu activation, using 3 layers of convolutional layers and 2
    max pooling for categorising handwritten digits.
    """
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(28, 28, 1)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9),
                  loss=tf.keras.losses.categorical_crossentropy,
                  metrics=['accuracy'])
    return model


dataX = pd.read_csv("handwritten_digits_images.csv")
dataY = pd.read_csv("handwritten_digits_labels.csv")
X = dataX.to_numpy()
Y = dataY.to_numpy()
x_train, x_test, y_train, y_test = model_selection.train_test_split(X, Y, shuffle=True, test_size=0.2, random_state=27)
model = get_model()
x_train, x_val = x_train.reshape(x_train.shape[0], 28, 28, 1), x_test.reshape(x_test.shape[0], 28, 28, 1)
y_train, y_val = to_categorical(y_train, num_classes=10), to_categorical(y_test, num_classes=10)
model.fit(x_train, y_train, batch_size=32, epochs=1)
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("model.h5")
print("Saved model to disk")

