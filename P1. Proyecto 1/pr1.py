import cv2 as cv
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

camara = cv.VideoCapture(0)

ret, frame = camara.read()
lienzo = np.zeros_like(frame)                       # Lienzo para colorear 

# Rango del color rojo en HSV
u_bajo = np.array([100, 50, 50])
u_alto = np.array([130, 255, 255])

# Declaracion de variables para los colores
blue = (255,0,0) 
green = (0,255,0)
red = (0,0,255)
yellow = (57,247,255)

pink = (251,81,255)
brown = (28,44,82)
aqua = (255,237,11)
orange = (72,143,240)

mode_names = ("paint", "figures")
colors = (blue, green, red, yellow, pink, brown, aqua, orange)
color_index = 0
shapes = ("line", "circle", "rectangle")
shape_index = 0
editor_mode = ("nothing","waiting","adding","move", "scale", "rotate")
editor_index = 0

cu_mode = mode_names[1]                             # Modo de paint o dibujo de primitivas
cu_color = colors[color_index]                      # Color seleccionado
cu_shape = shapes[shape_index]                      # Figura de la brocha
cu_editor_mode = editor_mode[editor_index]          # Configuracion al colocarl primitivas
figure_size = 10
size = 10                                           # Tamaño de la brocha                   

current_point = None
last_point = None
max_length = 50

cooldown = 0
mode_cooldown = 30
general_cooldown = 15

bx_1 = 100
bx_2 = 150
aux = ""


