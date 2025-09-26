import cv2
import numpy as np


camara = cv2.VideoCapture(0)

# Creamos un lienzo vacío
ret, cuadro = camara.read()
lienzo = np.zeros_like(cuadro)

# Rango del color rojo en HSV
u_bajo = np.array([40, 50, 50])
u_alto = np.array([80, 255, 255])


blue = (255,0,0)
green = (0,255,0)
red = (0,0,255)
yellow = (57,247,255)

pink = (251,81,255)
brown = (28,44,82)
aqua = (255,237,11)
orange = (72,143,240)

punto_anterior = None
umbral_distancia = 50  # para evitar trazos largos falsos

while True:
    ret, cuadro = camara.read()
    if not ret:
        break
    
    hsv = cv2.cvtColor(cuadro, cv2.COLOR_BGR2HSV)
    mascara = cv2.inRange(hsv, u_bajo, u_alto)
    cv2.rectangle(cuadro, (20,20), (110,100), blue, -1) # Rectangulo azul
    cv2.rectangle(cuadro, (120,20), (210,100), green, -1) # Rectangulo verde
    cv2.rectangle(cuadro, (220,20), (310,100), red, -1) # Rectangulo rojo
    cv2.rectangle(cuadro, (320,20), (410,100), yellow, -1) # Rectangulo amarillo
    
    
    cv2.rectangle(cuadro, (1510,20), (1600,100), pink, -1) # Rectangulo rosa
    cv2.rectangle(cuadro, (1610,20), (1700,100), brown, -1) # Rectangulo cafe
    cv2.rectangle(cuadro, (1710,20), (1800,100), aqua, -1) # Rectangulo aqua
    cv2.rectangle(cuadro, (1810,20), (1900,100), orange, -1) # Rectangulo naranja
    
    
    

    # Momentos de la máscara (para calcular el centroide)
    momentos = cv2.moments(mascara)
    if momentos["m00"] > 0:  # hay píxeles del color buscado
        cx = int(momentos["m10"] / momentos["m00"])
        cy = int(momentos["m01"] / momentos["m00"])
        punto_actual = (cx, cy)

        # Dibujar punto en la cámara
        cv2.circle(cuadro, punto_actual, 5, (0, 0, 255), -1)

        # Dibujar línea en el lienzo si el salto no es muy grande
        if punto_anterior is not None:
            distancia = np.linalg.norm(np.array(punto_actual) - np.array(punto_anterior))
            if distancia < umbral_distancia:
                cv2.line(lienzo, punto_anterior, punto_actual, (0, 255, 0), 5)

        punto_anterior = punto_actual
    else:
        punto_anterior = None

    combinado = cv2.add(cuadro, lienzo)

    cv2.imshow("Dibujo en vivo", combinado)
    cv2.imshow("Mascara de color", mascara)
    cv2.imshow("Lienzo", lienzo)
    tecla = cv2.waitKey(1) & 0xFF
    if tecla == 27:  # ESC para salir
        break
    elif tecla == ord('c'):  # limpiar lienzo
        lienzo = np.zeros_like(cuadro)

camara.release()
cv2.destroyAllWindows()
