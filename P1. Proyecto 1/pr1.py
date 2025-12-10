import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

camara = cv2.VideoCapture(0)

ret, cuadro = camara.read()
lienzo = np.zeros_like(cuadro)

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
cu_shape = 0                                        # Figura de la brocha


size = 10                                           # Tamaño de la brocha

while camara.isOpened():                            # Ciclo para examinar los frames
    
    ret, frame = camara.read()                      # Obtener el fotograma
    
    h, w, _ = frame.shape                           # Obtener la anchura y altura del frame
    
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
                
    cv2.imshow("Salida", frame)                        # Abrir una ventana mostrando el resultado
    
    if cv2.waitKey(1) & 0xFF == ord('q'): break
    
camara.release()
cv2.destroyAllWindows
    