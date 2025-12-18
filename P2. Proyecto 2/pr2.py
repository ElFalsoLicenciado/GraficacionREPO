import cv2
import glfw
import mediapipe as mp
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

# ============================================================
# Configuración
# ============================================================
# WINDOW_WIDTH
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
WINDOW_TITLE = "El Balatreador"

# Conexiones para dibujar el contorno facial
CONTORNO_CARA = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
                 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
                 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]

CONTORNO_BOCA = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291, 324,318, 402, 317, 14, 87, 178, 88, 95, 78]

CONTORNO_OJO_IZQ = [124, 225, 224, 223, 222, 221, 189, 244, 233, 232, 231, 230, 229, 228, 31, 35]
CONTORNO_OJO_DER = [353, 445, 444, 443, 442, 441, 417, 464, 453, 452, 451, 450, 449, 448, 261, 265]


EYE_DISTANCE_REF = 0.16
BASE_SCALE = 0.8
EXP = 1.8

card_tex = None

current_frame = 0.0
rotation_angle = 0.0
movement_offset = 0.0
movement_speed = 0.05
movement_direction = 1


def init_glfw():
    if not glfw.init():
        raise Exception("No se pudo inicializar GLFW")

    # No especificar version de OpenGL - usar la mejor disponible compatible
    # con fixed-function pipeline (glBegin/glEnd, GL_LIGHTING, etc.)

    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, None, None)

    if not window:
        glfw.terminate()
        raise Exception("No se pudo crear la ventana GLFW")

    glfw.make_context_current(window)
    glfw.swap_interval(1)

    return window


def setup_opengl():
    global card_tex
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glDisable(GL_CULL_FACE)
    glDepthFunc(GL_LESS)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

    card_tex = load_texture("C:/Users/User/Documents/Semestres/5to/Graficacion/Repositorio/P2. Proyecto 2/Egg.png")


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

def create_video_texture():
    video_tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, video_tex)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    return video_tex


def setup_lights():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)  # Luz adicional
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    # Luz principal frontal
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 2, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1))

    # Luz de relleno lateral
    glLightfv(GL_LIGHT1, GL_POSITION, (1, 1, 1, 0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.5, 0.5, 0.5, 1))


# ============================================================
# Funciones de dibujo
# ============================================================
def draw_sphere(x, y, z, radius, color=(1, 1, 1)):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(*color)
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, 16, 16)
    gluDeleteQuadric(quad)
    glPopMatrix()


def draw_line(p1, p2, color=(1, 1, 1), width=2.0):
    """Dibuja una línea entre dos puntos 3D"""
    glDisable(GL_LIGHTING)
    glLineWidth(width)
    glColor3f(*color)
    glBegin(GL_LINES)
    glVertex3f(*p1)
    glVertex3f(*p2)
    glEnd()
    glEnable(GL_LIGHTING)


def draw_textured_rectangle(p1,p2,color=(1, 1, 1), texture=None):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)


    glBegin(GL_QUADS)
    glColor3f(*color)

    glNormal3f(0.0, 0.0, -1.0)


    # point1 = (-0.05, -0.65, 1)
    # point2 = (0.05, -0.65, 1)
    # point3 = (0.05, -0.5, 1)
    # point4 = (-0.05, -0.5, 1)

    point1 = (p1[0], p1[1], 1)
    point2 = (p2[0], p1[1], 1)
    point3 = (p2[0], p2[1], 1)
    point4 = (p1[0], p2[1], 1)


    glTexCoord2f(0, 0); glVertex3f(*point1)
    glTexCoord2f(1, 0); glVertex3f(*point2)
    glTexCoord2f(1, 1); glVertex3f(*point3)
    glTexCoord2f(0, 1); glVertex3f(*point4)
    glEnd()


    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)


def draw_polygon(landmarks, indices,z_offset, color=(1, 1, 1), scale=1.0):
    glDisable(GL_LIGHTING)
    glLineWidth(1.0)
    glColor3f(*color)
    glBegin(GL_POLYGON)
    for idx in indices:
        p = norm_landmark(landmarks[idx])
        p = (p[0], p[1], p[2] - z_offset * scale)
        glVertex3f(*p)
    glEnd()
    glEnable(GL_LIGHTING)


