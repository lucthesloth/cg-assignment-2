import math
from time import sleep
import sdl2
from OpenGL.GL import *
from OpenGL.GLU import *


cores = ((1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 1, 1),
         (0, 0, 1), (1, 0, 1), (0.5, 1, 1), (1, 0, 0.5))

def drawCircle(radius,sides):
    glBegin(GL_POLYGON)
    for i in range(sides):
        angle = i * 2 * math.pi / sides
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        glVertex2f(x,y)
    glEnd()

def drawPyramid(radius,sides, height):
    vertices = []
    glBegin(GL_POLYGON)
    for i in range(sides):
        angle = i * 2 * math.pi / sides
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        vertices.append((x,y))
        glVertex3f(x,y,0)
    glEnd()
    for i in range(sides):
        glBegin(GL_TRIANGLES)        
        glColor3fv(cores[i%len(cores)])
        glVertex3d(vertices[i][0],vertices[i][1],0)
        glVertex3d(vertices[(i+1)%len(vertices)][0],vertices[(i+1)%len(vertices)][1],0)
        glVertex3d(0,0,radius*height)
        glEnd()


a = 0
b = 3
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def desenha():
    global a, b
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glRotatef(a, 0, 1, 1)
    drawPyramid(1, clamp(b, 3, 20), 1)
    glPopMatrix()
    a += 0.01


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, 2)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, 1)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK,
                         sdl2.SDL_GL_CONTEXT_PROFILE_CORE)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DOUBLEBUFFER, 1)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DEPTH_SIZE, 24)
sdl2.SDL_GL_SetSwapInterval(1)
window = sdl2.SDL_CreateWindow(b"Cubo", sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED,
                               WINDOW_WIDTH, WINDOW_HEIGHT, sdl2.SDL_WINDOW_OPENGL | sdl2.SDL_WINDOW_SHOWN)
if not window:
    sys.stderr.write("Error: Could not create window\n")
    exit(1)
glcontext = sdl2.SDL_GL_CreateContext(window)
glEnable(GL_MULTISAMPLE)
glEnable(GL_DEPTH_TEST)
glClearColor(0., 0., 0., 1.)
gluPerspective(45, 800.0/600.0, 0.1, 100.0)
glTranslatef(0.0, 0.0, -5)

running = True
event = sdl2.SDL_Event()
while running:
    while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
        if event.type == sdl2.SDL_QUIT:
            running = False
        if event.type == sdl2.events.SDL_KEYDOWN:
            print("SDL_KEYDOWN")
            if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                running = False
        if event.type == sdl2.events.SDL_MOUSEBUTTONUP:            
            b = 3 if b > 8 else b + 1
    desenha()
    sdl2.SDL_GL_SwapWindow(window)
