import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

camara = cv2.VideoCapture(0)

ret, frame = camara.read()
lienzo = np.zeros_like(frame)                      # Lienzo para colorear

mode_names = ("paint", "figures")

cooldown = 0
cooldown_frames = 15

# Declaracion de variables para los colores
blue = (255,0,0) 
green = (0,255,0)
red = (0,0,255)
yellow = (57,247,255)

pink = (251,81,255)
brown = (28,44,82)
aqua = (255,237,11)
orange = (72,143,240)

cu_color = green                                    # Color seleccionado
cu_shape = "line"                                 # Figura de la brocha
cu_mode = mode_names[0]                                    # Modo de paint o dibujo de primitivas
size = 10                                           # Tamaño de la brocha                   


last_point = None
max_length = 50

bx_1 = 100
bx_2 = 150


while camara.isOpened():                            # Ciclo para examinar los frames
    
    ret, frame = camara.read()                      # Obtener el fotograma
    
    h, w, = 1200, 1920                              # Obtener la anchura y altura del frame
    
    if not ret: break
    
    frame = cv2.flip(frame,1)                       # Girar el video
    
    # Cambiar de BRG a RGB para que charche
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
    
    results = hands.process(frame_rgb)
    
    left_index = None
    right_index = None
    

    
    # Detectar los landmarks que queremos
    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            label = handedness.classification[0].label      # Clasificacion: Left o Right
            
            index_tip = hand_landmarks.landmark[8]
            x,y = int(index_tip.x* w), int(index_tip.y * h) # Coordenadas del indice
            
            if label == 'Left': 
                left_index = (x,y)
                cv2.circle(frame, left_index, 4, red, -1)     # Circulo rojo en izquierdo
                
            elif label == 'Right': 
                right_index = (x,y)
                cv2.circle(frame, right_index, 4, blue, -1)   # Circulo azul en derecho
    

    cv2.rectangle(frame, (int(w*0.425),20), (int(w*0.475),100), (255,255,255), -1)                       # Cambiar de modo
    cv2.putText(frame, cu_mode , (int(w*0.430),70), cv2.FONT_HERSHEY_SIMPLEX, 0.80, (0,0,0), 2)

    cv2.rectangle(frame, (int(w*0.525),20), (int(w*0.575),100), (255,255,255), -1)                       # Limpiar lienzo
    cv2.putText(frame, "Limpiar", (int(w*0.527),70), cv2.FONT_HERSHEY_SIMPLEX, 0.80, (0,0,0), 2)
    
    
    if cu_mode == "paint":
        cv2.rectangle(frame, (int(w*0.01),20), (int(w*0.05),100), blue, -1)                             # Azul
        cv2.rectangle(frame, (int(w*0.06),20), (int(w*0.10),100), green, -1)                            # Verde
        cv2.rectangle(frame, (int(w*0.11),20), (int(w*0.15),100), red, -1)                              # Rojo
        cv2.rectangle(frame, (int(w*0.16),20), (int(w*0.20),100), yellow, -1)                           # Amarillo
        
        
        cv2.rectangle(frame, (int(w*0.80),20), (int(w*0.84),100), brown, -1)                            # Cafe
        cv2.rectangle(frame, (int(w*0.85),20), (int(w*0.89),100), pink, -1)                             # Rosa
        cv2.rectangle(frame, (int(w*0.90),20), (int(w*0.94),100), aqua, -1)                             # Aqua
        cv2.rectangle(frame, (int(w*0.95),20), (int(w*0.99),100), orange, -1)                           # Naranja
        
        mid_y = h // 2


        cv2.rectangle(frame, (bx_1,int(mid_y*.85)), (bx_2,int(mid_y*0.94)), (255,255,255), -1)          # Botón "+"
        cv2.putText(frame, "+", (bx_1,int(mid_y*.93)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3)

        
        cv2.rectangle(frame, (bx_1,int(mid_y*1.05)), (bx_2,int(mid_y*1.14)), (255,255,255), -1)         # Botón "-"
        cv2.putText(frame, "-", (bx_1, int(mid_y*1.13)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3)
    
        
        cv2.rectangle(frame, (bx_1,int(mid_y*1.25)), (bx_2,int(mid_y*1.34)), (255,255,255), -1)         # Boton "rectangulo"
        cv2.rectangle(frame, (int(bx_1*1.05),int(mid_y*1.265)), (int(bx_2*0.95),int(mid_y*1.33)), (0,0,0), -1)
    
        
        
        cv2.rectangle(frame, (bx_1,int(mid_y*1.45)), (bx_2,int(mid_y*1.54)), (255,255,255), -1)         # Botón "circulo"
        cv2.circle(frame, ((bx_2+bx_1)//2, int(mid_y*1.495)), int(h*0.018) , (0,0,0), -1)

        
        cv2.rectangle(frame, (bx_1,int(mid_y*1.65)), (bx_2,int(mid_y*1.74)), (255,255,255), -1)         # Boton "linea"
        cv2.line(frame, (int(bx_1*1.07),int(mid_y*1.66)), (int(bx_2*0.94),int(mid_y*1.724)), (0,0,0), 5)
        
        if left_index != None:
            
            if((left_index[0] >= bx_1 and left_index[0] <= bx_2) and (left_index[1] >= int(mid_y*.85) and left_index[1] <= (mid_y*0.94) and size <= 800)):
                size+=2
                print("Mas")
            
            if((left_index[0] >= bx_1 and left_index[0] <= bx_2) and (left_index[1] >= int(mid_y*1.05) and left_index[1] <= (mid_y*1.14) and size >= 10)):
                size-=2
                print("Menos")
            
            if((left_index[0] >= bx_1 and left_index[0] <= bx_2) and (left_index[1] >= int(mid_y*1.25) and left_index[1] <= (mid_y*1.34))):
                cu_shape = "rectangle"
                print("Rectangle")
                
            if((left_index[0] >= bx_1 and left_index[0] <= bx_2) and (left_index[1] >= int(mid_y*1.45) and left_index[1] <= (mid_y*1.54))):
                cu_shape = "circle"
                print("Circle")
                
            if((left_index[0] >= bx_1 and left_index[0] <= bx_2) and (left_index[1] >= int(mid_y*1.65) and left_index[1] <= (mid_y*1.74))):
                cu_shape = "line"
                print("Line")
            
            if((left_index[0] >= int(w*0.01) and left_index[0] <= int(w*0.05)) and (left_index[1] <= 100 and left_index[1] >= 20)):
                print("Blue")
                cu_color = blue
            
            if((left_index[0] >= int(w*0.06) and left_index[0] <= int(w*0.10)) and (left_index[1] <= 100 and left_index[1] >= 20)):
                print("Green")
                cu_color = green
                
            if((left_index[0] >= int(w*0.11) and left_index[0] <= int(w*0.15)) and (left_index[1] <= 100 and left_index[1] >= 20)):
                print("Red")
                cu_color = red
                
            if((left_index[0] >= int(w*0.16) and left_index[0] <= int(w*0.20)) and (left_index[1] <= 100 and left_index[1] >= 20)):
                print("Yellow")
                cu_color = yellow
            
            if((left_index[0] >= int(w*0.85) and left_index[0] <= int(w*0.89)) and (left_index[1] <= 100 and left_index[1] >= 20)):
                print("Pink")
                cu_color = pink
                
            if((left_index[0] >= int(w*0.80) and left_index[0] <= int(w*0.84)) and (left_index[1] <= 100 and left_index[1] >= 20)):
                print("Brown")
                cu_color = brown

            if((left_index[0] >= int(w*0.90) and left_index[0] <= int(w*0.94)) and (left_index[1] <= 100 and left_index[1] >= 20)):
                print("Aqua")
                cu_color = aqua
                
            if((left_index[0] >= int(w*0.95) and left_index[0] <= int(w*0.99)) and (left_index[1] <= 100 and left_index[1] >= 20)):
                print("Orange")
                cu_color = orange
                
            
            
            match cu_shape:
                case "line":
                    if last_point is not None:
                        length = np.linalg.norm(np.array(left_index) - np.array(last_point))
                        if length < max_length: cv2.line(lienzo, last_point, left_index , cu_color, size) 
                
                case "circle":
                    cv2.circle(lienzo, left_index, size, cu_color, -1)
                    
                case "rectangle":
                    cv2.rectangle(lienzo, (int(left_index[0])-size, int(left_index[1])-size), (int(left_index[0])+size, int(left_index[1])+size), cu_color, -1)
                
                
            last_point = left_index
        else: last_point = None
    
    if cu_mode == "figures":
        print("hi")        
    
    if(left_index != None and cooldown <= 0):
        if((left_index[0] >= int(w*0.425) and left_index[0] <= int(w*0.475)) and (left_index[1] >= 20 and left_index[1] <= 100) ):
            match cu_mode:
                case "paint": cu_mode = mode_names[1]
                case "figures": cu_mode = mode_names[0]
            cooldown = cooldown_frames
                
        if((left_index[0] >= int(w*0.525) and left_index[0] <= int(w*0.575)) and (left_index[1] >= 20 and left_index[1] <= 100) ):
            lienzo = np.zeros_like(frame)
    
    cooldown -= 1
        
    merge = cv2.add(frame, lienzo) # Combinar ambos para generar una sola imagen unificada.
        
    # cv2.imshow("Normal", frame)                        
    cv2.imshow("Dibujo", merge)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): break
    
    
camara.release()
cv2.destroyAllWindows
    