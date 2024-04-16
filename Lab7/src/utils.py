import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def draw_image(img, title):
    plt.imshow(img.reshape(28, 28), cmap="Greys")
    plt.title(title)
    plt.show()


def prepare_label(ys):
    ys = np.int64(ys)
    blank = np.zeros((len(ys), ys.max() + 1))
    for i, y in enumerate(ys):
        blank[i, y] = 1
    return blank


def read_train_data():
    data = np.array(pd.read_csv("dataset/data_train.csv"))
    labels = np.array(pd.read_csv("dataset/target_train.csv"))
    return data, prepare_label(labels)


def read_test_data():
    data = np.array(pd.read_csv("dataset/data_test.csv"))
    labels = np.array(pd.read_csv("dataset/target_test.csv"))
    return data, prepare_label(labels)
