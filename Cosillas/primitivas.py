import cv2 as cv
import numpy as np

img = np.ones((500,500,3), np.uint8) *150


# (imagen, punto central, tamano de radio, color, thickness)
cv.circle(img,(255,255), 100, (23, 43, 144), -1)

# (imagen, punto 1, punto 2, color, thickness)
cv.rectangle(img, (10,10), (200,200), (34,50,100), -1)



# (imagen, punto 1, punto 2, color, thickness)
cv.line(img, (255,255), (200,100), (250,21,24), -1)


for i in range(400):
    cv.circle(img,(i,i), 6, (23, 43, 144), -1)
    cv.imshow('img', img)
    #img = np.ones((500,500,3), np.uint8) *150
    cv.waitKey(30)


cv.imshow('img',img)
cv.waitKey(0)
cv.destroyAllWindows()
