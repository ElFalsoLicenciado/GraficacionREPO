import cv2 as cv
import numpy as np
import math

# Cargar la imagen en escala de grises
img = cv.imread('base.png', 0)

# Obtener el tamaño de la imagen
x, y = img.shape

# Crear una imagen vacía para almacenar el resultado
rotated_img = np.ones((x*2, y*2), dtype=np.uint8)*234 # Multiplicado por 2, escala la imagen * 2

xx, yy = rotated_img.shape

cx, cy = int(yy // 2), int(xx  // 2)

for i in range(x):
    for j in range(y):
        new_x = j + cx//2
        new_y = i + cy//2
        if 0 <= new_x < yy and 0 <= new_y < xx:
            rotated_img[new_y, new_x] = img[i, j]
            
cv.imshow('Imagen Original', img)
cv.imshow('Imagen Rotada (modo raw)', rotated_img)
cv.waitKey(0)
cv.destroyAllWindows()
        