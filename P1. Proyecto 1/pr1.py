import cv2
import numpy as np

camara = cv2.VideoCapture(0)

ret, cuadro = camara.read()
lienzo = np.zeros_like(cuadro)

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

size = 10

bx_1 = 200
bx_2 = 250
