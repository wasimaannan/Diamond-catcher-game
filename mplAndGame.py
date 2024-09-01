import sys
import random
import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

W_Width = 600
W_Height = 800


def MidpointLine(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    zone = findZone(dx, dy)
    a0, b0 = convertToZone0(x0, y0, zone)
    a1, b1 = convertToZone0(x1, y1, zone)
    dx = a1 - a0
    dy = b1 - b0
    d = 2 * dy - dx
    dE = 2 * dy
    dNE = 2 * (dy - dx)
    x, y = convertBackToZone(a0, b0, zone)
    draw_pixel(x, y)
    while a0 < a1:
        if d <= 0:
            d += dE
            a0 += 1
        else:
            d += dNE
            a0 += 1
            b0 += 1

        x, y = convertBackToZone(a0, b0, zone)
        draw_pixel(x, y)


def findZone(dx, dy):
    if abs(dx) >= abs(dy) and dx >= 0 and dy >= 0:
        return 0
    elif abs(dx) < abs(dy) and dx >= 0 and dy >= 0:
        return 1
    elif abs(dx) < abs(dy) and dx < 0 and dy >= 0:
        return 2
    elif abs(dx) >= abs(dy) and dx < 0 and dy >= 0:
        return 3
    elif abs(dx) >= abs(dy) and dx < 0 and dy < 0:
        return 4
    elif abs(dx) < abs(dy) and dx < 0 and dy < 0:
        return 5
    elif abs(dx) < abs(dy) and dx >= 0 and dy < 0:
        return 6
    elif abs(dx) >= abs(dy) and dx >= 0 and dy < 0:
        return 7


def convertToZone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y


def convertBackToZone(a, b, zone):
    if zone == 0:
        return a, b
    elif zone == 1:
        return b, a
    elif zone == 2:
        return -b, a
    elif zone == 3:
        return -a, b
    elif zone == 4:
        return -a, -b
    elif zone == 5:
        return -b, -a
    elif zone == 6:
        return b, -a
    elif zone == 7:
        return a, -b


def draw_pixel(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def draw_left_arrow():
    glColor3f(0.0, 1.0, 1.0)
    MidpointLine(15, 765, 60, 765)
    MidpointLine(15, 765, 35, 745)
    MidpointLine(15, 765, 35, 785)


def draw_pause():
    glColor3f(1.0, 1.0, 0.0)  # Yellow

    if pause:
        # play
        MidpointLine(287, 750, 320, 770)
        MidpointLine(320, 770, 287, 790)
        MidpointLine(287, 750, 287, 790)
    else:
        # pause
        MidpointLine(290, 745, 290, 790)
        MidpointLine(310, 745, 310, 790)


def draw_cross():
    glColor3f(1.0, 0.0, 0.0)
    MidpointLine(540, 750, 580, 790)
    MidpointLine(540, 790, 580, 750)


catcher_position_x = 0
catcher_width = 200


def draw_catcher():
    if game_over:
        glColor3f(1.0, 0.0, 0.0)
    else:
        glColor3f(1.0, 0.5, 1.0)

    MidpointLine(220 + catcher_position_x, 30, 380 + catcher_position_x, 30)
    MidpointLine(220 + catcher_position_x, 30, 200 + catcher_position_x, 70)
    MidpointLine(380 + catcher_position_x, 30, 400 + catcher_position_x, 70)
    MidpointLine(200 + catcher_position_x, 70, 400 + catcher_position_x, 70)


diamond_y = 700
diamond_x = random.randint(10, W_Width - 10)
fall_speed = 2
score = 0
pause = False
game_over = False
reset = False

diamond_color_r = 0.5 + 0.5 * random.random()
diamond_color_g = 0.5 + 0.5 * random.random()
diamond_color_b = 0.5 + 0.5 * random.random()


def draw_diamond():
    if not game_over:
        glColor3f(diamond_color_r, diamond_color_g, diamond_color_b)
        MidpointLine(diamond_x - 10, diamond_y, diamond_x, diamond_y + 10)
        MidpointLine(diamond_x, diamond_y + 10, diamond_x + 10, diamond_y)
        MidpointLine(diamond_x + 10, diamond_y, diamond_x, diamond_y - 10)
        MidpointLine(diamond_x, diamond_y - 10, diamond_x - 10, diamond_y)


def animate(value):
    global diamond_y, diamond_x, fall_speed, score, game_over

    if not pause and not game_over:
        diamond_y -= fall_speed
        diamond_min_x = diamond_x - 10
        diamond_max_x = diamond_x + 10
        diamond_min_y = diamond_y - 10
        diamond_max_y = diamond_y + 10

        catcher_min_x = catcher_position_x + 200
        catcher_max_x = catcher_position_x + 400
        catcher_min_y = 30
        catcher_max_y = 70

        # collision detection
        if (diamond_max_x >= catcher_min_x and diamond_min_x <= catcher_max_x and
                diamond_max_y >= catcher_min_y and diamond_min_y <= catcher_max_y):
            score += 1
            print(f"Score: {score}")
            reset_diamond()

        if diamond_y <= 0:
            game_over = True
            fall_speed = 0
            print("Game Over!")
            print(f"Your final Score: {score}")
            pause_game()

    glutPostRedisplay()
    glutTimerFunc(16, animate, 0)


def reset_diamond():
    global diamond_y, diamond_x, fall_speed, reset
    global diamond_color_r, diamond_color_g, diamond_color_b
    diamond_y = 700
    diamond_x = random.randint(10, W_Width - 10)
    if not reset:
        fall_speed += 1
    else:
        reset = False

    diamond_color_r = 0.5 + 0.5 * random.random()
    diamond_color_g = 0.5 + 0.5 * random.random()
    diamond_color_b = 0.5 + 0.5 * random.random()


def pause_game():
    global pause
    pause = True


def reset_game():
    global score, game_over, pause, catcher_position_x, reset
    score = 0
    game_over = False
    pause = False
    catcher_position_x = 0
    reset_diamond()
    reset = True
    print("Starting over!")


def specialKeyListener(key, x, y):
    global catcher_position_x
    step_size = 10
    if not pause:
        if key == GLUT_KEY_LEFT:
            if catcher_position_x > -W_Width // 2 + catcher_width // 2:
                catcher_position_x -= step_size
        elif key == GLUT_KEY_RIGHT:
            if catcher_position_x < W_Width // 2 - catcher_width // 2:
                catcher_position_x += step_size

        glutPostRedisplay()


def mouseListener(button, state, x, y):
    global pause
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = W_Height - y
        # pause
        if 290 <= x <= 310 and 745 <= y <= 790:
            pause = not pause
        # left arrow
        elif 15 <= x <= 35 and 745 <= y <= 785:
            reset_game()
        # cross
        elif 540 <= x <= 580 and 750 <= y <= 790:
            print(f"Your final Score is {score}. Goodbye!")
            glutLeaveMainLoop()
    glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT)

    draw_left_arrow()
    draw_pause()
    draw_cross()
    draw_catcher()
    draw_diamond()

    glutSwapBuffers()


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(0, W_Width, 0, W_Height)


# OpenGL setup
glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)  # Depth, Double buffer, RGB color

wind = glutCreateWindow(b"Catch the Diamonds!")
init()
glutTimerFunc(0, animate, 0)
glutDisplayFunc(display)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()