def draw_cone(x, y, z, base_radius, height, color=(1, 0, 0)):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(0, 0, 0, 1)
    glRotatef(-90, 1, 0, 0)
    glColor3f(*color)
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluCylinder(quad, base_radius, 0, height, 16, 16)
    gluDeleteQuadric(quad)
    glPopMatrix()


def draw_animated_card(p1,p2, scale=1.0):
    global rotation_angle

    glPushMatrix()

    glTranslatef(0.0, 0.0, -1.2+1.2*scale)
    glRotatef(rotation_angle, 0,1,0)

    draw_textured_rectangle(
        p1, p2,
        color=(1, 1, 1),
        texture=card_tex
    )

    glPopMatrix()


def norm_landmark(p, scale=2.0):
    return (p.x - 0.5) * scale, -(p.y - 0.5) * scale, p.z * scale


def get_eye_distance(lm):
    left_eye = lm[386]
    right_eye = lm[159]
    lx, ly, lz = norm_landmark(left_eye)
    rx, ry, rz = norm_landmark(right_eye)
    return abs(lx - rx)


def calculate_scale(eye_distance):
    scale = BASE_SCALE * (eye_distance / EYE_DISTANCE_REF) ** EXP

    return max(0.3, min(scale, 3.5))


def update_motion():
    global rotation_angle, movement_offset, movement_direction

    # Actualizar el ángulo de rotación
    rotation_angle += 1
    if rotation_angle >= 360:
        rotation_angle = 0  # Reiniciar el ángulo después de una vuelta completa

    # Actualizar el movimiento de vaivén
    movement_offset += movement_speed * movement_direction
    if movement_offset > 3.0:       # Limite derecho
        movement_direction = -1     # Cambiar dirección hacia la izquierda
    elif movement_offset < -3.0:    # Limite izquierdo
        movement_direction = 1      # Cambiar dirección hacia la derecha

    print(f"rotation_angle: {rotation_angle}, movement_offset: {movement_offset}")


# ============================================================
# Renderizado
# ============================================================
def render_video_background(frame_rgb, video_tex):
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1, 0, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glBindTexture(GL_TEXTURE_2D, video_tex)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                 frame_rgb.shape[1], frame_rgb.shape[0],
                 0, GL_RGB, GL_UNSIGNED_BYTE, frame_rgb)

    glColor3f(1.0, 1.0, 1.0)

    glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1); glVertex3f(0, 0,-1)
    glTexCoord2f(1, 1); glVertex3f(1, 0,-1)
    glTexCoord2f(1, 0); glVertex3f(1, 1,-1)
    glTexCoord2f(0, 0); glVertex3f(0, 1,-1)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_contour(landmarks, indices, width ,color=(0.3, 0.8, 0.4), scale=1.0):
    glDisable(GL_LIGHTING)
    glLineWidth(width * scale)
    glColor3f(*color)

    glBegin(GL_LINE_STRIP)
    for idx in indices:
        p = norm_landmark(landmarks[idx])
        glVertex3f(*p)
    # Cerrar el contorno
    p = norm_landmark(landmarks[indices[0]])
    glVertex3f(*p)
    glEnd()

    glEnable(GL_LIGHTING)


