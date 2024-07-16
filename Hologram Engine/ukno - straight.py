import pygame
from math import *
import numpy as np
import cv2

pygame.init()
pygame.display.set_caption('Engine shit')
Surface  = pygame.display.set_mode((1920,1080),pygame.FULLSCREEN)
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
        y=cos(a)*j[0]+sin(a)*j[2]
        i[0]=y
        x=-sin(a)*j[0]+cos(a)*j[2]
        i[2]=x
        
def rotateX(a,obj):
    a = radians(a)
    for i in obj:
        j=i
        y=cos(a)*j[1]-sin(a)*j[2]
        i[1]=y
        x=sin(a)*j[1]+cos(a)*j[2]
        i[2]=x
        
def rotateZ(a,obj):
    a = radians(a)
    for i in obj:
        j=i
        y=cos(a)*j[0]-sin(a)*j[1]
        i[0]=y
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
        x=[dz[faces[i][0]],dz[faces[i][1]],dz[faces[i][2]]]
        avz=0
        for j in x:
            avz+=j
        avz/=4
        pos.append([i,avz])
    pos=sorted(pos,key=lambda xo: xo[1])
    pos=Reverse(pos)
    faces2=[]

    for i in pos:
        faces2.append(faces[i[0]])


    for i in range(len(faces2)):
        x=[img[faces2[i][0]],img[faces2[i][1]],img[faces2[i][2]]]
        normal = np.cross( np.subtract(obj[faces2[i][2]],obj[faces2[i][0]]) , np.subtract(obj[faces2[i][1]],obj[faces2[i][0]] ) )
        normal = normalize(normal)
        intn = np.dot(l,normal)
        if intn>0:
            pygame.draw.polygon(Surface, (255*intn,255*intn,255*intn), x, 0)
        else:
            pygame.draw.polygon(Surface, (0,0,0), x, 0)

            
scale(150,vertices)

mi=0
for i in vertices:
    if (i[2]<mi):
        mi=i[2]

c=[0,0,25*50]
e=[0,0,25*50]
t=[0,0,0]
l=[0,0,-1]


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(1)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                c[0]+=100
                e[0]-=100
                
            if event.key == pygame.K_RIGHT:
                c[0]-=100
                e[0]+=100
                
            if event.key == pygame.K_UP:
                c[1]+=100
                e[1]-=100
                
            if event.key == pygame.K_DOWN:
                c[1]-=100
                e[1]+=100
                
            if event.key == pygame.K_PAGEUP:
                c[2]+=100
                e[2]+=100
                
            if event.key == pygame.K_PAGEDOWN:
                c[2]-=100
                e[2]-=100

#
            if event.key == pygame.K_w:
                translate(0,50,0,vertices)
                
            if event.key == pygame.K_s:
                translate(0,-50,0,vertices)
                
            if event.key == pygame.K_a:
                translate(50,0,0,vertices)
                
            if event.key == pygame.K_d:
                translate(-50,0,0,vertices)

            if event.key == pygame.K_q:
                translate(0,0,-50,vertices)
                
            if event.key == pygame.K_e:
                translate(0,0,50,vertices) 

    #ret, imgk = cap.read()
    #gray = cv2.cvtColor(imgk, cv2.COLOR_BGR2GRAY)
    #facesk = face_cascade.detectMultiScale(gray, 1.3, 5)
    #for (xk,yk,w,h) in facesk:
     #   cv2.rectangle(imgk,(xk,yk),(xk+w,yk+h),(255,0,0),2)
      #  xk+=w/2
       # yk+=h/2
    #cv2.imshow('img',imgk)
    #k = cv2.waitKey(30) & 0xff

    #xk-=640/2
    #yk-=480/2
    #or=xk
    #bop=-yk
    #c=[cor,bop,250]
    #e=[-cor,-bop,250]
    
    #rotateY(1,vertices)
    #rotateZ(1,vertices)
    #rotateX(1,vertices)

    Surface.fill((0,0,0))


    render(vertices,faces,c,t,e)

    clock.tick(60)
    pygame.display.update()
pygame.quit()
cap.release()
cv2.destroyAllWindows()
quit()
