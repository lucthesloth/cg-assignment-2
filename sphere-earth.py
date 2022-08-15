import math
import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


def remap(n, minn, maxn, minx, maxx):
    return (n - minn) / (maxn - minn) * (maxx - minx) + minx


cores = ((1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 1, 1),
         (0, 0, 1), (1, 0, 1), (0.5, 1, 1), (1, 0, 0.5))


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


def getXYZ(i, j, r, N):
    theta = remap(i, 0, N, -math.pi/2, math.pi/2)
    phy = remap(j, 0, N, 0, 2*math.pi)
    x = r * math.cos(theta)*math.cos(phy)
    y = r * math.sin(theta)
    z = r * math.cos(theta)*math.sin(phy)
    return x, y, z


def drawSolidSphere(radius, div):
    global b
    glColor3f(1, 1, 1)
    for i in range(0, div):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(0, div+1):
            x, y, z = getXYZ(i, j, radius, div)
            glTexCoord2f(remap(j, 0, div, 1, 0), remap(i, 0, div, 0, 1))
            glVertex3f(x, y, z)
            x, y, z = getXYZ(i+1, j, radius, div)
            glTexCoord2f(remap(j, 0, div, 1, 0), remap(i+1, 0, div, 0, 1))
            glVertex3f(x, y, z)
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


def desenha():
    global a, b
    r = 1.5
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glRotatef(a*5, 0, 1, 0)
    loadTexture("./2k_earth_daymap.jpg")
    drawSolidSphere(r, 20)
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

    glTranslatef(0.0, 0.0, -5)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()

        desenha()
        drawFPS()
        pg.display.flip()
        clock.tick(60)
        # pg.time.wait(10)


if __name__ == "__main__":
    main()
