import cv2 as cv
import numpy as np
from PIL import Image
import os

# Crea una imagen de 500x500 píxeles, todos con valor 240 (gris claro). 
# La imagen tiene solo un canal (escala de grises) y está inicializada con valores de tipo uint8 (enteros sin signo de 8 bits).
p = 12
size = (p*8)*10
margin = p*3

img = np.ones((size,size), dtype=np.uint8) * 30

x,y = img.shape
midx = x // 2
midy = y // 2

a = Image.new("RGB", (x,y), color="white")
a.save("base.png")
b = Image.new("RGB", (x,y), color="white")
b.save("negativo.png")

# El numero que multiplica a la matriz * x es el color que en este caso es en escala de gris


for i in range(x):
        for j in range(y):
            if(((i > margin and i < (x-margin)) and (j > margin and j < (y-margin)))): img[i,j] = 255



x = (midx)
y = (midy-(p*49//2))

# img[y,x]
for l in range(p): # y = 1 
    for k in range(p*6): # x = 16-22
        if(k < p*4): img[y+l,x+k] = 179   # px 16-20
        else: 
            if(k < p*5): img[y+l,x+k] = 173 # px 21
            else: img[y+l,x+k] = 158     # px 22

y = y + p
x = x - p*6

for l in range(p): # y = 2
    for k in range(p*17): # x = 10-27
        if(k < p*10): img[y+l,x+k] = 179 # px 10-18
        else:
            if(k < p*11): img[y+l,x+k] = 173 # px 19
            else: img[y+l,x+k] = 158 # px 20-27

y = y + p
x = x - p

for l in range(p*2): # y = 3-4
    for k in range(p*19): # x = 9-27
        if(k < p*10): img[y+l,x+k] = 179 # px 9-19
        else:
            if(k < p*11): img[y+l,x+k] = 173 # px 20
            else: img[y+l,x+k] = 158 # px 21-27


y = y + p*2
x = x - p

for l in range(p*2): # y = 5-6
    for k in range(p*20): # x = 8-28
        if(k < p*10): img[y+l,x+k] = 179 # px 8-18
        else:
            if(k < p*11): img[y+l,x+k] = 173 # px 19
            else: img[y+l,x+k] = 158 # px 20-28


y = y + p*2
x = x - p

for l in range(p*2): # y = 7-8
    for k in range(p*22): # x = 7-29
        if(k < p*11): img[y+l,x+k] = 179 # px 7-18
        else:
            if(k < p*12): img[y+l,x+k] = 173 # px 19
            else: img[y+l,x+k] = 158 # px 20-29

y = y + p*2
x = x - p

for l in range(p*2): # y = 9-10
    for k in range(p*23): # x = 6-29
        if(k < p*11): img[y+l, x+k] = 179
        else:
            if(k < p*12): img[y+l, x+k] = 173
            else:
                img[y+l, x+k] = 158

y = y + p*2
x = x - p


for l in range(p): # y = 11
    for k in range(p*24): # x = 5-29
        if(k < p*13): img[y+l, x+k] = 102 # px 6-19
        else: img[y+l, x+k] = 158 # px 19-29

y = y + p

for l in range(p): # y = 12
    for k in range(p*24): # x = 5-29
        if(k < p*18): img[y+l, x+k] = 102 # px 6-19
        else: img[y+l, x+k] = 158 # px 19-29

y = y + p
x = x + p

for l in range(p): # y = 13
    for k in range(p*23): # x = 6-29
        if(k < p*16): img[y+l, x+k] = 102
        else: 
            if(k < p *17): img[y+l,x+k] = 140
            else: img[y+l,x+k] = 158
y = y + p
x = x + p

for l in range(p): # y = 14
    for k in range(p*23): # x = 7-30
        if(k < p*13): img[y+l, x+k] = 102
        else: 
            if(k < p *15): img[y+l,x+k] = 140
            else: img[y+l,x+k] = 158
y = y + p

for l in range(p): # y = 15
    for k in range(p*23): # x = 7-30
        if(k < p*10): img[y+l, x+k] = 102
        else: 
            if(k < p *13): img[y+l,x+k] = 140
            else: 
                img[y+l,x+k] = 158

y = y + p

for l in range(p): # y = 16
    for k in range(p*23): # x = 7-30
        if((k < p*3) or (k < p*8 and k >= p*7)): img[y+l, x+k] = 102
        else: 
            if((k < p *8 and k >= p*3) or (k < p*10 and k >= p*8)): img[y+l,x+k] = 140
            else: 
                img[y+l,x+k] = 158

            
y = y + p
x = x - p

for l in range(p): # y = 17
    for k in range(p*24): # x = 6-30
        if((k < p*4) or (k < p*9 and k >= p*8)): img[y+l,x+k] = 140
        else:
            if((k < p*8 and k >= p*4) or (k < p*24 and k >= p*9)): 
                img[y+l,x+k] = 158

y = y + p

for l in range(p): # y = 18
    for k in range(p*25): # x = 6-31
        if((k < p*6) or (k < p*31 and k >= p*8)): img[y+l,x+k] = 158
        else:
            if(k < p*7): img[y+l,x+k] = 179
            else: img[y+l,x+k] = 173

y = y + p

for l in range(p): # y = 19
    for k in range(p*25): # x = 6-31
        if((k < p*5) or (k < p*31 and k >= p*8)): img[y+l,x+k] = 158
        else:
            if(k < p*7 ): img[y+l,x+k] = 179
            else: img[y+l,x+k] = 173

y = y + p
x = x - p

for l in range(p): # y = 20
    for k in range(p*26): # x = 5-31
        if((k < p*5) or (k < p*20 and k >= p*9) or (k < p*31 and k >= p*22)): img[y+l,x+k] = 158
        else:
            if((k < p*8) or (k < p*22 and k >= p*20)): img[y+l,x+k] = 179
            else: img[y+l,x+k] = 173

y = y + p

for l in range(p): # y = 21
    for k in range(p*26): # x = 5-31
        if((k < p*4) or (k < p*19 and k >= p*8) or (k < p*26 and k >= p*24)): img[y+l,x+k] = 158
        else:
            if((k < p*7) or (k < p*24 and k >= p*19)): img[y+l,x+k] = 179
            else: img[y+l,x+k] = 173

y = y + p
x = x - p

for l in range(p): # y = 22
    for k in range(p*27): # x = 4-31
        if((k < p*4) or (k < p*20 and k >= p*9) or (k < p*27 and k >= p*25)): img[y+l,x+k] = 158
        else:
            if((k < p*8) or (k < p*25 and k >= p*19)): img[y+l,x+k] = 179
            else: img[y+l,x+k] = 173

y = y + p

for l in range(p): # y = 23
    for k in range(p*27): # x = 4-31
        if((k < p*3) or (k < p*20 and k >= p*9) or (k < p*27 and k >= p*26)): img[y+l,x+k] = 158
        else:
            if((k < p*8) or (k < p*26 and k >= p*19)): img[y+l,x+k] = 179
            else: img[y+l,x+k] = 173

y = y + p
x = x - p

for l in range(p): # y = 24
    for k in range(p*28): # x = 3-31
        if((k < p*3) or (k < p*20 and k >= p*10) or (k < p*28 and k >= p*27)): img[y+l,x+k] = 158
        else:
            if((k < p*9) or (k < p*27 and k >= p*19)): img[y+l,x+k] = 179
            else: img[y+l,x+k] = 173

y = y + p
x = x -p

for l in range(p): # y = 25
    for k in range(p*30): # x = 2-32
        if((k < p*21) or (k < p* 30 and k >= p*28)):  img[y+l,x+k] = 158
        else: img[y+l,x+k] = 179
        
y = y + p
x = x -p

for l in range(p): # y = 26
    for k in range(p*31): # x = 1-32
        if((k < p*22) or (k < p* 31 and k >= p*30)):  img[y+l,x+k] = 158
        else: img[y+l,x+k] = 179
        
y = y + p
x = x -p

for l in range(p): # y = 27
    for k in range(p*32): # x = 0-32
        if((k < p*23) or (k < p* 32 and k >= p*31)):  img[y+l,x+k] = 158
        else: img[y+l,x+k] = 179

y = y + p

for l in range(p): #y = 28
    for k in range(p*32): # x = 0-32
        if(k < p*2): img[y+l,x+k] = 102
        else: 
            if((k < p*23 and k >= p*2) or (k < p*32 and k >= p*31)): img[y+l,x+k] = 158
            else: 
                if(k < p*30 and k >= p*23): img[y+l,x+k] = 179
                else: img[y+l,x+k] = 173

y = y + p

for l in range(p): #y = 29
    for k in range(p*33): # x = 0-33
        if((k < p*10) or (k < p*31 and k >= p*30)): img[y+l,x+k] = 102
        else: 
            if((k < p*23 and k >= p*10) or (k < p*33 and k >= p*31)): img[y+l,x+k] = 158
            else: 
                if(k < p*29 and k >= p*25): img[y+l,x+k] = 179
                else: img[y+l,x+k] = 173
                    
y = y + p
x = x + p*2

for l in range(p): # y = 30
    for k in range(p*31): # x = 2-33
        if((k < p*13) or (k < p*23 and k >= p*21)or (k < p*29 and k >= p*27)): img[y+l,x+k] = 102
        else: 
            if((k < p*21 and k >= p*13) or (k < p*31 and k >= p*29)): img[y+l,x+k] = 158
            else: img[y+l,x+k] = 173

y = y + p

for l in range(p): # y = 31
    for k in range(p*31): # x = 2-33
        if((k < p* 12) or (k < p*30 and k >= p*22)): img[y+l, x+k] = 102
        else:
            if((k < p*21 and k >= p*13) or (k < p*31 and k >= p*30)): img[y+l,x+k] = 158
            else: img[y+l,x+k] = 140

y = y + p

for l in range(p): # y = 32
    for k in range(p*31): # x = 2-33
        if((k < p* 11) or (k < p*30 and k >= p*22)): img[y+l, x+k] = 102
        else:
            if((k < p*21 and k >= p*12) or (k < p*31 and k >= p*30)): img[y+l,x+k] = 158
            else: img[y+l,x+k] = 140

y = y + p

for l in range(p): # y = 33
    for k in range(p*31): # x = 2-33
        if((k < p* 9) or (k < p*30 and k >= p*23)): img[y+l, x+k] = 102
        else:
            if((k < p*22 and k >= p*11) or (k < p*31 and k >= p*30)): img[y+l,x+k] = 158
            else: img[y+l,x+k] = 140

y = y + p
x = x - p

for l in range(p): # y = 34
    for k in range(p*32): # x = 1-33
        if(k < p*30 and k >= p*25): img[y+l, x+k] = 102
        else:
            if((k < p*24 and k >= p*10) or (k < p*32 and k >= p*31)): img[y+l,x+k] = 158
            else: img[y+l,x+k] = 140

y = y + p
x = x - p

for l in range(p): # y = 35
    for k in range(p*33): # x = 0-33
        if((k < p*26 and k >= p*2) or (k < p*33 and k >= p*31)): img[y+l,x+k] = 158
        else: 
            if((k < p*2) or (k < p*30 and k >= p*29)): img[y+l,x+k] = 102
            else: img[y+l,x+k] = 140

y = y + p

for l in range(p): # y = 36
    for k in range(p*33): # x = 0-33
        if(k < p*12): img[y+l,x+k] = 102
        else: 
            if((k < p*30 and k >= p*29)): img[y+l,x+k] = 140
            else: img[y+l,x+k] = 158

y = y + p
x = x + p

for l in range(p): # y = 37
    for k in range(p*32): # x = 1-33
        if(k < p*12): img[y+l,x+k] = 102
        else: img[y+l,x+k] = 158

y = y + p
x = x + p

for l in range(p): # y = 38
    for k in range(p*31): # x = 2-33
        if(k < p*11): img[y+l,x+k] = 102
        else: img[y+l,x+k] = 158

y = y + p

for l in range(p*2): # y = 39-40
    for k in range(p*31): # x = 1-33
        if(k < p*10): img[y+l,x+k] = 102
        else: 
            if(k < p*31 and k >= p*11): img[y+l,x+k] = 158
            else: img[y+l,x+k] = 140

y = y + p

for l in range(p): # y = 41
    for k in range(p*31): # x = 2-33
        if(k < p*9): img[y+l,x+k] = 102
        else: 
            if(k < p*31 and k > p*10): img[y+l,x+k] = 158
            else: img[y+l,x+k] = 140

y = y + p

for l in range(p): # y = 42
    for k in range(p*31): # x = 2-33
        if(k < p*9): img[y+l,x+k] = 140
        else: img[y+l,x+k] = 158

y = y + p

for l in range(p): # y = 43
    for k in range(p*31): # x = 2-33
        if(k < p*29 and k >= p): img[y+l,x+k] = 158
        else: img[y+l,x+k] = 102

y = y + p

for l in range(p): # y = 44
    for k in range(p*31): # x = 2-33
        if(k < p*27 and k >= p*2): img[y+l,x+k] = 158
        else: 
            if((k < p*2 and k >= p) or (k < p*31 and k >= p*25)): img[y+l,x+k] = 102 
            else: img[y+l,x+k] = 140

y = y + p
x = x + p

for l in range(p): # y = 45
    for k in range(p*30): # x = 3-33
        if(k < p*24 and k >= p*3): img[y+l,x+k] = 158
        else: 
            if((k < p*3 and k >= p) or (k < p*29 and k >= p*24)): img[y+l,x+k] = 102 
            else: img[y+l,x+k] = 140

y = y + p

for l in range(p): # y = 46
    for k in range(p*29): # x = 3-32
        if(k < p*18 and k >= p*10): img[y+l,x+k] = 158
        else: 
            if((k < p*10 and k >= p) or (k < p*28 and k >= p*18)): img[y+l,x+k] = 102 
            else: img[y+l,x+k] = 140
y = y + p
x = x + p

for l in range(p): # y = 47
    for k in range(p*27): # x = 4-30
        if(k < p*26 and k >= p): img[y+l,x+k] = 102
        else: img[y+l,x+k] = 140

y = y + p
x = x + p

for l in range(p): # y = 48
    for k in range(p*25): # x = 5-30
        if(k < p*22 and k > p*4): img[y+l,x+k] = 102
        else: img[y+l,x+k] = 140

y = y + p
x = x + p*4

for l in range(p): # y = 49
    for k in range(p*18): # x = 9-27
        img[y+l,x+k] = 140


cv.imwrite('base.png',img)
cv.imshow('img',img)


x,y = img.shape

for i in range(x): 
        for j in range(y):
                if(img[i,j]>150): # Operador puntual: Trabajan por punto
                        img[i,j]=255
                else:
                        img[i,j]=0
cv.imshow('img',img)
cv.imwrite('negativo.png', img)
            

cv.waitKey()
cv.destroyAllWindows()