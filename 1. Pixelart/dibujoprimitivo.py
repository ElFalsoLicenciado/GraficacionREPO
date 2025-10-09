import cv2 as cv
import numpy as np

img = np.ones((500,500,3), np.uint8) *100


s = 3

p1= 50

b = 0

cv.rectangle(img, (p1, 50), (p1 + 25 * s,50 + (145) * s), (255,255,255), -1)

p1 = p1 + 25 * s

cv.rectangle(img, (p1, 50), (p1 + 25 * s,50 + (145) * s), (255,255,255), -1)

# print(p1)

b = (int) (p1 - 12 )

# print(b)

cv.rectangle(img, (b, 50), (b + 12 * s,50 + (90) * s), (1,1,1), -1)

cv.line(img, (p1+6, 50+90*s), (p1+6,50+145*s), (70,70,70), 1)


p1 = p1 + 25 * s

cv.rectangle(img, (p1, 50), (p1 + 25 * s,50 + (145) * s), (255,255,255), -1)

# print(p1)

b = (int) (p1 - 12 )

# print(b)

cv.rectangle(img, (b, 50), (b + 12 * s,50 + (90) * s), (1,1,1), -1)

cv.line(img, (p1+6, 50+90*s), (p1+6,50+145*s), (70,70,70), 1)


p1 = p1 + 25 * s

cv.rectangle(img, (p1, 50), (p1 + 25 * s,50 + (145) * s), (255,255,255), -1)

# print(p1)

b = (int) (p1 - 12 )

# print(b)

cv.rectangle(img, (b, 50), (b + 12 * s,50 + (90) * s), (1,1,1), -1)

cv.line(img, (p1+6, 50+90*s), (p1+6,50+145*s), (70,70,70), 1)


p1 = p1 + 25 * s

cv.rectangle(img, (p1, 50), (p1 + 25 * s,50 + (145) * s), (255,255,255), -1)


cv.line(img, (p1+6, 50), (p1+6,50+145*s), (70,70,70), 1)


# print(p1)

p1 = p1 + 25 * s

cv.rectangle(img, (p1, 50), (p1 + 25 * s,50 + (145) * s), (255,255,255), -1)

# print(p1)

b = (int) (p1 - 12 )

# print(b)

cv.rectangle(img, (b, 50), (b + 12 * s,50 + (90) * s), (1,1,1), -1)

cv.line(img, (p1+6, 50+90*s), (p1+6,50+145*s), (70,70,70), 1)


cv.imshow('img',img)
cv.waitKey(0)
cv.destroyAllWindows()

