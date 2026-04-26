
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()

display = (1000, 500)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

glEnable(GL_DEPTH_TEST)
glClearColor(0.2, 0.2, 0.2, 1.0)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(60, display[0]/display[1], 0.1, 100)

glMatrixMode(GL_MODELVIEW)

rot1 = 0
rot2 = 0

board = [[[0 for _ in range(7)] for _ in range(6)] for _ in range(6)]
current_player = 1

selected_col = 3
selected_depth = 3

def cube():
    glBegin(GL_QUADS)

    # ───────────────────────── FRONT FACE
    glNormal3f(0, 0, 1)
    glVertex3f(-0.5, -0.5,  0.5)
    glVertex3f( 0.5, -0.5,  0.5)
    glVertex3f( 0.5,  0.5,  0.5)
    glVertex3f(-0.5,  0.5,  0.5)

    # ───────────────────────── BACK FACE
    glNormal3f(0, 0, -1)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5,  0.5, -0.5)
    glVertex3f( 0.5,  0.5, -0.5)
    glVertex3f( 0.5, -0.5, -0.5)

    # ───────────────────────── LEFT FACE
    glNormal3f(-1, 0, 0)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5,  0.5)
    glVertex3f(-0.5,  0.5,  0.5)
    glVertex3f(-0.5,  0.5, -0.5)

    # ───────────────────────── RIGHT FACE
    glNormal3f(1, 0, 0)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5,  0.5, -0.5)
    glVertex3f(0.5,  0.5,  0.5)
    glVertex3f(0.5, -0.5,  0.5)

    # ───────────────────────── TOP FACE
    glNormal3f(0, 1, 0)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5,  0.5)
    glVertex3f( 0.5, 0.5,  0.5)
    glVertex3f( 0.5, 0.5, -0.5)

    # ───────────────────────── BOTTOM FACE
    glNormal3f(0, -1, 0)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f( 0.5, -0.5, -0.5)
    glVertex3f( 0.5, -0.5,  0.5)
    glVertex3f(-0.5, -0.5,  0.5)

    glEnd()

def sphere():
    quad = gluNewQuadric()
    gluSphere(quad, 0.3, 20, 20)
    
def drop_piece(col, depth, player):
    for row in range(5, -1, -1):
        if board[row][col][depth] == 0:
            board[row][col][depth] = player
            return True
    if not (0 <= col < 6 and 0 <= depth < 7):
        return False
    
def draw_board(): 
    for depth in range(7): 
        for col in range(6):
            glPushMatrix()
            
           
            glTranslatef(col - 3, 1.3, depth - 3)
            
            if col == selected_col and depth == selected_depth:
                glColor3f(0.2, 0.6, 1.0)  # bright selection
            else:
                glColor3f(0.7, 0.7, 0.7)
            
           
            glScalef(0.2, 3.5, 0.2)
            cube()

            glPopMatrix()
            
    for row in range(6):
        for col in range(6):
            for depth in range(7):

                glPushMatrix()

                glTranslatef(col - 3, row * 0.7, depth - 3)

                if board[row][col][depth] == 1:
                    glColor3f(1, 0, 0)
                    sphere()
                elif board[row][col][depth] == 2:
                    glColor3f(1, 1, 0)
                    sphere()

                glPopMatrix()
                
    glTranslatef(3, 0.5, 3)
    glScalef(6, 0.15, 6)
    #cube()
    
                
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                rot1 -= 5
            elif event.key == pygame.K_s:
                rot1 += 5
            elif event.key == pygame.K_a:
                rot2 -= 5
            elif event.key == pygame.K_d:
                rot2 += 5

            # COLUMN SELECTION (LEFT/RIGHT)
            elif event.key == pygame.K_LEFT:
                selected_col = max(0, selected_col - 1)
            elif event.key == pygame.K_RIGHT:
                selected_col = min(5, selected_col + 1)

            # DEPTH SELECTION (UP/DOWN)
            elif event.key == pygame.K_DOWN:
                selected_depth = min(6, selected_depth + 1)
            elif event.key == pygame.K_UP:
                selected_depth = max(0, selected_depth - 1)

           # PLACE PIECE
            elif event.key == pygame.K_RETURN:
                if drop_piece(selected_col, selected_depth, current_player):
                    current_player = 3 - current_player

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            col = int(x / (display[0] / 6))
            col = max(0, min(5, col))

            depth = selected_depth

            if drop_piece(col, depth, current_player):
                current_player = 3 - current_player
            
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(0, 0, 12, 0, 0, 0, 0, 1, 0)
    
    glRotatef(rot1, 1, 0, 0)
    glRotatef(rot2, 0, 1, 0)

    draw_board()

    pygame.display.flip()
    pygame.time.wait(16)

pygame.quit()