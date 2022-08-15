import math
import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


def remap(n, minn, maxn, minx, maxx):
    return (n - minn) / (maxn - minn) * (maxx - minx) + minx


def loadTexture(filename):
    texture = pg.image.load(filename)
    data = pg.image.tostring(texture, "RGBA", True)
    glEnable(GL_TEXTURE_2D)
    texid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texid)
    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, int(texture.get_width()), int(texture.get_height()),
                 0, GL_RGBA, GL_UNSIGNED_BYTE, data)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    return texid


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


vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1),
)

faces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)


def getTexCoord(basePoint, i):
    if i == 0:
        return basePoint
    if i == 1:
        return (basePoint[0] + 1/3, basePoint[1])
    if i == 2:
        return (basePoint[0] + 1/3, basePoint[1] + 1/2)
    if i == 3:
        return (basePoint[0], basePoint[1] + 1/2)


def drawDice():
    glBegin(GL_QUADS)
    i = 0
    for face in faces:
        j = 0
        basepoint = (remap(i % 3, 0, 3, 0, 1),
                     remap(math.floor(i/3), 0, 2, 0, 1))
        for vertex in face:
            x, y = getTexCoord(basepoint, j)
            glTexCoord2f(x, y)
            glVertex3fv(vertices[vertex])
            j += 1
        i = i+1
    glEnd()


def draw():
    global a, b
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # make a light source appear by the cube
    glLightfv(GL_LIGHT0, GL_POSITION, [1, 1, 1, 0])
    glPushMatrix()
    glRotatef(a*5, 0, 1, 0)
    glRotatef(math.sin(a/40)*30, 1, 0, 0)
    glRotatef(math.sin(a/40)*30, 0, 0, 1)
    loadTexture("dice.png")
    drawDice()
    glPopMatrix()
    a += 0.1


def getPoint(t, radius):
    angle = 2 * math.pi * t
    x = math.cos(angle) * radius
    y = math.sin(angle) * radius
    return x, y


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

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()

        draw()
        drawFPS()
        pg.display.flip()
        clock.tick(60)
        # pg.time.wait(10)


if __name__ == "__main__":
    main()