while camara.isOpened():                            # Ciclo para examinar los frames
    
    ret, frame = camara.read()                      # Obtener el fotograma
    
    h, w, = 1200, 1920
    
    mid_y = h // 2
    # Obtener la anchura y altura del frame
    
    if not ret: break
    
    frame = cv.flip(frame,1)                       # Girar el video
    
    # Cambiar de BRG a RGB para que charche
    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)  
    results = hands.process(frame_rgb)
    
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mascara = cv.inRange(hsv, u_bajo, u_alto)
    
    
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
                cv.circle(frame, left_index, 4, red, -1)     # Circulo rojo en izquierdo
                
            elif label == 'Right': 
                right_index = (x,y)
                cv.circle(frame, right_index, 4, blue, -1)   # Circulo azul en derecho
    

    cv.rectangle(frame, (int(w*0.425),20), (int(w*0.475),100), (255,255,255), -1)                       # Cambiar de modo
    cv.putText(frame, cu_mode , (int(w*0.430),70), cv.FONT_HERSHEY_SIMPLEX, 0.80, (0,0,0), 2)

    cv.rectangle(frame, (int(w*0.525),20), (int(w*0.575),100), (255,255,255), -1)                       # Limpiar lienzo
    cv.putText(frame, "Limpiar", (int(w*0.527),70), cv.FONT_HERSHEY_SIMPLEX, 0.80, (0,0,0), 2)
    
    
    if cu_mode == "paint":
        cv.rectangle(frame, (int(w*0.01),20), (int(w*0.05),100), blue, -1)                             # Azul
        cv.rectangle(frame, (int(w*0.06),20), (int(w*0.10),100), green, -1)                            # Verde
        cv.rectangle(frame, (int(w*0.11),20), (int(w*0.15),100), red, -1)                              # Rojo
        cv.rectangle(frame, (int(w*0.16),20), (int(w*0.20),100), yellow, -1)                           # Amarillo
        
        
        cv.rectangle(frame, (int(w*0.80),20), (int(w*0.84),100), brown, -1)                            # Cafe
        cv.rectangle(frame, (int(w*0.85),20), (int(w*0.89),100), pink, -1)                             # Rosa
        cv.rectangle(frame, (int(w*0.90),20), (int(w*0.94),100), aqua, -1)                             # Aqua
        cv.rectangle(frame, (int(w*0.95),20), (int(w*0.99),100), orange, -1)                           # Naranja
        

        cv.rectangle(frame, (bx_1,int(mid_y*.85)), (bx_2,int(mid_y*0.94)), (255,255,255), -1)          # Botón "+"
        cv.putText(frame, "+", (bx_1,int(mid_y*.93)), cv.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3)

        
        cv.rectangle(frame, (bx_1,int(mid_y*1.05)), (bx_2,int(mid_y*1.14)), (255,255,255), -1)         # Botón "-"
        cv.putText(frame, "-", (bx_1, int(mid_y*1.13)), cv.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3)
    
        
        cv.rectangle(frame, (bx_1,int(mid_y*1.25)), (bx_2,int(mid_y*1.34)), (255,255,255), -1)         # Boton "rectangulo"
        cv.rectangle(frame, (int(bx_1*1.081),int(mid_y*1.266)), (int(bx_2*0.948),int(mid_y*1.3269)), (0,0,0), -1)
    
        
        
        cv.rectangle(frame, (bx_1,int(mid_y*1.45)), (bx_2,int(mid_y*1.54)), (255,255,255), -1)         # Botón "circulo"
        cv.circle(frame, ((bx_2+bx_1)//2, int(mid_y*1.495)), int(h*0.018) , (0,0,0), -1)

        
        cv.rectangle(frame, (bx_1,int(mid_y*1.65)), (bx_2,int(mid_y*1.74)), (255,255,255), -1)         # Boton "linea"
        cv.line(frame, (int(bx_1*1.07),int(mid_y*1.66)), (int(bx_2*0.94),int(mid_y*1.724)), (0,0,0), 5)
        
        momentos = cv.moments(mascara)
        if momentos["m00"] > 0:  # hay píxeles del color buscado
            cx = int(momentos["m10"] / momentos["m00"])
            cy = int(momentos["m01"] / momentos["m00"])
            current_point = (cx, cy)    
        
        
        if current_point != None:
            
            if((current_point[0] >= bx_1 and current_point[0] <= bx_2) and (current_point[1] >= int(mid_y*.85) and current_point[1] <= (mid_y*0.94) and size <= 800)):
                size+=2
                print("Mas")
            
            if((current_point[0] >= bx_1 and current_point[0] <= bx_2) and (current_point[1] >= int(mid_y*1.05) and current_point[1] <= (mid_y*1.14) and size >= 10)):
                size-=2
                print("Menos")
            
            if((current_point[0] >= bx_1 and current_point[0] <= bx_2) and (current_point[1] >= int(mid_y*1.25) and current_point[1] <= (mid_y*1.34))):
                shape_index = 0
                print("Rectangle")
                
            if((current_point[0] >= bx_1 and current_point[0] <= bx_2) and (current_point[1] >= int(mid_y*1.45) and current_point[1] <= (mid_y*1.54))):
                shape_index = 1
                print("Circle")
                
            if((current_point[0] >= bx_1 and current_point[0] <= bx_2) and (current_point[1] >= int(mid_y*1.65) and current_point[1] <= (mid_y*1.74))):
                shape_index = 2
                print("Line")
            
            if((current_point[0] >= int(w*0.01) and current_point[0] <= int(w*0.05)) and (current_point[1] <= 100 and current_point[1] >= 20)):
                print("Blue")
                color_index = 0
            
            if((current_point[0] >= int(w*0.06) and current_point[0] <= int(w*0.10)) and (current_point[1] <= 100 and current_point[1] >= 20)):
                print("Green")
                color_index = 1
                
            if((current_point[0] >= int(w*0.11) and current_point[0] <= int(w*0.15)) and (current_point[1] <= 100 and current_point[1] >= 20)):
                print("Red")
                color_index = 2
                
            if((current_point[0] >= int(w*0.16) and current_point[0] <= int(w*0.20)) and (current_point[1] <= 100 and current_point[1] >= 20)):
                print("Yellow")
                color_index = 3
            
            if((current_point[0] >= int(w*0.85) and current_point[0] <= int(w*0.89)) and (current_point[1] <= 100 and current_point[1] >= 20)):
                print("Pink")
                color_index = 4
                
            if((current_point[0] >= int(w*0.80) and current_point[0] <= int(w*0.84)) and (current_point[1] <= 100 and current_point[1] >= 20)):
                print("Brown")
                color_index = 5

            if((current_point[0] >= int(w*0.90) and current_point[0] <= int(w*0.94)) and (current_point[1] <= 100 and current_point[1] >= 20)):
                print("Aqua")
                color_index = 6
                
            if((current_point[0] >= int(w*0.95) and current_point[0] <= int(w*0.99)) and (current_point[1] <= 100 and current_point[1] >= 20)):
                print("Orange")
                color_index = 7
            
            cu_color = colors[color_index]
            cu_shape = shapes[shape_index]    
            
            
            match cu_shape:
                case "line":
                    if last_point is not None:
                        length = np.linalg.norm(np.array(current_point) - np.array(last_point))
                        if length < max_length: cv.line(lienzo, last_point, current_point , cu_color, size) 
                
                case "circle":
                    cv.circle(lienzo, current_point, size, cu_color, -1)
                    
                case "rectangle":
                    cv.rectangle(lienzo, (int(current_point[0])-size, int(current_point[1])-size), (int(current_point[0])+size, int(current_point[1])+size), cu_color, -1)
                
                
            last_point = current_point
        else: last_point = None
    
    if cu_mode == "figures":
        cv.rectangle(frame, (bx_1,int(mid_y*.85)), (bx_2,int(mid_y*0.94)), cu_color, -1)          

        
        cv.rectangle(frame, (bx_1,int(mid_y*1.05)), (bx_2,int(mid_y*1.14)), (255,255,255), -1)         
        match cu_shape:
            case "circle":
                cv.circle(frame, ((bx_2+bx_1)//2, int(mid_y*1.095)), int(h*0.018) , (0,0,0), -1)
                
            case "rectangle":
                cv.rectangle(frame, (int(bx_1*1.081),int(mid_y*1.066)), (int(bx_2*0.948),int(mid_y*1.1269)), (0,0,0), -1)
            
            case "line":
                cv.line(frame, (int(bx_1*1.07),int(mid_y*1.06)), (int(bx_2*0.94),int(mid_y*1.124)), (0,0,0), 5)        
        
        cv.rectangle(frame, (bx_1,int(mid_y*1.25)), (bx_2,int(mid_y*1.34)), (255,255,255), -1)
        
        match cu_editor_mode:
            case "nothing":     aux = "N"
            case "adding":      aux = "A"
            case "waiting":     aux = "W"
            case "move":        aux = "M"
            case "scale":       aux = "S"
            case "rotate":      aux = "R"
        
        cv.putText(frame, aux, (bx_1, int(mid_y*1.3299)), cv.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3)            
        
        # print(cooldown)
        
        if left_index != None and (cooldown <= 0):
            if((left_index[0] >= bx_1 and left_index[0] <= bx_2) and (left_index[1] >= int(mid_y*.85) and left_index[1] <= (mid_y*0.94))):
                # print("COLOR")
                # print(color_index)
                if(color_index < 7): color_index = color_index + 1
                else:                color_index = 0     
                cu_color = colors[color_index]
                cooldown = general_cooldown        
                        
                
            
            if((left_index[0] >= bx_1 and left_index[0] <= bx_2) and (left_index[1] >= int(mid_y*1.05) and left_index[1] <= (mid_y*1.14)) and (cu_editor_mode == "nothing" or cu_editor_mode == "waiting")):
                # print("SHAPE")
                # print(shape_index)
                if(shape_index < 2): shape_index = shape_index + 1
                else:                shape_index = 0
                cu_shape = shapes[shape_index]
                cooldown = general_cooldown
                last_point = None
                current_point = None
        
        
        tecla = cv.waitKey(1) & 0xFF
        
        
        # Teclas para modo Figures:
        # A == "AGREGAR"
        # R == "ROTAR"
        # T == "MOVER"
        # S == "ESCALAR"
        # E == "TERMINAR"
        
        if tecla == ord('a'):       
            if editor_index == 0 or editor_index == 1:   
                editor_index = 2
                last_point = None
                current_point = None
            elif editor_index == 2: editor_index = 1
        elif tecla == ord('t'):     
            if editor_index == 1:   editor_index = 2
        elif tecla == ord('s'):     
            if editor_index == 1:   editor_index = 3
        elif tecla == ord('r'):     
            if editor_index == 1:   editor_index = 4
        elif tecla == ord('q'):     break

        
        cu_editor_mode = editor_mode[editor_index]
        
        
        if cu_editor_mode == "adding":
            if left_index != None: 
                match cu_shape:
                    case "line":
                        if last_point != None:
                            cv.line(frame, left_index, last_point, cu_color, 5)
                            
                        if last_point == None and tecla == ord('e'):
                            last_point = left_index
                            
                        elif last_point != None and tecla == ord('e'):
                            current_point = left_index
                            cv.line(frame, current_point, last_point, cu_color, 5)
                            editor_index = 1
                        
                    case "circle":
                        cv.circle(frame, left_index, figure_size, cu_color, -1)
                        if tecla == ord('e'):
                            last_point = left_index
                            cv.circle(frame, last_point, figure_size, cu_color, -1)
                            editor_index = 1
                    
                    case "rectangle":
                        if last_point != None:
                            cv.rectangle(frame, left_index, last_point, cu_color, -1)
                        
                        if last_point == None and tecla == ord('e'):
                            last_point = left_index
                        
                        if last_point != None and tecla == ord('e'):
                            current_point = left_index
                            cv.rectangle(frame, current_point, last_point, cu_color, -1)
                            editor_index = 1
            
            if tecla == ord('e'):
                editor_index = 1     
        
        if cu_editor_mode == "waiting":
            
            if tecla == ord('e'):
                match cu_shape:
                    case "line":
                        cv.line(lienzo, current_point, last_point, cu_color, 5 )
                        last_point = None
                        current_point = None
                        editor_index = 0
                    case "circle":
                        cv.circle(lienzo, last_point, figure_size, cu_color, -1)
                        last_point = None
                        current_point = None
                        editor_index = 0
                    
                    case "rectangle":
                        cv.rectangle(lienzo, current_point, last_point, cu_color, -1)
                        last_point = None
                        current_point = None
                        editor_index = 0
            
            else:
                match cu_shape:
                    case "line":
                        cv.line(frame, current_point, last_point, cu_color, 5 )
                    case "circle":
                        cv.circle(frame, last_point, figure_size, cu_color, -1)
                    case "rectangle":
                        cv.rectangle(frame, current_point, last_point, cu_color, -1)
                                        

        
        cu_editor_mode = editor_mode[editor_index]
        
    
    if(left_index != None and cooldown <= 0):
        if((left_index[0] >= int(w*0.425) and left_index[0] <= int(w*0.475)) and (left_index[1] >= 20 and left_index[1] <= 100) ):
            match cu_mode:
                case "paint": 
                    cu_mode = mode_names[1]
                    last_point = None
                    current_point = None
                case "figures": 
                    cu_mode = mode_names[0]
                    last_point = None
                    current_point = None

            cooldown = mode_cooldown
                
        if((left_index[0] >= int(w*0.525) and left_index[0] <= int(w*0.575)) and (left_index[1] >= 20 and left_index[1] <= 100) ):
            lienzo = np.zeros_like(frame)
    
    cooldown -= 1
        
    merge = cv.add(frame, lienzo) # Combinar ambos para generar una sola imagen unificada.
        
    # cv.imshow("Normal", frame)                        
    cv.imshow("Dibujo", merge)
    
    if cv.waitKey(1) & 0xFF == ord('q'): break
    
    
camara.release()
cv.destroyAllWindows
    