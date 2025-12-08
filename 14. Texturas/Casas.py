import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
from PIL import Image
import sys

tex_grass = None
tex_wall = None
tex_roof = None

z = 5
aug = 0.005

def load_texture(path):

    img = Image.open(path).convert("RGB")
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = img.tobytes()

    tex_id = glGenTextures(1)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    glBindTexture(GL_TEXTURE_2D, tex_id)

    # Filtrado
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Envoltura (tiling)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    # Subir la textura
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                 img.width, img.height, 0,
                 GL_RGB, GL_UNSIGNED_BYTE, img_data)

    # Crear mipmaps
    glGenerateMipmap(GL_TEXTURE_2D)

    glBindTexture(GL_TEXTURE_2D, 0)
    return tex_id


def init():
    global tex_grass, tex_wall, tex_roof
    """Configuración inicial de OpenGL"""
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)           # Activar prueba de profundidad

    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1, 6, 100.0)  # Campo de visión más amplio
    glMatrixMode(GL_MODELVIEW)
    
    tex_grass = load_texture("C:/Users/User/Documents/Semestres/5to/Graficacion/Repositorio/14. Texturas/grass.jpg")
    tex_wall = load_texture("C:/Users/User/Documents/Semestres/5to/Graficacion/Repositorio/14. Texturas/Wall.png")  # <<-- TU IMAGEN AQUÍ
    tex_roof = load_texture("C:/Users/User/Documents/Semestres/5to/Graficacion/Repositorio/14. Texturas/beans.jpg")

def draw_cube():
    """Dibuja el cubo (base de la casa)"""
    glBindTexture(GL_TEXTURE_2D, tex_wall)
    glBegin(GL_QUADS)
    glColor3f(0.8, 0.5, 0.2)  # Marrón para todas las caras

    # Frente
    glVertex3f(-1, 0, 1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 5, 1)
    glVertex3f(-1, 5, 1)

    # Atrás     X  Y   Z
    glVertex3f(-1, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 5, -1)
    glVertex3f(-1, 5, -1)

    # Izquierda
    glVertex3f(-1, 0, -1)
    glVertex3f(-1, 0, 1)
    glVertex3f(-1, 5, 1)
    glVertex3f(-1, 5, -1)

    # Derecha
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 5, 1)
    glVertex3f(1, 5, -1)
    

    # Arriba
    glColor3f(0.9, 0.6, 0.3)  # Color diferente para el techo
    glVertex3f(-1, 5, -1)
    glVertex3f(1, 5, -1)
    glVertex3f(1, 5, 1)
    glVertex3f(-1, 5, 1)

    # Abajo
    glColor3f(0.6, 0.4, 0.2)  # Suelo más oscuro
    glVertex3f(-1,0 , -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(-1, 0, 1)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)

    
def draw_roof():
    
    """Dibuja el techo (pirámide)"""
    glBindTexture(GL_TEXTURE_2D, tex_roof)
    glBegin(GL_TRIANGLES)
    glColor3f(0.9, 0.1, 0.1)  # Rojo brillante

    # Frente
    glVertex3f(-1, 5, 1)
    glVertex3f(1, 5, 1)
    glVertex3f(0, 9, 0)

    # Atrás     x  y   z 
    glVertex3f(-1, 5, -1)
    glVertex3f(1, 5, -1)
    glVertex3f(0, 9, 0)

    # Izquierda
    glVertex3f(-1, 5, -1)
    glVertex3f(-1, 5, 1)
    glVertex3f(0, 9, 0)

    # Derecha
    glVertex3f(1, 5, -1)
    glVertex3f(1, 5, 1)
    glVertex3f(0, 9, 0)
    glEnd()
    
    glBindTexture(GL_TEXTURE_2D, 0)


def draw_ground():

    """Dibuja un plano para representar el suelo o calle"""
    glBindTexture(GL_TEXTURE_2D, tex_grass)
    
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)  # Gris oscuro para la calle

    # Coordenadas del plano
    glVertex3f(-20, 0, 20)
    glVertex3f(20, 0, 20)
    glVertex3f(20, 0, -20)
    glVertex3f(-20, 0, -20)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)


def draw_house():
    """Dibuja una casa (base + techo)"""
    draw_cube()  # Base de la casa
    draw_roof()  # Techo

def draw_scene():
    """Dibuja toda la escena con 4 casas"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara
    # gluLookAt(9, 10, 15,  # Posición de la cámara
    #           0, 0, 0,    # Punto al que mira
    #           0, 1 ,0 )    # Vector hacia arriba

    # Vista: Cerca de una casa, perspectiva de un humano
    # gluLookAt(12, 2, 14,
    #       0, 6, 0,
    #       0, 1, 0)

    # Vista: Mirando al horizonte
    # gluLookAt(9, 10, 15,  # Posición de la cámara
    #           15, 10, -0,    # Punto al que mira
    #           0, 1 ,0 )    # Vector hacia arriba

    # Vista: Camara volteada
    # gluLookAt(9, 5, 15,  # Posición de la cámara
    #           0, 5, 0,    # Punto al que mira
    #           0, 0 ,1 )    # Vector hacia arriba
    
    # Vista    
    gluLookAt(2.5, 2, z,  # Posición de la cámara
              2.5, 2.5, -10,    # Punto al que mira
              0.15, 1 ,0 )    # Vector hacia arriba

    # Dibujar el suelo
    draw_ground()

    # Dibujar las casas en diferentes posiciones
    positions = [
        (-5, 0, -5),  # Casa 1
        (5, 0, -5),   # Casa 2
        (-5, 0, 5),   # Casa 3
        (5, 0, 5),
        (0, 0, 0),
        
    ]
    for pos in positions:
        glPushMatrix()
        glTranslatef(*pos)  # Mover la casa a la posición actual
        draw_house()        # Dibujar la casa
        glPopMatrix()

    glfw.swap_buffers(window)

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
    
    # Crear ventana de GLFW
    width, height = 800, 600
    window = glfw.create_window(width, height, "Escena con 4 casas", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Bucle principal
    while not glfw.window_should_close(window):
        global z
        global aug
        
        draw_scene()
        glfw.poll_events()
        
        z += aug
        
        if(z > 20):
            aug = aug*-1
        else: 
            if( z < -3):
                aug = aug*-1

    glfw.terminate()

if __name__ == "__main__":
    main()
