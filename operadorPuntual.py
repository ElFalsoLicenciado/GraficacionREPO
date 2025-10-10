import cv2 as cv
from PIL import Image
import numpy as np
import os

# Afectar pixel por pixel

img = cv.imread('1a.jpg',1)
img1 = cv.imread('1a.jpg', 0) # Imagen en escala de grises (1 solo canal)
img2 = cv.imread('1a.jpg', 1)
img3 = np.zeros(img.shape, img.dtype)
img4 = cv.imread('1a.jpg', 1)
img5 = cv.imread('1a.jpg', 1)

x,y=img1.shape[:2] # Dimensiones
a = Image.new("RGB", (x,y), color="white")
# a.save("ngOP.png")


# Operador de umbral
# for i in range(x): 
#         for j in range(y):
#                 if(img1[i,j]<150): img1[i,j]=255
#                 else: img1[i,j]=0

# # cv.imwrite('ngOP.png',img)

# # Operador de negativo
# r, g, b = cv.split(img)

# for i in range(x):
#         for j in range(y):
#                 r[i,j] = 255 - r[i,j]
#                 b[i,j] = 255 - b[i,j]
#                 g[i,j] = 255 - g[i,j]
# img2 = cv.merge([g,b,r])


# # Correcion gamma
# alpha = 2.0       # Entre 1 y 3
# beta = 3        # Entre 0 y 100

# for y in range(img.shape[0]):
#     for x in range(img.shape[1]):
#         for c in range(img.shape[2]):
#                 img3[y,x,c] = np.clip(int(alpha*img[y,x,c] + beta), 0, 255)

log_constant

# Transformacion logaritmica
for y in range(img.shape[0]):
    print(y)
    for x in range(img.shape[1]):
        for c in range(img.shape[2]):
                img3[y,x,c] = np.clip(int(alpha*img[y,x,c] + beta), 0, 255)



# cv.imshow('Umbral', img1) # Imagen binarisada
# cv.imshow('Negativo', img2) # Imagen negativizada
# cv.imshow('Gamma', img3) # Imagen con gamma

cv.waitKey(0)
cv.destroyAllWindows()
