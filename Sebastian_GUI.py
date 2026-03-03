import os
import numpy as np
import cv2
import tensorflow as tf
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw

IMG_SIZE = 32
MODEL_PATH = "schrift_model.h5"
DATASET_PATH = "BigDataSet_32x32"

model = tf.keras.models.load_model(MODEL_PATH, compile=False)
letters = sorted(os.listdir(DATASET_PATH))


class LetterRecognitionApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Letter Recognition")

        self.canvas_size = 300

        # ================= Canvas =================
        self.canvas = tk.Canvas(root, width=self.canvas_size,
                                height=self.canvas_size, bg="white")
        self.canvas.pack()

        self.image = Image.new("L", (self.canvas_size, self.canvas_size), 255)
        self.draw = ImageDraw.Draw(self.image)

        self.canvas.bind("<B1-Motion>", self.paint)

        # ================= Buttons =================
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Read", command=self.predict).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Clear", command=self.clear).pack(side=tk.LEFT, padx=10)

        # ================= Prediction Output =================
        self.result_label = tk.Label(root, text="Prediction: ",
                                     font=("Arial", 18))
        self.result_label.pack()

        self.confidence_label = tk.Label(root, text="",
                                         font=("Arial", 12))
        self.confidence_label.pack()

        # ================= Wahrscheinlichkeiten =================
        prob_frame = tk.LabelFrame(root, text="Class Probabilities")
        prob_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(prob_frame,
                                 columns=("Letter", "Probability"),
                                 show="headings",
                                 height=10)

        self.tree.heading("Letter", text="Letter")
        self.tree.heading("Probability", text="Probability (%)")

        self.tree.column("Letter", width=80, anchor="center")
        self.tree.column("Probability", width=150, anchor="center")

        scrollbar = ttk.Scrollbar(prob_frame, orient="vertical",
                                  command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # ================= Zeichnen =================

    def paint(self, event):
        r = 8
        x1, y1 = event.x - r, event.y - r
        x2, y2 = event.x + r, event.y + r

        self.canvas.create_oval(x1, y1, x2, y2, fill="black")
        self.draw.ellipse([x1, y1, x2, y2], fill=0)

    # ================= Clear =================

    def clear(self):
        self.canvas.delete("all")
        self.draw.rectangle([0, 0, self.canvas_size,
                             self.canvas_size], fill=255)

        self.result_label.config(text="Prediction: ")
        self.confidence_label.config(text="")

        for row in self.tree.get_children():
            self.tree.delete(row)

    # ================= Prediction =================

    def predict(self):

        img = self.image.resize((IMG_SIZE, IMG_SIZE))
        img = np.array(img)

        img = img / 255.0
        img = img.reshape(1, IMG_SIZE, IMG_SIZE, 1)

        prediction = model.predict(img, verbose=0)[0]

        class_index = np.argmax(prediction)
        predicted_letter = letters[class_index]
        confidence = prediction[class_index] * 100

        self.result_label.config(text=f"Prediction: {predicted_letter}")
        self.confidence_label.config(text=f"Confidence: {confidence:.2f}%")

        # Tabelle leeren
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Sortieren nach Wahrscheinlichkeit
        sorted_indices = np.argsort(prediction)[::-1]

        for i in sorted_indices:
            self.tree.insert("", "end",
                             values=(letters[i],
                                     f"{prediction[i]*100:.2f}"))
        

# ================= Start =================

root = tk.Tk()
app = LetterRecognitionApp(root)
root.mainloop()