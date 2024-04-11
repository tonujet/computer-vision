import os, shutil

import cv2
from keras.applications.vgg16 import VGG16, preprocess_input
from sklearn.cluster import KMeans
import keras.utils as image
import numpy as np
import matplotlib.pyplot as plt


def clusterize_solar_panels(num_clusters, src_dir=r"./dataset", target_dir=r"./result"):
    image.LOAD_TRUNCATED_IMAGES = True
    model = VGG16(weights='imagenet', include_top=False)

    img_files = []
    with os.scandir(src_dir) as files:
        for file in files:
            if file.name.endswith('.png'):
                img_files.append(file)

    features = []
    for i, img_path in enumerate(map(lambda e: e.path, img_files)):
        img = image.load_img(img_path, target_size=(224, 224))
        img = np.array(img)
        img_data = np.expand_dims(img, axis=0)
        img_data = preprocess_input(img_data)
        feature = np.array(model.predict(img_data))
        features.append(feature.flatten())


    kmeans = KMeans(n_clusters=num_clusters, init='k-means++', n_init=10, random_state=0).fit(np.array(features))
    clusters = {}
    for i, m in enumerate(kmeans.labels_):
        out = os.path.join(target_dir, str(m))
        img_path = img_files[i].path
        if m not in clusters:
            clusters[m] = []
        clusters[m].append(img_path)
        shutil.copy(img_path, out + "_" + str(i) + ".png")
    return clusters


def view_clusters(clusters):
    def view_cluster(i):
        plt.figure(figsize=(20, 20))
        files = clusters[i]

        for index, file in enumerate(files):
            plt.subplot(4, 4, index + 1)
            img = image.load_img(file)
            img = np.array(img)
            plt.imshow(img)
            plt.axis('off')

    for i in range(len(clusters.keys())):
        view_cluster(i)
    plt.show()


clusters = clusterize_solar_panels(num_clusters=6)
view_clusters(clusters)
