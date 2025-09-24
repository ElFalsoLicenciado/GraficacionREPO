import numpy as np
import cv2

width, height = 1000, 600
img = np.ones((height, width, 3), dtype=np.uint8) * 255

r = 50                 
theta_increment = 0.05  
theta = 0
i_x, i_y = 50, height // 2              

while True:
    img = np.ones((height, width, 3), dtype=np.uint8) * 255

    for t in np.arange(0, theta, theta_increment):
        x = int(r * (t - np.sin(t))) + i_x  
        y = int(r * (1 - np.cos(t)))*-1 + i_y

        if 0 <= x < width and 0 <= y < height:
            cv2.circle(img, (x, y), 2, (0, 0, 0), -1)

    
    cv2.imshow("Parametrica de una cicloide", img)

    theta += theta_increment

    if r * (theta - np.sin(theta)) > width - 50:
        theta = 0

    if cv2.waitKey(10) & 0xFF == 27:
        break

cv2.destroyAllWindows()
