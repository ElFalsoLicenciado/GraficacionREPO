import cv2 as cv
import numpy as np
import math

s_x = 500 # Ancho
s_y = 300 # Alto


# Imagen y su inicializacion
img = np.ones((s_y,s_x,3), dtype=np.uint8)*255

# Variables para el sentido de la pelota
d_x = 6
d_y = 6

# Variables para el centro de la pelota
i = 49
j = 21

# Variables para el centro de la evasora
I = s_x//2
J = s_y//2

time  = 0


while(True):
    
    time += 1
    # Sirve para que la imagen se vuelva a hacer    
    img = np.ones((s_y,s_x,3), dtype=np.uint8)*255
    
    # Pelota rebotadora
    cv.circle(img, (i, j), 20, (40,241,20), -1)
    # Pelota evasora
    cv.circle(img, (I, J), 20, (190,251,96), -1)
    
    # Incremento en posicion de la reobotadora
    i = i + d_x
    j = j + d_y
    
    # Condicion para que rebote con los bordes
    if((i >= s_x-20) or (i <= 19)): d_x = d_x*-1 
    if((j >= s_y-20) or (j <= 19)): d_y = d_y*-1 
    
    # Debug
    
    # Condicion para cuando la rebotadora se vaya acercando, si la distancia es menor o igual a 100 se mueva
    if(math.sqrt((I - i)**2 + (J - j)**2) <= 100):
        # Se mueve en sentido contrario a la pelota
        I = I + (-1*d_x)
        J = J + (-1*d_y)
        print(time)
        print("CERCA")
        
    cv.imshow('img', img)

    if cv.waitKey(30) & 0xF77 == 27:
        break

    
cv.destroyAllWindows()

    