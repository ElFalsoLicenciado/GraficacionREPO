import cv2 as cv
import numpy as np
import math

### Imagen 1
# Escalar en factor a 2, aplicar filtro bilineal
# Rotar 45 grados, aplicar filtro bilineal

img1 = cv.imread('fgeed.jpg',0 )
x , y = img1.shape

img1_edited = np.zeros((x*2,y*2), dtype=np.uint8)

xx, yy = img1_edited.shape

print(img1.shape)

print(img1_edited.shape)

f = 2
angle = 45
theta = math.radians(angle)

for i in range(x):
    for j in range(y):
        new_x = int((((j) * math.cos(theta) + (i) * math.sin(theta))*f)) 
        new_y = int(((- (j) * math.sin(theta) + (i) * math.cos(theta))*f))
        
        if 0 <= new_x < yy and 0 <= new_y < xx and new_x < yy and new_y < xx:  
            img1_edited[new_y, new_x] = img1[i, j]
        
cv.imshow('Original', img1)
cv.imshow('Imagen editada', img1_edited)
cv.waitKey(0)
cv.destroyAllWindows()

### Imagen 2 
# Escalar 2
# Rotar 45
# Filtro bilineal

### Imagen 3
# Trasladar imagen al centro
# Escalar 2
# Filtro bilineal