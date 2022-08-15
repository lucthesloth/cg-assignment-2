import math
import pygame as pg
from pygame.locals import *
from time import sleep
from OpenGL.GL import *
from OpenGL.GLU import *


cores = ((1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 1, 1),
         (0, 0, 1), (1, 0, 1), (0.5, 1, 1), (1, 0, 0.5))


def drawCircle(radius, sides):
    glBegin(GL_POLYGON)
    for i in range(sides):
        angle = i * 2 * math.pi / sides
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        glVertex2f(x, y)
    glEnd()


def drawPyramid(radius, sides, height):
    vertices = []
    glBegin(GL_POLYGON)
    for i in range(sides):
        angle = i * 2 * math.pi / sides
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        vertices.append((x, y))
        glVertex3f(x, y, 0)
    glEnd()
    for i in range(sides):
        glBegin(GL_TRIANGLES)
        glColor3fv(cores[i % len(cores)])
        glVertex3d(vertices[i][0], vertices[i][1], 0)
        glVertex3d(vertices[(i+1) % len(vertices)][0],
                   vertices[(i+1) % len(vertices)][1], 0)
        glVertex3d(0, 0, radius*height)
        normal = getPlaneNormal((vertices[i][0], vertices[i][1], 0),
                                (vertices[(i+1) % len(vertices)][0],
                                 vertices[(i+1) % len(vertices)][1], 0),
                                (0, 0, radius*height))
        glNormal3f(normal[0], normal[1], normal[2])
        glEnd()


def getPlaneNormal(a, b, c):
    u = (b[0]-a[0], b[1]-a[1], b[2]-a[2])
    v = (c[0]-a[0], c[1]-a[1], c[2]-a[2])
    n = (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
    return n


def drawPrism(height):
    vertices = []
    verticesTop = []
    for i in range(3):
        angle = i * 2 * math.pi / 3
        x = math.cos(angle) * height
        y = math.sin(angle) * height
        vertices.append((x, y, 0))
        verticesTop.append((x, y, height))

    for i in range(3):
        glBegin(GL_QUADS)
        glColor3fv(cores[i % len(cores)])
        glVertex3d(vertices[i][0], vertices[i][1], vertices[i][2])
        glColor3fv(cores[i+1 % len(cores)])
        glVertex3d(vertices[(i+1) % len(vertices)][0],
                   vertices[(i+1) % len(vertices)][1],
                   vertices[(i+1) % len(vertices)][2])
        glColor3fv(cores[i+2 % len(cores)])
        glVertex3d(verticesTop[(i+1) % len(verticesTop)][0],
                   verticesTop[(i+1) % len(verticesTop)][1],
                   verticesTop[(i+1) % len(verticesTop)][2])
        glColor3fv(cores[i+3 % len(cores)])
        glVertex3d(verticesTop[i][0], verticesTop[i][1],
                   verticesTop[i][2])
        normal = getPlaneNormal(vertices[i],
                                vertices[(i+1) % len(vertices)],
                                verticesTop[(i+1) % len(verticesTop)])
        glNormal3f(normal[0], normal[1], normal[2])
        glEnd()
    glBegin(GL_POLYGON)
    for i in range(3):
        glColor3fv(cores[i % len(cores)])
        glVertex3d(vertices[i][0], vertices[i][1], vertices[i][2])
    glEnd()
    glBegin(GL_POLYGON)
    for i in range(3):
        glColor3fv(cores[i % len(cores)])
        glVertex3d(verticesTop[i][0], verticesTop[i][1], verticesTop[i][2])
    glEnd()


def drawFPS():
    global clock
    font = pg.font.SysFont("monospace", 15)
    text = font.render(str(int(clock.get_fps())), True,
                       (255, 255, 0), (0, 66, 0, 255))
    textData = pg.image.tostring(text, "RGBA", True)
    glWindowPos2d(2, 2)
    glDrawPixels(text.get_width(), text.get_height(),
                 GL_RGBA, GL_UNSIGNED_BYTE, textData)


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


a = 0
b = 3


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def desenha():
    global a, b
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glRotatef(a*10, 0, 1, 1)
    drawPyramid(1, 4, 1)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 0, 4)
    glRotatef(a*15, 0, 0, 1)
    drawPrism(0.7)
    glPopMatrix()
    a += 0.01


# Globals
clock = pg.time.Clock()
a = 0
b = 3


def main():
    global b, clock
    pg.init()
    display = (900, 600)
    pg.display.set_mode(display, DOUBLEBUF | OPENGL)
    pg.display.set_caption("Pygame + OpenGL")
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_DEPTH_TEST)

    glLight(GL_LIGHT0, GL_POSITION,  (0, 3, 3, 2))
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

    glTranslatef(-2, 0, -3)
    glRotate(30, 0, 1, 0)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        desenha()
        drawFPS()

        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHTING)
        glDisable(GL_COLOR_MATERIAL)
        pg.display.flip()
        clock.tick(60)
        # pg.time.wait(10)


if __name__ == "__main__":
    main()
