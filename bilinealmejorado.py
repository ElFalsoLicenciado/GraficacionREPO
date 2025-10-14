import cv2 as cv
import numpy as np
import math

img = cv.imread('base.png',0)
x, y = img.shape



def traslacion(original, dx, dy):
    x, y = original.shape
    
    trasladada = np.zeros((x,y), dtype=np.uint8)
        
    for i in range(x):
        for j in range(y):
            new_x = j + dx
            new_y = i + dy
            
            if 0 <= new_x < y and 0 <= new_y < x and new_x < y and new_y < x:  
                trasladada[new_y, new_x] = original[i, j]
    return trasladada

def escalado(original, f):
    x, y = original.shape
    
    escalada = np.zeros((x*f,y*f), dtype=np.uint8)
    
    for i in range(x):
        for j in range(y):
            escalada[int(i*f), int(j*f)] = original[i, j]
            
    return escalada

def rotacion (original, angle):
    x, y = original.shape
    rads = math.radians(angle)
    
    rotada = np.zeros((x,y), dtype=np.uint8)
    
    for i in range(x):
        for j in range(y):
            new_x = int(j * math.cos(rads) + i * math.sin(rads))
            new_y = int(-j * math.sin(rads) + i * math.cos(rads))
            
            if 0 <= new_x < y and 0 <= new_y < x and new_x < y and new_y < x:  
                rotada[new_y, new_x] = original[i, j]
    
    return rotada

def filtro_bilineal (original):
    y, x = original.shape
    #Traajar sobre la copia
    filtrado = original.copy()
    
    for i in range(1, y - 1):
        for j in range(1, x - 1):
            
            if filtrado[i, j] == 0:
                relleno = cruz(original,i,j)
                if(relleno == 0):
                    relleno = diagonal(original,i,j)
                
                filtrado[i,j] = relleno
                
                
    return filtrado
                
            

def cruz(imagen, i,j):
    relleno = 0
    
    arriba = float(imagen[i - 1, j])
    abajo = float(imagen[i + 1, j])
    izquierda = float(imagen[i, j - 1])
    derecha = float(imagen[i, j + 1])
    
    vecinos = []
    if arriba > 0: vecinos.append(arriba)
    if abajo > 0: vecinos.append(abajo)
    if izquierda > 0: vecinos.append(izquierda)
    if derecha > 0: vecinos.append(derecha)
                
    if len(vecinos) > 0:
        relleno = np.clip(int(sum(vecinos) / len(vecinos)), 0 ,255)
    
    return relleno
                

def diagonal(imagen, i,j):
    relleno = 0

    arribaIzq = float(imagen[i - 1, j - 1])
    arribaDer = float(imagen[i - 1, j + 1])
    abajoIzq = float(imagen[i + 1, j - 1])
    abajoDer = float(imagen[i + 1, j + 1])

    vecinos = []
    if arribaIzq > 0: vecinos.append(arribaIzq)
    if arribaDer > 0: vecinos.append(arribaDer)
    if abajoIzq > 0: vecinos.append(abajoIzq)
    if abajoDer > 0: vecinos.append(abajoDer)
                    
    if len(vecinos) > 0:
        relleno = np.clip(int(sum(vecinos) / len(vecinos)), 0 ,255)
    
    return relleno
        
   
   
     

### Imagen 1
# Escalar en factor a 2, aplicar filtro bilineal
# Rotar 45 grados, aplicar filtro bilineal


img1 = escalado(img, 2)
cv.imshow('Escalado', img1)
img1 = filtro_bilineal(img1)
cv.imshow('Filtrado #1', img1)

img1 = rotacion(img1, 45)
cv.imshow('Rotado', img1)
img1 = filtro_bilineal(img1)
cv.imshow('Filtrado #2', img1)

cv.waitKey(0)
cv.destroyAllWindows()

### Imagen 2 
# Escalar 2
# Rotar 45
# Filtro bilineal

img2 = escalado(img, 2)
cv.imshow('Escalado', img2)

img2 = rotacion(img2, 45)
cv.imshow('Rotado', img2)

img2 = filtro_bilineal(img2)
cv.imshow('Filtrado', img2)

cv.waitKey(0)
cv.destroyAllWindows()

### Imagen 3
# Trasladar imagen al centro
# Escalar 2
# Rotar 90
# Filtro bilineal

img3 = traslacion(img, x//2, y//2)
cv.imshow('Traslado', img3)

img3 = escalado(img3, 2)
cv.imshow('Escalado', img3)

img3 = rotacion(img,90)
cv.imshow('Rotado', img3)

img3 = filtro_bilineal(img3)
cv.imshow('Finalizado', img3)

cv.waitKey(0)
cv.destroyAllWindows()
