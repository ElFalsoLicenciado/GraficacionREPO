import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
from PIL import Image
import sys

tex_grass = None
tex_wall = None
tex_roof = None
tex_card = None


current_frame = 0.0
rotation_angle = 0.0
movement_offset = 0.0
movement_speed = 0.05
movement_direction = 1


# ------------------------------------------------------------
# Cargar textura con correcciones
# ------------------------------------------------------------
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
    

# ------------------------------------------------------------
# OpenGL Init
# ------------------------------------------------------------
def init():
    global tex_grass, tex_wall, tex_roof, tex_card
    glClearColor(0.5, 0.8, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


    tex_grass = load_texture("C:/Users/User/Documents/Semestres/5to/Graficacion/Repositorio/14. Texturas/grass.jpg")
    tex_wall = load_texture("C:/Users/User/Documents/Semestres/5to/Graficacion/Repositorio/14. Texturas/Wall.png")  # <<-- TU IMAGEN AQUÍ
    tex_roof = load_texture("C:/Users/User/Documents/Semestres/5to/Graficacion/Repositorio/14. Texturas/beans.jpg")
    tex_card = load_texture("C:/Users/User/Documents/Semestres/5to/Graficacion/Repositorio/P2. Proyecto 2/Egg.png")

# ------------------------------------------------------------
# Casa con textura de pared
# ------------------------------------------------------------
def draw_cube():
    glBindTexture(GL_TEXTURE_2D, tex_wall)

    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)

    # Frente
    glTexCoord2f(0, 0); glVertex3f(-1, 0, 1)
    glTexCoord2f(1, 0); glVertex3f( 1, 0, 1)
    glTexCoord2f(1, 1); glVertex3f( 1, 1, 1)
    glTexCoord2f(0, 1); glVertex3f(-1, 1, 1)

    # Atrás
    glTexCoord2f(0, 0); glVertex3f(-1, 0,-1)
    glTexCoord2f(1, 0); glVertex3f( 1, 0,-1)
    glTexCoord2f(1, 1); glVertex3f( 1, 1,-1)
    glTexCoord2f(0, 1); glVertex3f(-1, 1,-1)

    # Izquierda
    glTexCoord2f(0, 0); glVertex3f(-1, 0,-1)
    glTexCoord2f(1, 0); glVertex3f(-1, 0, 1)
    glTexCoord2f(1, 1); glVertex3f(-1, 1, 1)
    glTexCoord2f(0, 1); glVertex3f(-1, 1,-1)

    # Derecha
    glTexCoord2f(0, 0); glVertex3f( 1, 0,-1)
    glTexCoord2f(1, 0); glVertex3f( 1, 0, 1)
    glTexCoord2f(1, 1); glVertex3f( 1, 1, 1)
    glTexCoord2f(0, 1); glVertex3f( 1, 1,-1)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)


# ------------------------------------------------------------
# Techo con textura propia
# ------------------------------------------------------------
def draw_roof():
    glBindTexture(GL_TEXTURE_2D, tex_roof)

    glBegin(GL_TRIANGLES)
    glColor3f(1, 1, 1)

    glTexCoord2f(0, 0);    glVertex3f(-1, 1, 1)
    glTexCoord2f(1, 0);    glVertex3f( 1, 1, 1)
    glTexCoord2f(0.5, 1);  glVertex3f( 0, 2, 0)

    glTexCoord2f(0, 0);    glVertex3f(-1, 1,-1)
    glTexCoord2f(1, 0);    glVertex3f( 1, 1,-1)
    glTexCoord2f(0.5, 1);  glVertex3f( 0, 2, 0)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)


# ------------------------------------------------------------
# Piso con textura
# ------------------------------------------------------------
def draw_ground():
    glBindTexture(GL_TEXTURE_2D, tex_grass)

    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)

    scale = 3  # Cambia entre 1 y 5 según cómo quieras el mosaico

    glTexCoord2f(0, 0)
    glVertex3f(-10, 0, 10)

    glTexCoord2f(scale, 0)
    glVertex3f(10, 0, 10)

    glTexCoord2f(scale, scale)
    glVertex3f(10, 0, -10)

    glTexCoord2f(0, scale)
    glVertex3f(-10, 0, -10)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)

def draw_textured_rectangle(p1, p2, color=(1, 1, 1), texture=None):
    glBindTexture(GL_TEXTURE_2D, texture)


    glBegin(GL_QUADS)
    glColor3f(*color)

    glNormal3f(0.0, 0.0, -1.0)

    glTexCoord2f(0, 0); glVertex3f(-0.5, 0, 1)
    glTexCoord2f(1, 0); glVertex3f(0.5, 0, 1)
    glTexCoord2f(1, 1); glVertex3f(0.5, 1.5, 1)
    glTexCoord2f(0, 1); glVertex3f(-0.5, 1.5, 1)

    glEnd()


    glBindTexture(GL_TEXTURE_2D, 0)


def draw_animated_card():
    global rotation_angle

    glPushMatrix()

    glTranslatef(0.0, 0.0, -1.2)
    glRotatef(rotation_angle, 0, 1, 0)

    draw_textured_rectangle(
        ( 0.5,  1.0, 0.0),
        (-0.5, -1.5, 0.0),
        texture=tex_card
    )

    glPopMatrix()


def update_motion():
    global rotation_angle, movement_offset, movement_direction

    # Actualizar el ángulo de rotación
    rotation_angle += 0.1
    if rotation_angle >= 360:
        rotation_angle = 0  # Reiniciar el ángulo después de una vuelta completa

    # Actualizar el movimiento de vaivén
    movement_offset += movement_speed * movement_direction
    if movement_offset > 3.0:       # Limite derecho
        movement_direction = -1     # Cambiar dirección hacia la izquierda
    elif movement_offset < -3.0:    # Limite izquierdo
        movement_direction = 1      # Cambiar dirección hacia la derecha

# ------------------------------------------------------------
# Dibujo principal
# ------------------------------------------------------------
def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(4, 4, 8, 0, 1, 0, 0, 1, 0)

    update_motion()
    draw_ground()
    # draw_cube()
    # draw_roof()
    draw_animated_card()

    glfw.swap_buffers(window)


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():
    global window

    if not glfw.init():
        sys.exit()

    window = glfw.create_window(800, 600, "Casa con Textura de Pasto", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, 800, 600)

    init()

    while not glfw.window_should_close(window):
        draw_scene()
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()