import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import utils
from typing import Callable

train_data, train_labels = utils.read_train_data()
train_data, train_labels = shuffle(train_data, train_labels, random_state=0)

test_data, test_labels = utils.read_test_data()
test_data, test_labels = shuffle(test_data, test_labels, random_state=0)


class NeuralNetwork:
    learn_rate: float
    correct_in_epoch: int

    # Input / Output
    X: np.array
    Y: np.array

    # Layer functions
    fs: list[Callable[[np.array], np.array]]

    # Weights
    Ws: list[np.array]

    # Biases
    Bs: list[np.array]

    # layers
    As: list[np.array]

    def sigmoid(self, X):
        return 1 / (1 + np.exp(-X))

    def deriv_sigmoid(self, X):
        return X * (1 - X)

    def softmax(self, X):
        exp = np.exp(X)
        return exp / np.sum(exp)

    def __init__(
            self,
            reshape_input=True,
            learn_rate=0.01,
            neuron_layers=np.array([784, 10, 10]),
    ):
        self.learn_rate = learn_rate
        self.reshape_input = reshape_input
        self.correct_in_epoch = 0
        self.Ws = []
        self.Bs = []

        for i, n in enumerate(neuron_layers[:-1]):
            next_n = neuron_layers[i + 1]
            W = np.random.uniform(-0.5, 0.5, (next_n, n))
            B = np.random.uniform(-0.5, 0.5, (next_n, 1))
            self.Ws.append(W)
            self.Bs.append(B)

        fs = [self.sigmoid] * (len(self.Ws) - 1)
        fs.append(self.softmax)
        self.fs = fs

    def error(self, Y):
        Ao = self.get_output()
        return np.sum(((Ao - Y) ** 2)) / len(Ao)

    def set_io(self, X, Y):
        if self.reshape_input:
            self.X = X.reshape(-1, 1)
            self.Y = Y.reshape(-1, 1)
        else:
            self.X = X
            self.Y = Y

    def is_correct(self):
        self.correct_in_epoch += int(np.argmax(self.Y) == np.argmax(self.get_output()))

    def forward_propagation(self):
        self.As = [self.X]
        for i, (W, B, f) in enumerate(zip(self.Ws, self.Bs, self.fs)):
            A = f(B + np.dot(W, self.As[i]).reshape(-1, 1))
            self.As.append(A)

    def backward_propagation(self):
        m = self.Y.size
        prev_delta = None
        last_index = len(self.Ws) - 1

        for i in range(last_index, -1, -1):
            if i == last_index:
                delta = self.As[i + 1] - self.Y
            else:
                delta = np.dot(self.Ws[i + 1].T, prev_delta) * self.deriv_sigmoid(self.As[i + 1])

            self.Ws[i] += 1 / m * np.dot(delta, self.As[i].T) * -self.learn_rate
            self.Bs[i] += 1 / m * delta * -self.learn_rate

            prev_delta = delta

    def train_iteration(self, X, Y):
        self.set_io(X, Y)
        self.forward_propagation()
        self.backward_propagation()
        self.is_correct()

    def train(self, Xs, Ys, epoch=5):
        print("Start training")
        for i in range(epoch):
            print(f"Epoch {i + 1}")

            for X, Y in zip(Xs, Ys):
                self.train_iteration(X, Y)

            print(f"Correct {self.correct_in_epoch} from {len(Xs)}")
            print(f"Accuracy {self.correct_in_epoch / len(Xs)}\n")
            self.correct_in_epoch = 0

    def get_output(self):
        return self.As[-1]

    def predict(self, X, Y, argmax=False):
        self.set_io(X, Y)
        self.forward_propagation()
        output = self.get_output()
        if argmax:
            output = output.argmax()
            Y = Y.argmax()
        return output, Y


model = NeuralNetwork(neuron_layers=[
    784,
    300,
    100,
    50,
    20,
    10
])

model.train(train_data, train_labels, epoch=10)

while True:
    index = int(input("Enter a number (0 - 59999): "))
    img, label = test_data[index], test_labels[index]
    prediction, label = model.predict(img, label, argmax=True)

    text = f"Prediction: {prediction}  |  Label: {label}\n"
    print(text)

    utils.draw_image(img, text)
