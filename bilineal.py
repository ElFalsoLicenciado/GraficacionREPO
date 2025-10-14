import cv2 as cv
import numpy as np
import math
from PIL import Image


### Imagen 1
# Escalar en factor a 2, aplicar filtro bilineal
# Rotar 45 grados, aplicar filtro bilineal


img1 = cv.imread('base.png',0 )
x , y = img1.shape

img1_edited = np.zeros((x*2,y*2), dtype=np.uint8)

xx, yy = img1_edited.shape

# a = Image.new("RGB", (xx,yy), color="white")
# a.save("confiltro.png")


f = 2
angle = 45
theta = math.radians(angle)

# Escalado
for i in range(x):
    for j in range(y):
        new_x = int(j*f) 
        new_y = int(i*f)
        
        if 0 <= new_x < yy and 0 <= new_y < xx and new_x < yy and new_y < xx:  
            img1_edited[new_y, new_x] = img1[i, j]

# Filtro bilineal
for i in range(1,xx-1):
    for j in range(1,yy-1):
        p = 0
        suma = 0
        relleno = 0
        if(img1_edited[i,j] == 0 ):
            cruz = np.array(
                [float(img1_edited[i-1,j]),
                float(img1_edited[i+1,j]),
                float(img1_edited[i,j-1]),
                float(img1_edited[i,j+1])]
            )
            
            for k in range(3):
                if(cruz[k] != 0):
                    p += 1
                    suma += cruz[k]
            
            if(p != 0):
                relleno = np.clip(int(suma/p),0, 255)
                img1_edited[i,j] = relleno
            
            else:
                p = 0
                suma = 0
                relleno = 0
                
                diagonal = np.array(
                    [float(img1_edited[i - 1, j - 1]),
                    float(img1_edited[i - 1, j + 1]),
                    float(img1_edited[i + 1, j - 1]),
                    float(img1_edited[i + 1, j + 1])]
                )
                
                for k in range(3):
                    if(diagonal[k] != 0):
                        p += 1
                        suma += diagonal[k]
                
                if(p != 0):
                    relleno = np.clip(int(suma/p),0, 255)
                    img1_edited[i,j] = relleno
                         
img1_edited_final = np.zeros((x*2,y*2), dtype=np.uint8)
# Rotado
for i in range(x):
    for j in range(y):
        new_x = int(j * math.cos(theta) + i * math.sin(theta))
        new_y = int(-j * math.sin(theta) + i * math.cos(theta))
        
        if 0 <= new_x < yy and 0 <= new_y < xx and new_x < yy and new_y < xx:  
            img1_edited_final[new_y, new_x] = img1_edited[i, j]

# Filtro bilineal
for i in range(1,xx-1):
    for j in range(1,yy-1):
        p = 0
        suma = 0
        relleno = 0
        if(img1_edited_final[i,j] == 0 ):
            cruz = np.array(
                [float(img1_edited_final[i-1,j]),
                float(img1_edited_final[i+1,j]),
                float(img1_edited_final[i,j-1]),
                float(img1_edited_final[i,j+1])]
            )
            
            for k in range(3):
                if(cruz[k] != 0):
                    p += 1
                    suma += cruz[k]
            
            if(p != 0):
                relleno = np.clip(int(suma/p),0, 255)
                img1_edited_final[i,j] = relleno
            
            else:
                p = 0
                suma = 0
                relleno = 0
                
                diagonal = np.array(
                    [float(img1_edited_final[i - 1, j - 1]),
                    float(img1_edited_final[i - 1, j + 1]),
                    float(img1_edited_final[i + 1, j - 1]),
                    float(img1_edited_final[i + 1, j + 1])]
                )
                
                for k in range(3):
                    if(diagonal[k] != 0):
                        p += 1
                        suma += diagonal[k]
                
                if(p != 0):
                    relleno = np.clip(int(suma/p),0, 255)
                    img1_edited_final[i,j] = relleno

cv.imshow('Original', img1)
cv.imshow('Imagen editada', img1_edited_final)
cv.waitKey(0)
cv.destroyAllWindows()

### Imagen 2 
# Escalar 2
# Rotar 45
# Filtro bilineal


img2 = cv.imread('base.png',0 )
x , y = img2.shape

img2_edited = np.zeros((x*2,y*2), dtype=np.uint8)

xx, yy = img2_edited.shape


