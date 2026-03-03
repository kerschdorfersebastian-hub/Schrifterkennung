from PIL import Image
import os

img = Image.open("4_Bild.png")

# Neue X‑Koordinaten (Spalten)
columns = [
    (0, 32),
    (33, 65),
    (68, 100),
    (102, 134),
    (137, 169),
    (172, 204),
    (205, 237),
    (240, 272),
    (275, 307),
    (313, 345)
]

# Neue Y‑Koordinaten (Zeilen)
rows = [
    (484, 516)
]

# Buchstaben pro Zeile (A–O)
letters = [
    "A", "B", "C", "D", "E",
    "F", "G", "H", "I", "J",
    "K", "L", "M", "N", "O"
]

# Funktion: oben 2 Pixel abschneiden
def cut_top_2px(img):
    w, h = img.size
    return img.crop((0, 2, w, h))

# Funktion: die ersten N Pixelspalten links auf weiß setzen
def clear_left_border(img, border_width=4):
    img = img.convert("RGB")
    pixels = img.load()
    w, h = img.size
    bw = min(border_width, w)

    for y in range(h):
        for x in range(bw):
            pixels[x, y] = (255, 255, 255)  # weiß

    return img

# Ordner anlegen
for letter in letters:
    os.makedirs(letter, exist_ok=True)

# Ausschneiden + oben 2 Pixel weg + linken Rand weiß machen
for r, (y1, y2) in enumerate(rows):
    for c, (x1, x2) in enumerate(columns):

        crop = img.crop((x1, y1, x2, y2))
        crop = cut_top_2px(crop)
        crop = clear_left_border(crop, border_width=4)

        letter = letters[r]
        filename = f"{letter}/{letter}_{r}_{c}_bild_1.png"
        crop.save(filename)

print("Fertig! Oben 2 Pixel abgeschnitten und linke 4 Pixel weiß gesetzt.")
