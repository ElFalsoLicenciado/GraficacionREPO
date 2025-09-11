import numpy as np
import cv2 as cv 

img = np.ones((500, 500), dtype=np.uint8) * 240

# Crear una mancha


# center = (500 // 2, 500 // 2)   # (x, y)
# radius = 500 // 4                # radius of circle
# color = (0, 0, 0)                 # black
# thickness = 5                     # line thickness (-1 fills the circle)

# cv.circle(img, center, radius, color, thickness)

for i in range(50):
    for j in range(50):
        img[i+200,j+100] = 0

# Variable para contar los cuadras

square = 0

# ciclo para calcular el area

c_x = 0
c_y = 0


for i in range(500):
    for j in range(500):
        if(img[i,j] == 0): 
            square = square + 1
            c_x = c_x + j
            c_y = c_y + i

print(c_x//square)
print(c_y//square)


for i in range(10):
    for j in range(10):
        img[c_y//square+i-5,c_x//square+j-5] = 100        

# print(square)




cv.imshow('img', img)

cv.waitKey()
cv.destroyAllWindows()