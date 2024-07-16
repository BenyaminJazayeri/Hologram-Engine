import pygame
from math import *
import numpy as np
pygame.init()
pygame.display.set_caption('Engine shit')
Surface = gameDisplay = pygame.display.set_mode((1920,1080))
clock = pygame.time.Clock()

cube= [
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, -1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, -1, 1],
    [-1, 1, 1]
    ]


edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

color = [
    [0,0,255],
    [0,255,0],
    [255,0,0],
    [255,255,0],
    [0,255,255],
    [255,0,255]]
def Reverse(lst): 
    return [ele for ele in reversed(lst)]

def clone(cube):
    tempy=[]
    for k in cube:
        templist=[]
        for h in k:
            templist.append(h)
        tempy.append(templist)
    return tempy

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

    b=(bx,by,dx,dy,dz)
    return b

def barycentric(pts,P):
    x=np.array((    pts[2][0]-pts[0][0],
                    pts[1][0]-pts[0][0],
                    pts[0][0]-P[0]))
    
    y=np.array((    pts[2][1]-pts[0][1],
                    pts[1][1]-pts[0][1],
                    pts[0][1]-P[1]))
    u = np.cross(x,y).tolist()
    if (abs(u[2])<1):
        return (-1,1,1);
    return (1.0-(u[0]+u[1])/u[2], u[1]/u[2], u[0]/u[2]); 

def normalize(normal):
        m = sqrt(float(np.dot(normal,normal)))
        normal = [normal[0]/m,normal[1]/m,normal[2]/m]        
        return normal
    
def render(obj,faces,c,t,e):
    img=[]
    dz=[]
    
    for i in obj:
        p=perspective( i,c,t,e )
        img.append((p[0]+1920/2,p[1]+1080/2))
        dis=sqrt(pow(p[2],2)+pow(p[3],2)+pow(p[4],2))
        dz.append(dis)
    pos=[]
    for i in range(len(faces)):
        x=[dz[faces[i][0]],dz[faces[i][1]],dz[faces[i][2]],dz[faces[i][3]]]
        avz=0
        for j in x:
            avz+=j
        avz/=4
        pos.append([i,avz])
    pos=sorted(pos,key=lambda xo: xo[1])
    pos=Reverse(pos)
    faces2=[]
    color2=[]
    for i in pos:
        faces2.append(faces[i[0]])
        color2.append(color[i[0]])

    

    for i in range(len(faces2)):
        x=[img[faces2[i][0]],img[faces2[i][1]],img[faces2[i][2]],img[faces2[i][3]]]
        normal = np.cross( np.subtract(obj[faces2[i][2]],obj[faces2[i][0]]) , np.subtract(obj[faces2[i][1]],obj[faces2[i][0]] ) )
        normal = normalize(normal)
        intn = np.dot(l,normal)
        if intn>0:
            pygame.draw.polygon(Surface, (color2[i][0]*intn,color2[i][1]*intn,color2[i][2]*intn), x, 0)
        else:
            pygame.draw.polygon(Surface, (0,0,0), x, 0)
    '''   
    for i in edges:
        pygame.draw.line(Surface,(255,255,255) , (img[i[0]][0],img[i[0]][1]), (img[i[1]][0],img[i[1]][1]),1)
    '''
############################################################################################################################################################################################################

scale(50,cube)
c=[100,0,250]
t=[0,0,0]
e=[-100,0,250]
l=[0.5,-0.5,0.5]

cor=0
pygame.display.toggle_fullscreen()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                cor+=100
                c=[cor,0,250]
                e=[-cor,0,250]

    gameDisplay.fill((0,0,0))
    #rotateY(1,cube)
    rotateZ(1,cube)
    #rotateX(1,cube)

    for i in range(5):
        for j in range(5):
            tempy=clone(cube)
            translate(i*150-150,j*150-150,0,tempy)
            render(tempy,surfaces,c,t,e)

    clock.tick(60)
    pygame.display.update()
pygame.quit()
quit()