f = 2
angle = 45
theta = math.radians(angle)

# Escalado y rotado

for i in range(x):
    for j in range(y):
        new_x = int((((j) * math.cos(theta) + (i) * math.sin(theta))*f)) 
        new_y = int(((- (j) * math.sin(theta) + (i) * math.cos(theta))*f))
        
        if 0 <= new_x < yy and 0 <= new_y < xx and new_x < yy and new_y < xx:  
            img2_edited[new_y, new_x] = img2[i, j]

for i in range(1,xx-1):
    for j in range(1,yy-1):
        p = 0
        suma = 0
        relleno = 0
        if(img2_edited[i,j] == 0 ):
            cruz = np.array(
                [float(img2_edited[i-1,j]),
                float(img2_edited[i+1,j]),
                float(img2_edited[i,j-1]),
                float(img2_edited[i,j+1])]
            )
            
            for k in range(3):
                if(cruz[k] != 0):
                    p += 1
                    suma += cruz[k]
            
            if(p != 0):
                relleno = np.clip(int(suma/p),0, 255)
                img2_edited[i,j] = relleno
            
            else:
                p = 0
                suma = 0
                relleno = 0
                
                diagonal = np.array(
                    [float(img2_edited[i - 1, j - 1]),
                    float(img2_edited[i - 1, j + 1]),
                    float(img2_edited[i + 1, j - 1]),
                    float(img2_edited[i + 1, j + 1])]
                )
                
                for k in range(3):
                    if(diagonal[k] != 0):
                        p += 1
                        suma += diagonal[k]
                
                if(p != 0):
                    relleno = np.clip(int(suma/p),0, 255)
                    img1_edited[i,j] = relleno


cv.imshow('Original', img2)
cv.imshow('Imagen editada', img2_edited)
cv.waitKey(0)
cv.destroyAllWindows()


### Imagen 3
# Trasladar imagen al centro
# Escalar 2
# Rotar 90
# Filtro bilineal

img3 = cv.imread('base.png',0 )
x , y = img3.shape

img3_edited = np.zeros((x*2,y*2), dtype=np.uint8)

xx, yy = img3_edited.shape

cx = (xx - x)//2
cy = (yy - y)//2

f = 2

# Centrado
for i in range(x):
    for j in range(y):
        new_x =  j + cy
        new_y =  i + cx
        
        if 0 <= new_x < yy and 0 <= new_y < xx and new_x < yy and new_y < xx:  
            img3_edited[new_y, new_x] = img3[i, j]

img3_edited_final = np.zeros((x*2,y*2), dtype=np.uint8)

## Escalado
for i in range(x):
    for j in range(y):
        new_x = int(j*f) 
        new_y = int(i*f)
        
        if 0 <= new_x < yy and 0 <= new_y < xx and new_x < yy and new_y < xx:  
            img3_edited_final[new_y, new_x] = img3_edited[i, j]

## Filtro bilineal
for i in range(1,xx-1):
    for j in range(1,yy-1):
        p = 0
        suma = 0
        relleno = 0
        if(img3_edited_final[i,j] == 0 ):
            cruz = np.array(
                [float(img3_edited_final[i-1,j]),
                float(img3_edited_final[i+1,j]),
                float(img3_edited_final[i,j-1]),
                float(img3_edited_final[i,j+1])]
            )
            
            for k in range(3):
                if(cruz[k] != 0):
                    p += 1
                    suma += cruz[k]
            
            if(p != 0):
                relleno = np.clip(int(suma/p),0, 255)
                img3_edited_final[i,j] = relleno
            
            else:
                p = 0
                suma = 0
                relleno = 0
                
                diagonal = np.array(
                    [float(img3_edited_final[i - 1, j - 1]),
                    float(img3_edited_final[i - 1, j + 1]),
                    float(img3_edited_final[i + 1, j - 1]),
                    float(img3_edited_final[i + 1, j + 1])]
                )
                
                for k in range(3):
                    if(diagonal[k] != 0):
                        p += 1
                        suma += diagonal[k]
                
                if(p != 0):
                    relleno = np.clip(int(suma/p),0, 255)
                    img3_edited_final[i,j] = relleno



cv.imshow('Original', img3)
cv.imshow('Imagen editada', img3_edited_final)
cv.waitKey(0)
cv.destroyAllWindows()
