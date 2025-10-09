import cv2
import numpy as np


camara = cv2.VideoCapture(0)

# Creamos un lienzo vacío
ret, cuadro = camara.read()
lienzo = np.zeros_like(cuadro)

# Rango del color rojo en HSV
u_bajo = np.array([100, 50, 50])
u_alto = np.array([130, 255, 255])


blue = (255,0,0)
green = (0,255,0)
red = (0,0,255)
yellow = (57,247,255)

pink = (251,81,255)
brown = (28,44,82)
aqua = (255,237,11)
orange = (72,143,240)

cu_color = green
cu_shape = 0

punto_anterior = None
umbral_distancia = 50  # para evitar trazos largos falsos

size = 10

bx_1 = 200
bx_2 = 250

while True:
    
    h, w= 1050, 1680
    
    ret, cuadro = camara.read()
    if not ret:
        break
    
    hsv = cv2.cvtColor(cuadro, cv2.COLOR_BGR2HSV)
    mascara = cv2.inRange(hsv, u_bajo, u_alto)
    cv2.rectangle(cuadro, (int(w*0.01),20), (int(w*0.05),100), blue, -1) # Rectangulo azul
    cv2.rectangle(cuadro, (int(w*0.06),20), (int(w*0.10),100), green, -1) # Rectangulo verde
    cv2.rectangle(cuadro, (int(w*0.11),20), (int(w*0.15),100), red, -1) # Rectangulo rojo
    cv2.rectangle(cuadro, (int(w*0.16),20), (int(w*0.20),100), yellow, -1) # Rectangulo amarillo
    
    
    cv2.rectangle(cuadro, (int(w*0.80),20), (int(w*0.84),100), brown, -1) # Rectangulo cafe
    cv2.rectangle(cuadro, (int(w*0.85),20), (int(w*0.89),100), pink, -1) # Rectangulo rosa
    cv2.rectangle(cuadro, (int(w*0.90),20), (int(w*0.94),100), aqua, -1) # Rectangulo aqua
    cv2.rectangle(cuadro, (int(w*0.95),20), (int(w*0.99),100), orange, -1) # Rectangulo naranja
    
    
    mid_y = h // 2

    # Botón "+"
    cv2.rectangle(cuadro, (bx_1,int(mid_y*.92)), (bx_2,int(mid_y*1.01)), (255,255,255), -1)
    cv2.putText(cuadro, "+", (bx_1,int(mid_y)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3)

    # Botón "-"
    cv2.rectangle(cuadro, (bx_1,int(mid_y*1.12)), (bx_2,int(mid_y*1.21)), (255,255,255), -1)
    cv2.putText(cuadro, "-", (bx_1, int(mid_y*1.2)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3)
    
    # Botón "circulo"
    cv2.rectangle(cuadro, (bx_1,int(mid_y*1.52)), (bx_2,int(mid_y*1.61)), (255,255,255), -1)
    cv2.circle(cuadro, ((bx_2+bx_1)//2, int(mid_y*1.565)), int(h*0.018) , (0,0,0), -1)

    # Boton "rectangulo"
    cv2.rectangle(cuadro, (bx_1,int(mid_y*1.32)), (bx_2,int(mid_y*1.41)), (255,255,255), -1)
    cv2.rectangle(cuadro, (int(bx_1*1.05),int(mid_y*1.335)), (int(bx_2*0.95),int(mid_y*1.40)), (0,0,0), -1)

    # Boton "linea"
    cv2.rectangle(cuadro, (bx_1,int(mid_y*1.72)), (bx_2,int(mid_y*1.81)), (255,255,255), -1)
    cv2.line(cuadro, (int(bx_1*1.04),int(mid_y*1.73)), (int(bx_2*0.99),int(mid_y*1.794)), (0,0,0), 5)

    # cv2.line(lienzo, punto_anterior, punto_actual, cu_color, 5)

    

    

    # Momentos de la máscara (para calcular el centroide)
    momentos = cv2.moments(mascara)
    if momentos["m00"] > 0:  # hay píxeles del color buscado
        cx = int(momentos["m10"] / momentos["m00"])
        cy = int(momentos["m01"] / momentos["m00"])
        punto_actual = (cx, cy)

        if((cx >= bx_1 and cx <= bx_2) and (cy >= int(mid_y*.92) and cy <= (mid_y*1.01) and size <= 800)):
            size+=2
            print("Mas")
            
        if((cx >= bx_1 and cx <= bx_2) and (cy >= int(mid_y*1.12) and cy <= (mid_y*1.21) and size >= 10)):
            size-=2
            print("Menos")
        
        if((cx >= bx_1 and cx <= bx_2) and (cy >= int(mid_y*1.32) and cy <= (mid_y*1.41))):
            cu_shape = 1
            print("Cuadrado")
            
        if((cx >= bx_1 and cx <= bx_2) and (cy >= int(mid_y*1.52) and cy <= (mid_y*1.61))):
            cu_shape = 0
            print("Circulo")
            
        if((cx >= bx_1 and cx <= bx_2) and (cy >= int(mid_y*1.72) and cy <= (mid_y*1.81))):
            cu_shape = 2
            print("Linea")
        
        if((cx >= int(w*0.01) and cx <= int(w*0.05)) and (cy <= 100 and cy >= 20)):
            print("Blue")
            cu_color = blue
        
        if((cx >= int(w*0.06) and cx <= int(w*0.010)) and (cy <= 100 and cy >= 20)):
            print("Green")
            cu_color = green
            
        if((cx >= int(w*0.11) and cx <= int(w*0.15)) and (cy <= 100 and cy >= 20)):
            print("Rojo")
            cu_color = red
            
        if((cx >= int(w*0.16) and cx <= int(w*0.20)) and (cy <= 100 and cy >= 20)):
            print("Amarillo")
            cu_color = yellow
        
        if((cx >= int(w*0.85) and cx <= int(w*0.89)) and (cy <= 100 and cy >= 20)):
            print("Pink")
            cu_color = pink
            
        if((cx >= int(w*0.80) and cx <= int(w*0.80)) and (cy <= 100 and cy >= 20)):
            print("Brown")
            cu_color = brown

        if((cx >= int(w*0.90) and cx <= int(w*0.94)) and (cy <= 100 and cy >= 20)):
            print("Aqua")
            cu_color = aqua
            
        if((cx >= int(w*0.95) and cx <= int(w*0.99)) and (cy <= 100 and cy >= 20)):
            print("Orange")
            cu_color = orange
        
        print(f"{cx},{cy}")
        
        # Dibujar punto en la cámara
        match cu_shape:
            case 0: 
                cv2.circle(cuadro, punto_actual, size, cu_color, -1)
                cv2.circle(lienzo, punto_actual, size, cu_color, -1)
            case 1: 
                cv2.rectangle(cuadro,(cx-size, cy-size), (cx+size, cy+size), cu_color,-1)
                cv2.rectangle(lienzo,(cx-size, cy-size), (cx+size, cy+size), cu_color,-1)
            case 2:# Dibujar línea en el lienzo si el salto no es muy grande
                cv2.circle(cuadro, punto_actual, size, cu_color, -1)
                if punto_anterior is not None:
                    distancia = np.linalg.norm(np.array(punto_actual) - np.array(punto_anterior))
                    if distancia < umbral_distancia: cv2.line(lienzo, punto_anterior, punto_actual, cu_color, size)

        punto_anterior = punto_actual
    else:
        punto_anterior = None

    combinado = cv2.add(cuadro, lienzo)

    cv2.imshow("Mascara de color", mascara)
    # cv2.imshow("Lienzo", lienzo)
    cv2.imshow("Dibujo en vivo", combinado)
    
    tecla = cv2.waitKey(1) & 0xFF
    if tecla == 27:  # ESC para salir
        break
    elif tecla == ord('c'):  # limpiar lienzo
        lienzo = np.zeros_like(cuadro)

camara.release()
cv2.destroyAllWindows()
