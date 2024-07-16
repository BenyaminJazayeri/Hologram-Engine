import pygame
import numpy as np
from math import *

pygame.init()
pygame.display.set_caption('Engine shit')
Surface = gameDisplay = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()

f = open("african_head.obj","r")


vertices = []
faces = []


for i in f:
    if len(i)>2 and i[0]+i[1] == "v ":
        temp = i.split()
        vertices.append([ float(temp[1]), float(temp[2]), float(temp[3]) ])
    elif len(i)>2 and i[0]+i[1] == "f ":
        temp = i.split()
        faces.append([ int(temp[1].split("/")[0])-1, int(temp[2].split("/")[0])-1, int(temp[3].split("/")[0])-1 ])

def normalize(normal):
        m = sqrt(float(np.dot(normal,normal)))
        normal = [normal[0]/m,normal[1]/m,normal[2]/m]        
        return normal


def translate(x,y,z,obj):
    for i in obj:
        i[0]=i[0]+x
        i[1]=i[1]+y
        i[2]=i[2]+z
        
def rotateY(a,obj):
    a = radians(a)
    for i in obj:
        j=i
        x=cos(a)*j[0]+sin(a)*j[2]
        i[0]=x
        x=-sin(a)*j[0]+cos(a)*j[2]
        i[2]=x
        
def rotateX(a,obj):
    a = radians(a)
    for i in obj:
        j=i
        x=cos(a)*j[1]-sin(a)*j[2]
        i[1]=x
        x=sin(a)*j[1]+cos(a)*j[2]
        i[2]=x
        
def rotateZ(a,obj):
    a = radians(a)
    for i in obj:
        j=i
        x=cos(a)*j[0]-sin(a)*j[1]
        i[0]=x
        x=sin(a)*j[0]+cos(a)*j[1]
        i[1]=x
        
def scale(a,obj):
    for i in obj:
        i[0]=i[0]*a
        i[1]=i[1]*a
        i[2]=i[2]*a
        
def perspective(a,c,theta,e):
    
    x= a[0]-c[0]
    y= a[1]-c[1]
    z= a[2]-c[2]

    tx= radians(theta[0])
    ty= radians(theta[1])
    tz= radians(theta[2])

    ex= e[0]
    ey= e[1]
    ez= e[2]
    
    dx= cos(ty) * ( sin(tz)*y + cos(tz)*x ) - sin(ty)*z
    dy= sin(tx) * ( cos(ty)*z + sin(ty)*( sin(tz)*y + cos(tz)*x )) + cos(tx)*( cos(tz)*y - sin(tz)*x)
    dz= cos(tx) * ( cos(ty)*z + sin(ty)*( sin(tz)*y + cos(tz)*x )) - sin(tx)*( cos(tz)*y - sin(tz)*x)

    bx= ez*dx/dz +ex
    by= ez*dy/dz +ey

    b=(bx,by)
    return b

def render( vertices ,faces ,c ,t ,e):
    img=[]

    
    
    for i in vertices:
        img.append(( perspective( i,c,t,e )[0]+250, perspective( i,c,t,e )[1]+250))
        
    for i in range(len(faces)):
        x= [ img[ faces[i][0] ], img[ faces[i][1] ], img[ faces[i][2] ]]
        normal = np.cross( np.subtract(vertices[faces[i][2]],vertices[faces[i][0]]) , np.subtract(vertices[faces[i][1]],vertices[faces[i][0]] ) )
        normal = normalize(normal)
        intn = np.dot(l,normal)
        if intn>0:
            pygame.draw.polygon(Surface, (255*intn,255*intn,255*intn) , x, 0)
    for i in range(500):
        for j in range(500):
            gameDisplay.set_at((i, j), (0,0,255))
###################################################################
temp=vertices

rotateX(180,vertices)
scale(300,vertices)
c=[0,0,-3000]
t=[0,0,0]
e=[0,0,3000]
l=[0,0,1]
flag=0

while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                c[2]+=100
                e[1]+=100

    gameDisplay.fill((0,0,0))
    rotateY(1,vertices)
    rotateZ(1,vertices)
    rotateX(1,vertices)
    render(vertices, faces, c, t ,e )
    clock.tick(60)
    pygame.display.update()
pygame.quit()
quit()
