from __future__ import division
import pygame
import numpy as np
from math import *
import time
import cv2
pygame.init()
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
pygame.display.set_caption('Engine shit')
Surface = gameDisplay = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()
cap = cv2.VideoCapture(1)
f = open("cube.obj","r")


vertices = []
faces = []


for i in f:
    if len(i)>2 and i[0]+i[1] == "v ":
        temp = i.split()
        vertices.append([ float(temp[1]), float(temp[2]), float(temp[3]) ])
    elif len(i)>2 and i[0]+i[1] == "f ":
        temp = i.split()
        faces.append([ int(temp[1].split("/")[0])-1, int(temp[2].split("/")[0])-1, int(temp[3].split("/")[0])-1 ])

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
    zbuffer=[]
    for i in range(600):
        temp=[]
        for j in range(600):
            temp.append(999)
        zbuffer.append(temp)

    
    
    for i in vertices:
        img.append(( perspective( i,c,t,e )[0]+250, perspective( i,c,t,e )[1]+250))
        
    for i in range(len(faces)):
        x= [ img[ faces[i][0] ], img[ faces[i][1] ], img[ faces[i][2] ]]
        normal = np.cross( np.subtract(vertices[faces[i][2]],vertices[faces[i][0]]) , np.subtract(vertices[faces[i][1]],vertices[faces[i][0]] ) )
        normal = normalize(normal)
        intn = np.dot(l,normal)

        if intn>0:
            
            '''
            bboxminX=int(min(x[0][0],x[1][0],x[2][0]))
            bboxmaxX=int(max(x[0][0],x[1][0],x[2][0]))
            bboxminY=int(min(x[0][1],x[1][1],x[2][1]))
            bboxmaxY=int(max(x[0][1],x[1][1],x[2][1]))
            for i in range(bboxminX,bboxmaxX+1):
                for j in range(bboxminY,bboxmaxY+1):
                    bc = barycentric(x,(i,j))
                    if bc[0]<0 or bc[1]<0 or bc[2]<0:
                        continue
                    gameDisplay.set_at((i, j), (255*intn,255*intn,255*intn))

                    z=bc[0]*x[0][2]+bc[1]*x[1][2]+bc[2]*x[2][2]
                    if zbuffer[i][j]>z:
                        zbuffer[i][j]=z
                        gameDisplay.set_at((i, j), (255*intn,255*intn,255*intn))
            '''
            pygame.draw.polygon(Surface, (255*intn,255*intn,255*intn) , x, 0)
                        
                
 
###################################################################

translate(-.5,-.5,-.5,vertices)
scale(100,vertices)
c=[0,0,3000]
t=[0,0,0]
e=[-0,0,3000]
l=[0,0.1,-1]


cor=0
while 1:
    '''
    ret, imgk = cap.read()
    gray = cv2.cvtColor(imgk, cv2.COLOR_BGR2GRAY)
    facesk = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in facesk:
        cv2.rectangle(imgk,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = imgk[y:y+h, x:x+w]

    cv2.imshow('img',imgk)
    k = cv2.waitKey(30) & 0xff
    x=x*50
    cor=x-(320)

'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                cor-=100
                c=[cor,0,3000]
                e=[-cor,0,3000]
    gameDisplay.fill((0,0,220))
    #rotateY(1,vertices)
    #rotateZ(1,vertices)
    rotateX(1,vertices)
    render(vertices, faces, c, t ,e )
    clock.tick(60)
    pygame.display.update()

cap.release()
cv2.destroyAllWindows()
pygame.quit()
quit()
