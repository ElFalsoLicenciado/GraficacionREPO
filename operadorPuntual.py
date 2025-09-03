import cv2 as cv
from PIL import Image
import os

# Afectar pixel por pixel

img = cv.imread('1a.jpg', 0) # Imagen en escala de grises (1 solo canal)
cv.imshow('salida', img)
x,y=img.shape # Dimensiones
a = Image.new("RGB", (x,y), color="white")
a.save("ngOP.png")


for i in range(x): 
        for j in range(y):
                if(img[i,j]<150): # Operador puntual: Trabajan por punto
                        img[i,j]=255
                else:
                        img[i,j]=0

cv.imshow('negativo', img) # Imagen binarisada

cv.imwrite('ngOP.png',img)

cv.imshow('negativo', img) # Imagen binarisada
print( img.shape, x , y)
cv.waitKey(0)
cv.destroyAllWindows()
