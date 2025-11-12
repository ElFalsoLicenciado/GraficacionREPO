import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

orange = (0.839, 0.478, 0.039)
red = (0.839, 0.039, 0.039)
brown = (0.58, 0.384, 0.016)

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Establecer color de fondo
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(120, 1, 0.1, 50.0)  # Configuración de perspectiva
    glMatrixMode(GL_MODELVIEW)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpiar buffers
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -3)  # Mover la cámara hacia atrás

    # Dibujar un cuadrado
    glBegin(GL_QUADS)
    glColor3f(0.839,0.478,0.039)  # ROJO
    glVertex2f(0.0,0.0) # vertice 1
    glColor3f(0.839,0.478,0.039)  # VERDE
    glVertex2f(2.0,0.0) # vertice 2
    glColor3f(0.839,0.478,0.039)  # NEGRO
    glVertex2f(2.0,2.0) # vertice 3
    glColor3f(0.839,0.478,0.039)  # AZUL
    glVertex2f(0.0,2.0) # vertice 4
    
    glColor3f(0.58, 0.384, 0.016)
    glVertex2f(0.75,0)
    glColor3f(0.58, 0.384, 0.016)
    glVertex2f(1.25,0)
    glColor3f(0.58, 0.384, 0.016)
    glVertex2f(1.25,0.75)
    glColor3f(0.58, 0.384, 0.016)
    glVertex2f(0.75,0.75)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(0.839, 0.039, 0.039)
    glVertex2f(0,2.0)
    glColor3f(0.839, 0.039, 0.039)
    glVertex2f(2.0,2.0)
    glColor3f(0.839, 0.039, 0.039)
    glVertex2f(1,3)
    glEnd()
    
    glBegin(GL_x)
    
    

    glutSwapBuffers()  # Intercambiar buffers

def main():
    # Inicializar GLUT
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Triangulo con GLUT y Python")


    init()
    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()