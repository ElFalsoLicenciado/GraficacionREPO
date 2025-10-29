import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Establecer color de fondo
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1.0, 0.1, 50.0)  # Configuración de perspectiva
    glMatrixMode(GL_MODELVIEW)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpiar buffers
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -3)  # Mover la cámara hacia atrás

    # Dibujar un cuadrado
    glBegin(GL_QUADS)
    glColor3f(1.0,0.0,0.0)  # ROJO
    glVertex3f(2.0,2.0,0.0) # vertice 1
    glColor3f(0.0,1.0,0.0)  # VERDE
    glVertex3f(2.0,1.0,0.0) # vertice 2
    glColor3f(0.0,0.0,0.0)  # NEGRO
    glVertex3f(1.0,1.0,0.0) # vertice 3
    glColor3f(0.0,0.0,1.0)  # AZUL
    glVertex3f(1.0,2.0,0.0) # vertice 4
    glEnd()
    
    
    # Dibujar un triángulo
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)  # Rojo
    glVertex3f(-2.0, -2.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)  # Verde
    glVertex3f(-1.0, 0.0, 0.0)
    glColor3f(0.0, 0.0, 1.0)  # Azul
    glVertex3f(0.0, -2.0, 0.0)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0.0, 1.0)  # Rojo
    glVertex3f(2.0, 0.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)  # Verde
    glVertex3f(0.0, 0.0, 0.0)
    glColor3f(1.0, 0.0, 0.0)  # Azul
    glVertex3f(1.0, -1.0, 0.0)
    glEnd()

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