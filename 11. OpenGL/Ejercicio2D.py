import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_lines():
    #Para funcionar son 2 puntos, el punto de inicio y el punto final.
    """GL_LINES - Dibuja líneas separadas (pares de vértices)"""
    glLineWidth(10.0)
    glBegin(GL_LINES)
    # Primera línea
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-0.4, 0.3)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(-0.1, 0.0)
    # Segunda línea
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(0.1, 0.3)
    glColor3f(1.0, 1.0, 0.0)
    glVertex2f(0.4, 0.0)
    glEnd()

def draw_line_strip():
    #Conjunto de puntos que forman una sola linea
    """GL_LINE_STRIP - Dibuja una línea continua conectada"""
    glLineWidth(10.0)
    glBegin(GL_LINE_STRIP)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-0.4, 0.3)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(-0.2, 0.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(0.0, 0.3)
    glColor3f(1.0, 1.0, 0.0)
    glVertex2f(0.2, 0.0)
    glColor3f(1.0, 0.0, 1.0)
    glVertex2f(0.4, 0.3)
    glEnd()

def draw_line_loop():
    #Si son 3 puntos, se rellena la parte que falta siendo usualmente, el primer punto y el ultimo.
    """GL_LINE_LOOP - Dibuja una línea cerrada"""
    glLineWidth(3.0)
    glBegin(GL_LINE_LOOP)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-0.3, 0.3)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(0.3, 0.3)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(0.3, -0.3)
    glColor3f(1.0, 1.0, 0.0)
    glVertex2f(-0.3, -0.3)
    glEnd()

def draw_triangles():
    #Triangulo de toda la vida
    """GL_TRIANGLES - Dibuja triángulos separados"""
    glBegin(GL_TRIANGLES)
    # Primer triángulo
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-0.4, 0.3)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(-0.2, -0.2)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(-0.0, 0.3)
    # Segundo triángulo
    glColor3f(1.0, 1.0, 0.0)
    glVertex2f(0.1, 0.3)
    glColor3f(1.0, 0.0, 1.0)
    glVertex2f(0.3, -0.2)
    glColor3f(0.0, 1.0, 1.0)
    glVertex2f(0.5, 0.3)
    glEnd()

def draw_triangle_strip():
    """GL_TRIANGLE_STRIP - Dibuja una tira de triángulos conectados"""
    glBegin(GL_TRIANGLE_STRIP)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-0.4, 0.3)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(-0.3, -0.2)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(-0.1, 0.3)
    glColor3f(1.0, 1.0, 0.0)
    glVertex2f(0.0, -0.2)
    glColor3f(1.0, 0.0, 1.0)
    glVertex2f(0.2, 0.3)
    glColor3f(0.0, 1.0, 1.0)
    glVertex2f(0.3, -0.2)
    glEnd()

def draw_quads():
    """GL_QUADS - Dibuja cuadriláteros separados"""
    glBegin(GL_QUADS)
    # Primer cuadrilátero
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-0.5, 0.3)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(-0.2, 0.3)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(-0.2, -0.1)
    glColor3f(1.0, 1.0, 0.0)
    glVertex2f(-0.5, -0.1)
    # Segundo cuadrilátero
    glColor3f(1.0, 0.0, 1.0)
    glVertex2f(0.0, 0.3)
    glColor3f(0.0, 1.0, 1.0)
    glVertex2f(0.3, 0.3)
    glColor3f(1.0, 1.0, 0.0)
    glVertex2f(0.3, -0.1)
    glColor3f(1.0, 0.5, 0.0)
    glVertex2f(0.0, -0.1)
    glEnd()


def draw_all_primitives_grid():
    """Dibuja todas las primitivas en una cuadrícula 3x4"""
    
    # Configurar viewport y proyección para cuadrícula
    width, height = glfw.get_window_size(glfw.get_current_context())
    
    arreglo = [
        
    ]
        
    for idx, (name, draw_func) in enumerate(arreglo):
        
        # Configurar viewport para esta celda
        
        glViewport(x, y, cell_width, cell_height)
        
        # Configurar proyección
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Dibujar la primitiva
        draw_func()
        
        # Dibujar el nombre (en la parte inferior)
        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2f(-0.8, -0.9)
        # Nota: glutBitmapCharacter no está disponible sin GLUT

def main():
    # Inicializa GLFW
    if not glfw.init():
        return

    # Crear la ventana más grande para mostrar todas las primitivas
    window = glfw.create_window(1200, 900, "Todas las Primitivas de OpenGL", None, None)
    if not window:
        glfw.terminate()
        return

    # Hacer el contexto de OpenGL actual para la ventana
    glfw.make_context_current(window)

    # Configurar color de fondo
    glClearColor(0.5, 0.5, 0.5, 1.0)

    # Bucle principal
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        draw_all_primitives_grid()

        glfw.swap_buffers(window)
        glfw.poll_events()

    # Finalizar GLFW
    glfw.terminate()

if __name__ == "__main__":
    main()