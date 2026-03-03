import os
import numpy as np
import cv2
import tensorflow as tf

# =============================
# Einstellungen
# =============================

IMG_SIZE = 32
MODEL_PATH = "schrift_model.h5"
DATASET_PATH = "BigDataSet_32x32"

# =============================
# Modell & Klassen laden
# =============================

model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False
)

letters = sorted(os.listdir(DATASET_PATH))

print("Klassen:", letters)
print()

# =============================
# Manuelle Prediction
# =============================

while True:

    img_path = input("Bildpfad eingeben (oder 'exit'): ")

    if img_path.lower() == "exit":
        break

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print("❌ Bild konnte nicht geladen werden\n")
        continue

    # ---- Preprocessing wie beim Training ----
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0
    img = img.reshape(1, IMG_SIZE, IMG_SIZE, 1)

    # Prediction
    prediction = model.predict(img, verbose=0)[0]

    class_index = np.argmax(prediction)

    print("\nErgebnis:", letters[class_index])
    print("Wahrscheinlichkeiten:")

    for i, letter in enumerate(letters):
        print(f"{letter} : {prediction[i]*100:.2f}%")

    print("\n-------------------------\n")