import cv2 as cv
from PIL import Image
import numpy as np

# Afectar pixel por pixel

img = cv.imread('1a.jpg',1)
img_g = cv.imread('1a.jpg',0)
img1 = cv.imread('1a.jpg', 0) # Imagen en escala de grises (1 solo canal)

img2 = np.zeros(img.shape, img.dtype)
img3 = np.zeros(img.shape, img.dtype)
img4 = np.zeros(img.shape, img.dtype)
img5 = np.zeros(img.shape, img.dtype)

x,y=img.shape[:2] # Dimensiones


# Operador de umbral
for i in range(x): 
        for j in range(y):
                if(img_g[i,j]<150): img1[i,j]=255
                else: img1[i,j] = 0

# cv.imwrite('ngOP.png',img)

# Operador de negativo
r, g, b = cv.split(img)

for i in range(x):
        for j in range(y):
                r[i,j] = 255 - r[i,j]
                b[i,j] = 255 - b[i,j]
                g[i,j] = 255 - g[i,j]
img2 = cv.merge([g,b,r])


# Correcion gamma
alpha = 2.0       # Entre 1 y 3
beta = 3        # Entre 0 y 100

for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        for c in range(img.shape[2]):
                img3[y,x,c] = np.clip(int(alpha*img[y,x,c] + beta), 0, 255)

aux = img.astype(np.float32)
log_constant = 255 / np.log(1 + np.max(aux))

# Transformacion logaritmica
for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        for c in range(img.shape[2]):
                img4[y,x,c] = np.clip(int(log_constant * np.log(1+aux[y,x,c])), 0, 255)

img4 = np.uint8(np.clip(img4, 0, 255))

pow_constant = 255
gamma = 0.8
# Raise To Power Transform
for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        for c in range(img.shape[2]):
                img5[y,x,c] = np.clip(int(pow_constant * (img[y,x,c]/255) ** gamma), 0, 255)




cv.imshow('Umbral', img1) # Imagen binarisada
cv.imshow('Negativo', img2) # Imagen negativizada
cv.imshow('Gamma', img3) # Imagen con gamma
cv.imshow('Trans. logaritmica', img4) # Imagen con transformacion logaritmica
cv.imshow('Trans. de potencia', img5) # Imagen con transformacion de potencia

cv.waitKey(0)
cv.destroyAllWindows()
