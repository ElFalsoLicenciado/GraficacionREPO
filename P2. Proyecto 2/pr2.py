import math
import cv2
import glfw
import mediapipe as mp
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import pygame, time

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

egg_card_tex = None
cavendish_card_tex = None

current_frame = 0.0
rotation_angle = 0.0
movement_offset = 0.0
movement_speed = 0.005
movement_direction = 1

in_animation = False
mouth_open = False
falling_card_offset = 0.0

mouth_ref = 0.1

jimbo = None
multi = None

voice_cooldown = 5
cooldown_timer = 0.0

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
    global egg_card_tex, cavendish_card_tex
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glDisable(GL_CULL_FACE)
    glDepthFunc(GL_LESS)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

    egg_card_tex = load_texture("C:/Users/User/Documents/Semestres/5to/Graficacion/Repositorio/P2. Proyecto 2/Egg.png")
    cavendish_card_tex = load_texture("C:/Users/User/Documents/Semestres/5to/Graficacion/Repositorio/P2. Proyecto 2/Cavendish.png")


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
    global rotation_angle, movement_offset

    radian = math.radians(rotation_angle)

    cos_a = math.cos(radian)
    sin_a = math.sin(radian)

    cx = (p1[0] + p2[0]) / 2
    cz = (p1[2] + p2[2]) / 2

    dx1 = p1[0] - cx; dx2 = p2[0] - cx
    dz1 = p1[2] - cz; dz2 = p2[2] - cz

    p1 = (dx1 * cos_a - dz1 * sin_a + cx,p1[1]+movement_offset, dx1*sin_a + dz2*cos_a + cz)
    p2 = (dx2 * cos_a - dz2 * sin_a + cx,p2[1]+movement_offset, dx2*sin_a + dz2*cos_a + cz)


    glPushMatrix()

    # glTranslatef(0.0, 0.0, -0.6+0.6*scale)


    draw_textured_rectangle(
        p1, p2,
        color=(1, 1, 1),
        texture=egg_card_tex
    )

    glPopMatrix()

def draw_falling_card(p1,p2, scale=1.0):
    global rotation_angle, falling_card_offset, in_animation

    radian = math.radians(rotation_angle)

    cos_a = math.cos(radian)
    sin_a = math.sin(radian)

    cx = (p1[0] + p2[0]) / 2
    cz = (p1[2] + p2[2]) / 2

    dx1 = p1[0] - cx; dx2 = p2[0] - cx
    dz1 = p1[2] - cz; dz2 = p2[2] - cz

    p1 = (dx1 * cos_a - dz1 * sin_a + cx, p1[1] + falling_card_offset, dx1 * sin_a + dz2 * cos_a + cz)
    p2 = (dx2 * cos_a - dz2 * sin_a + cx, p2[1] + falling_card_offset, dx2 * sin_a + dz2 * cos_a + cz)

    glPushMatrix()

    draw_textured_rectangle(
        p1, p2,
        color=(1, 1, 1),
        texture=cavendish_card_tex
    )

    glPopMatrix()

    print(f"Carta cayendo")


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


def update_motion(scale=1.0, chin=None):
    global in_animation, mouth_open,rotation_angle,movement_offset, falling_card_offset, movement_direction

    base_amplitude = 0.05 * scale

    min_amp = 0.001
    max_amp = 0.15

    # clamp
    amplitude = max(min_amp, min(base_amplitude, max_amp))

    movement_offset += movement_speed * movement_direction

    rotation_angle += 5
    if rotation_angle >= 360:
        rotation_angle = 0  # Reiniciar el ángulo después de una vuelta completa

    if movement_offset > chin[1] + amplitude:
        movement_direction = -1
    elif movement_offset < chin[1] - amplitude:
        movement_direction = 1

    if in_animation:
        falling_card_offset -= 0.01
        if falling_card_offset < -2.5:
            in_animation = False
            mouth_open = False
            falling_card_offset = 0.0


def get_mouth_opening(lm):
    upper_lip = lm[13]
    lower_lip = lm[14]

    _, uy, _ = norm_landmark(upper_lip)
    _, ly, _ = norm_landmark(lower_lip)

    mouth_open = abs(ly - uy)
    return mouth_open



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
    global in_animation, mouth_open, falling_card_offset, jimbo, multi, cooldown_timer
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
    head_left = norm_landmark(lm[148])
    head_right = norm_landmark(lm[372])

    hx, hy, hz = norm_landmark(head_top)

    head_width = abs(head_right[0] - head_left[0])
    head_radius = head_width * 0.75

    cone_radius = head_radius * 1.05
    cone_height = head_radius * 1.6

    draw_cone(hx,hy, -0.5, cone_radius, cone_height, (0.992, 0.361, 0.341))
    draw_sphere(hx,hy+cone_height, -0.5, cone_radius * 0.25, (0.81,0.81,0.81))

    card_width = 0.075 * scale
    card_height = 0.15 * scale

    chin = norm_landmark(lm[152])
    left_side = norm_landmark(lm[148])
    right_side = norm_landmark(lm[372])

    hx = (left_side[0] + right_side[0]) / 2

    hy = chin[1] - (0.15 * scale) / 2 - 0.02 * scale

    hz = chin[2]

    draw_animated_card((hx, hy, hz), (hx + card_width, hy + card_height, hz), scale=scale)


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
    # 4. NARIZ
    # ============================================================

    nose_center = lm[4]
    nx, ny, nz = norm_landmark(nose_center)
    nz += 0.024 * scale

    draw_sphere(nx, ny, nz, scale * 0.060, (0.98, 0.243, 0.059))

    # ============================================================
    # 5. BOCA
    # ============================================================
    mouth_length = get_mouth_opening(lm)

    print(f"Mouth Length: {mouth_length} - Ref: {mouth_ref*scale}")
    print(f"Cooldown Timer: {cooldown_timer}")

    if mouth_length > mouth_ref*scale and cooldown_timer <= 0.0:
        jimbo.play()
        cooldown_timer = voice_cooldown

    if mouth_length > mouth_ref*scale and not mouth_open:
        multi.set_volume(0.25)
        multi.play()
        mouth_open = True
        in_animation = True
        falling_card_offset = 0.0

    if in_animation:
        draw_falling_card(
            (0.075, 0.9, 0),
            (-0.075, 1.5, 0),
            scale=scale
        )

    draw_contour(lm, CONTORNO_BOCA,3.5, color=(0.98, 0.243, 0.059), scale=scale)
    draw_polygon(lm, CONTORNO_BOCA, z_offset=0.024, color=(1,1,1), scale=scale)

    cooldown_timer -= 0.1

    # Restaurar matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


# ============================================================
# Función principal
# ============================================================
def main():
    global current_frame, jimbo, multi

    scale = 1.0; chin = None
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

    pygame.mixer.init()

    pygame.mixer.music.load(
        "C:/Users/User/Documents/Semestres/5to/Graficacion/Repositorio/P2. Proyecto 2/balatro.mp3")
    jimbo = pygame.mixer.Sound(
        "C:/Users/User/Documents/Semestres/5to/Graficacion/Repositorio/P2. Proyecto 2/jimbo.mp3")
    multi = pygame.mixer.Sound(
        "C:/Users/User/Documents/Semestres/5to/Graficacion/Repositorio/P2. Proyecto 2/multi.ogg")

    pygame.mixer.music.set_volume(0.15)
    pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=1000)


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
                    chin = norm_landmark(face_landmarks.landmark[152])
                    render_3d_mask_extended(face_landmarks, current_frame, scale)
            update_motion(scale, chin)


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
