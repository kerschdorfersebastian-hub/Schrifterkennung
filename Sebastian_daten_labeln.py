import os
import numpy as np
import cv2

DATASET_PATH = "BigDataSet_32x32"
IMG_SIZE = 32


images = []
labels = []

classes = sorted(os.listdir(DATASET_PATH))

for class_index, class_name in enumerate(classes):

    class_folder = os.path.join(DATASET_PATH, class_name)

    for img_name in os.listdir(class_folder):

        img_path = os.path.join(class_folder, img_name)

        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue

        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        img = img / 255.0

        images.append(img)
        labels.append(class_index)

# Array formen
X = np.array(images).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
y = np.array(labels)

# Dateien speichern
np.save("X.npy", X)
np.save("y.npy", y)

print("Fertig! X.npy und y.npy wurden erstellt.")