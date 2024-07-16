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
    
def barycentric(pts,p):
    v0 = np.subtract(pts[1],pts[0])
    v1 = np.subtract(pts[2],pts[0])
    v2 = np.subtract(p,pts[0])
    d00 = np.dot(v0, v0)
    d01 = np.dot(v0, v1)
    d11 = np.dot(v1, v1)
    d20 = np.dot(v2, v0)
    d21 = np.dot(v2, v1)
    denom = d00 * d11 - d01 * d01
    v = (d11 * d20 - d01 * d21) / denom
    w = (d00 * d21 - d01 * d20) / denom
    u = 1.0 - v - w;
    return (u,v,w)
    
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
    b2=(dx,dy,dz)
    return (b,b2)

def render( vertices ,faces ,c ,t ,e):
    
    img=[]
    storage = []
    for i in vertices:
        pointpack = perspective( i,c,t,e )
        img.append(( pointpack[0][0]+250, pointpack[0][1]+250))
        storage.append(pointpack[1])
    for i in range(len(faces)):
        x= [ img[ faces[i][0] ], img[ faces[i][1] ], img[ faces[i][2] ]]
        normal = np.cross( np.subtract(vertices[faces[i][2]],vertices[faces[i][0]]) , np.subtract(vertices[faces[i][1]],vertices[faces[i][0]] ) )
        normal = normalize(normal)
        intn = np.dot(l,normal)
        if intn>0:

            g= [ storage[ faces[i][0] ], storage[ faces[i][1] ], storage[ faces[i][2] ]]
            bboxminX=min(x[0][0],x[1][0],x[2][0])
            bboxmaxX=max(x[0][0],x[1][0],x[2][0])
            bboxminY=min(x[0][1],x[1][1],x[2][1])
            bboxmaxY=max(x[0][1],x[1][1],x[2][1])
            for i in range(int(bboxminX),int(bboxmaxX)+1):
                for j in range(int(bboxminY),int(bboxmaxY)+1):
                    p=[i,j,0]
                    bc = barycentric(g,p)
                    print bc
                    if bc[0]<0 or bc[1]<0 or bc[2]<0:
                        continue
                    p[2]+=bc[0]*g[0][2]+bc[1]*g[1][2]+bc[2]*g[2][2]

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
    #rotateY(1,vertices)
    #rotateZ(1,vertices)
    #rotateX(1,vertices)
    render(vertices, faces, c, t ,e )
    clock.tick(60)
    pygame.display.update()
pygame.quit()
quit()
