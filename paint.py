import numpy as np
import cv2 as cv 

img = np.ones((500, 500), dtype=np.uint8) * 240

for i in range(50):
    for j in range(50):
        img[i+200,j+100] = 0


square = 0

for i in range(500):
    for j in range(500):
        if(img[i,j] == 0): square = square + 1

print(square)




cv.imshow('img', img)

cv.waitKey()
cv.destroyAllWindows()