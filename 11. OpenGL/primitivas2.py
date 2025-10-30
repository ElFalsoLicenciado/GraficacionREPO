import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

# Variables globales
window = None
angle = 0  # Declaramos angle en el nivel superior

def init():
    # Configuración inicial de OpenGL
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Color de fondo
    glEnable(GL_DEPTH_TEST)  # Activar prueba de profundidad para 3D

    # Configuración de proyección
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0, 0.1, 50.0)

    # Cambiar a la matriz de modelo para los objetos
    glMatrixMode(GL_MODELVIEW)

def draw_cube():
    global angle
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpiar pantalla y buffer de profundidad

    # Configuración de la vista del cubo
    glLoadIdentity()
    glTranslatef(-3.0, 0.0, -15)  # Alejar el cubo para que sea visible
    glRotatef(angle, 0, 1,0)   # Rotar el cubo en todos los ejes
    
    vertice = (1, 1, 1)
    vertice2 = (-1, 1, 1)

    glBegin(GL_TRIANGLES)
    glColor3f(1,1,1) # Base
    glVertex3f(2.0,0.0,0.0)
    glVertex3f(4.0,0.0,0.0)
    glVertex3f(3.0,0.0,1.5)    
    
    glColor3f(1,0,0) # Triangulo 1: ROJO
    glVertex3f(2.0,0.0,0.0)
    glVertex3f(4.0,0.0,0.0)
    glVertex3f(3.0,2.0,1)

    glColor3f(0,1,0) # Triangulo 2: VERDE
    glVertex3f(4.0,0.0,0.0)
    glVertex3f(3.0,0.0,1.5)
    glVertex3f(3.0,2.0,1)

    glColor3f(0,0,1) # Triangulo 3: AZUL
    glVertex3f(2.0,0.0,0.0)
    glVertex3f(3.0,0.0,1.5)
    glVertex3f(3.0,2.0,1)

    glEnd()
    glFlush()

    glfw.swap_buffers(window)  # Intercambiar buffers para animación suave
    angle += 0.05  # Incrementar el ángulo para rotación

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()

    # Crear ventana de GLFW
    width, height = 500, 500
    window = glfw.create_window(width, height, "Cubo 3D Rotando con GLFW", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    # Configurar el contexto de OpenGL en la ventana
    glfw.make_context_current(window)

    # Configuración de viewport y OpenGL
    glViewport(0, 0, width, height)
    init()

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_cube()
        glfw.poll_events()

    glfw.terminate()  # Cerrar GLFW al salir

if __name__ == "__main__":
    main()
