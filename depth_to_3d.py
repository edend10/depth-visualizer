# Adapted from http://openglsamples.sourceforge.net/cube_py.html

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import os
import threading
from PIL import Image
import numpy as np
import sys
import random
import imageio
 
ESCAPE = '\033'
 
window = 0
 
#rotation
X_AXIS = 0.0
Y_AXIS = 0.0
Z_AXIS = 0.0
 
DIRECTION = 1

save_counter = 0
depth_texture = None
save_limit = int(sys.argv[1]) if len(sys.argv) > 1 else 1
width = int(sys.argv[2]) if len(sys.argv) > 3 else 640
height = int(sys.argv[3]) if len(sys.argv) > 3 else 480
point_size = float(sys.argv[4]) if len(sys.argv) > 4 else 4.0
bg_threshold = int(sys.argv[5]) if len(sys.argv) > 5 else -1
input_img_name = sys.argv[6] if len(sys.argv) > 6 else 'input.png'
output_img_name = sys.argv[7] if len(sys.argv) > 7 else 'output.gif'

gif_imgs = []
 
 
def InitGL(): 
    global width, height

    glClearColor(0.8, 0.8, 0.8, 0.0)
    glClearDepth(1.0) 
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)   
    glMatrixMode(GL_PROJECTION)
    #gluPerspective(45.0, float(width)/float(height), 15, 45.0)
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(-100.0, 100.0, -100.0, 100.0, -100.0, 100.0);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glRotatef(35.264, 1.0, 0.0, 0.0);
    glRotatef(-45.0, 0.0, 1.0, 0.0);
    glScalef(10.0, 10.0, -10.0);
 
def DrawGLScene():
    global save_counter
    global X_AXIS,Y_AXIS,Z_AXIS
    global DIRECTION
    global gif_imgs
    global bg_threshold


    degrees_max = 360
    #X_AXIS = random.random() * degrees_max
    #Y_AXIS = random.random() * degrees_max
    #Z_AXIS = random.random() * degrees_max

    scale_min = 5
    scale_max = 12
    #X_SCALAR = scale_min + random.random() * (scale_max - scale_min)
    #Y_SCALAR = scale_min + random.random() * (scale_max - scale_min)
    #Z_SCALAR = scale_min + random.random() * (scale_max - scale_min)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    #glLoadIdentity()

    if X_AXIS <= -3.14:
        X_AXIS = 0
        Y_AXIS = 0
        Z_AXIS = 0
    #glTranslatef(0.0,0.0,-50.0)
    glRotatef(X_AXIS,1.0,0.0,0.0)
    glRotatef(Y_AXIS,0.0,1.0,0.0)
    glRotatef(Z_AXIS,0.0,0.0,1.0)

    # Draw Cube (multiple quads)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glPointSize(point_size)
    glBegin(GL_POINTS)
    #glBegin(GL_LINES)

    
    glColor3f(0.2,0.2,0.2)
    
    #draw_cube_vertices()
    im = Image.open(input_img_name)
    im = im.convert('L') # to grayscale if needed
    im_arr = np.array(im)

    current_bg_thresh = bg_threshold if bg_threshold > -1 else np.max(im_arr)
    non_bg_truth_table = im_arr < current_bg_thresh # np.max(im_arr) # 204 for real 150 for fake
    vertex_xy = np.argwhere(non_bg_truth_table)
    vertex_z = im_arr[non_bg_truth_table]
    norm_factor = 5 # normalize xyz coordinates to range of -norm_factor to norm_factor so it's in view of camera
    vertex_xy = normalize_arr(vertex_xy, norm_factor)
    vertex_z = normalize_arr(vertex_z, norm_factor)
    for xy, z in zip(vertex_xy, vertex_z):
        x = xy[1]
        y = xy[0]
        glVertex3f(x, y, z) 

    glEnd()


    rotate_delta = 0.30
    X_AXIS = X_AXIS - rotate_delta
    Y_AXIS = Y_AXIS - rotate_delta
    Z_AXIS = Z_AXIS - rotate_delta


    if save_counter < save_limit:
        capture_screen(gif_imgs)
    else:
        print('saving gif...')
        save_gif(gif_imgs)
        sys.exit()

    save_counter += 1

    glutSwapBuffers()


def save_gif(gif_imgs):
    global output_img_name
    print(output_img_name)
    imageio.mimsave(output_img_name, gif_imgs)


def normalize_arr(arr, norm_factor):
    return ((arr - np.min(arr))/ (np.max(arr) - np.min(arr))) * norm_factor * 2 - norm_factor


def capture_screen(gif_imgs=None, filename=None):
    global width, height
    glPixelStorei(GL_PACK_ALIGNMENT, 1)

    # for rgb to grayscale conversion
    glPixelTransferf(GL_RED_SCALE, 0.299);
    glPixelTransferf(GL_GREEN_SCALE, 0.587);
    glPixelTransferf(GL_BLUE_SCALE, 0.114);

    data = glReadPixels(0, 0, width, height, GL_LUMINANCE, GL_UNSIGNED_BYTE)

    glPixelTransferf(GL_RED_SCALE, 1);
    glPixelTransferf(GL_GREEN_SCALE, 1);
    glPixelTransferf(GL_BLUE_SCALE, 1);

    image = Image.frombytes("L", (width, height), data)
    if filename is not None:
        image.save(filename, 'png')
    if gif_imgs is not None:
        gif_imgs.append(image)
 
def main():
    global width, height
    global window

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(200,200)

    window = glutCreateWindow('OpenGL Python Cube')

    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    InitGL()
    glutMainLoop()
 
if __name__ == "__main__":
    main() 