def render_3d_mask_extended(face_landmarks, animation_time, scale=1.0):
    """Renderiza la máscara 3D extendida"""
    glEnable(GL_DEPTH_TEST)
    glClear(GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluPerspective(45, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 100)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    gluLookAt(0, 0, 2,
              0, 0, 0,
              0, 1, 0)

    setup_lights()

    lm = face_landmarks.landmark

    head_top = lm[10]
    hx, hy, hz = norm_landmark(head_top)

    cone_height = 0.3 * scale

    draw_cone(hx,hy, -0.5, 0.10*scale, cone_height, color=(0.992, 0.361, 0.341))
    draw_sphere(hx,hy+cone_height, -0.5, scale * 0.030, (0.81,0.81,0.81))


    chin = lm[152]
    hx, hy, hz = norm_landmark(chin)

    draw_animated_card((hx, hy, hz), (hx+0.075, hy+0.15*scale, hz), scale=scale)

    # ============================================================
    # 1. CONTORNO CARA
    # ============================================================
    draw_contour(lm, CONTORNO_CARA,1.5, color=(1.0, 1.0, 1.0), scale=scale)
    draw_polygon(lm, CONTORNO_CARA, z_offset=0.1, color=(1, 1, 1), scale=scale)

    # ============================================================
    # 2. OJOS
    # ============================================================
    left_eye = lm[374]
    right_eye = lm[145]
    lx, ly, lz = norm_landmark(left_eye)
    rx, ry, rz = norm_landmark(right_eye)

    # Globos oculares (blancos)
    glColor3f(1.0, 1.0, 1.0)
    draw_sphere(lx, ly, lz, scale * 0.038, (1, 1, 1))
    draw_sphere(rx, ry, rz, scale * 0.038, (1, 1, 1))

    # Pupilas (azul oscuro)
    draw_sphere(lx, ly, lz + 0.024*scale, scale * 0.024, (0.1, 0.1, 0.4))
    draw_sphere(rx, ry, rz + 0.024*scale, scale * 0.024, (0.1, 0.1, 0.4))

    draw_polygon(lm, CONTORNO_OJO_IZQ, z_offset=-0.002, color=(0.839, 0.561, 0.157), scale=scale)
    draw_polygon(lm, CONTORNO_OJO_DER, z_offset=-0.002, color=(0.839, 0.561, 0.157), scale=scale)


    # ============================================================
    # 3. CEJAS
    # ============================================================


    # ============================================================
    # 4. NARIZ
    # ============================================================

    nose_center = lm[4]
    nx, ny, nz = norm_landmark(nose_center)
    nz += 0.024 * scale

    draw_sphere(nx, ny, nz, scale * 0.060, (0.98, 0.243, 0.059))

    # ============================================================
    # 5. BOCA
    # ============================================================

    draw_contour(lm, CONTORNO_BOCA,3.5, color=(0.98, 0.243, 0.059), scale=scale)
    draw_polygon(lm, CONTORNO_BOCA, z_offset=0.024, color=(1,1,1), scale=scale)

    # ============================================================
    # 6. CACHETES
    # ============================================================


    # ============================================================
    # 7. FRENTE Y BARBA
    # ============================================================


    # Restaurar matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


# ============================================================
# Función principal
# ============================================================
def main():
    global current_frame
    try:
        window = init_glfw()
    except Exception as e:
        print(f" Error al inicializar GLFW: {e}")
        return

    setup_opengl()
    video_tex = create_video_texture()

    mp_face = mp.solutions.face_mesh
    face_mesh = mp_face.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5,
                                 min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print(" No se pudo abrir la camara")
        glfw.terminate()
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)
    print("Camara inicializada")

    frame_count = 0
    fps_timer = glfw.get_time()

    try:
        while not glfw.window_should_close(window):
            ret, frame = cap.read()
            if not ret:
                break

            current_frame = glfw.get_time()

            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = face_mesh.process(frame_rgb)

            glfw.poll_events()

            if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
                break

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            render_video_background(frame_rgb, video_tex)
            glClear(GL_DEPTH_BUFFER_BIT)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    eye_distance = get_eye_distance(face_landmarks.landmark)
                    scale = calculate_scale(eye_distance)
                    render_3d_mask_extended(face_landmarks, current_frame, scale)
            update_motion()

            glfw.swap_buffers(window)

            frame_count += 1
            current_time = glfw.get_time()
            if current_time - fps_timer >= 1.0:
                fps = frame_count / (current_time - fps_timer)
                glfw.set_window_title(window, f"{WINDOW_TITLE} - FPS: {fps:.1f}")
                frame_count = 0
                fps_timer = current_time

    except Exception as e:
        print(f" Error en el loop principal: {e}")
        import traceback
        traceback.print_exc()

    finally:
        print("\nCerrando aplicación...")
        cap.release()
        face_mesh.close()
        glfw.terminate()


if __name__ == "__main__":
    main()
