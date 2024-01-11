import pygame
import pygame.freetype
import math
import time as t
import matplotlib.pyplot as plt
import pylab as plb

pygame.font.init()
pygame.freetype.init()
width = 800
height = 600
window = pygame.display.set_mode((width,height))
pygame.display.set_caption("Projectile Motion")
clock = pygame.time.Clock()
fps = 60
velocities = []
time = []
ground = pygame.Rect(5,height-100,width,100)

class Ball():
    def __init__(self) -> None:
        self.ball_r = pygame.Rect(5,ground.y-10,10,10)
        self.duration = 0
        self.newx = 0
        self.newy = 0

    def controls(self,mousex,mousey):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            mousex-=5
        if keys[pygame.K_RIGHT]:
            mousex+=5
        if keys[pygame.K_UP]:
            mousey-=5
        if keys[pygame.K_DOWN]:
            mousey+=5
        return mousex,mousey

    def movement(self,ball_r2,hvelocity,vvelocity,duration,mousex,mousey,angle,i,h_max,down):
        pygame.draw.rect(window,g.black,ball_r2)# movement does not work after first throw
        mag = math.sqrt(vvelocity**2+hvelocity**2)/5 # chromebook numpy issue
        newx = (ball_r2.x+c.x[i])
        newy = (ball_r2.y-c.y[i])
        if newy <= height-h_max:
            down = True
        if down == True:
            velocities.append(-mag)
        else:
            velocities.append(mag)             
        time.append(duration)
        t.sleep(0.05)      
        duration+=0.05 
        ball_r2 = pygame.Rect(newx,newy,10,10)
        window.fill(g.white)
        g.draw(ball_r2)
        g.text(vvelocity,hvelocity,angle,duration)
        pygame.display.flip()
        clock.tick(fps)
        return duration,ball_r2,i,down

    def collision(self,duration,ball_r2):
        duration = 0
        b.ball_r.x = ball_r2.x
        b.ball_r.y = ball_r2.y-15
        return duration,ball_r2

    def reset(self): # reset if goes oob or allow for frame to be extended
        duration = 0
        b.ball_r.x = 5
        b.ball_r.y = height-110
        self.newx = b.ball_r.x
        self.newy = b.ball_r.y
        self.stop = False
        return duration,5,(height-110)

class Calculations():
    def __init__(self) -> None:
        self.gravity = 9.81
        self.x = []
        self.y = []

    def velocity(self,vdistance,hdistance):
        try:
            vvelocity = round(math.sqrt(2*self.gravity*vdistance),2)
        except ValueError:
            vvelocity = 0
        try:
            hvelocity = round(math.sqrt(2*self.gravity*hdistance),2)
        except ValueError:
            hvelocity = 0
        return vvelocity,hvelocity

    def distance(self,lenx,leny):
        hdistance = round(lenx*10,2)
        vdistance = round(leny*10,2)
        return hdistance,vdistance

    def angle(self,lenx,leny):
        try:
            angle = round(math.degrees(math.atan(leny/lenx)))
        except ZeroDivisionError:
            angle = 90
        return angle

    def trajectory(self,vvelocity,hvelocity,angle):
        y0=100
        mag = math.sqrt(vvelocity**2+hvelocity**2)       
        b=-2*mag*math.sin(angle)
        c=-2*y0
        coeff=plb.array([self.gravity,b,c])
        t1,t2=plb.roots(coeff)
        h1=mag**2*(math.sin(angle))**2/(2*self.gravity)
        h_max=h1*10+y0
        R=mag*math.cos(angle)*plb.max(t1,t2)
        self.x=plb.linspace(0,R,50)
        self.y=self.x*math.tan(angle)-(1/2)*(self.gravity*self.x**2)/(mag**2*(math.cos(angle))**2)
        return self.x,self.y,h_max

    def graphs(self,x,y):
        plt.plot(x,y)
        plt.savefig("proto2.png")
    

class Graphics():
    def __init__(self) -> None:
        self.font = pygame.font.SysFont("Arial", 30, False)
        self.bounds = pygame.Rect(0,0,width,height)
        self.white = (255,255,255)
        self.green = (0,100,0)
        self.red = (255,0,0)
        self.black = (0,0,0)

    def draw(self,ball_r2):
        pygame.draw.rect(window,self.white,self.bounds)
        pygame.draw.rect(window,self.green,ground)
        pygame.draw.rect(window,self.white,b.ball_r)
        pygame.draw.rect(window,self.black,ball_r2)

    def bounds_rect(self,ball_r2):
        if ball_r2.y > 600:
            ball_r2.y = 590
        if ball_r2.y < 0:
            ball_r2.y = 10
        if ball_r2.x > 800:
            ball_r2.x = 790
        if ball_r2.x < 0:
            ball_r2.x = 10
        return ball_r2

    def text(self,vvelocity,hvelocity,angle,duration):
        textfont = pygame.font.Font(None,40)
        window.blit(pygame.font.Font.render(textfont, f"Vertical Velocity: {round(vvelocity/50,2)}m/s", True, self.black, None), (2,40))
        window.blit(pygame.font.Font.render(textfont, f"Horizontal Velocity: {round(hvelocity/50,2)}m/s", True, self.black, None), (2,80))
        window.blit(pygame.font.Font.render(textfont, f"Angle: {angle}°", True, self.black, None), (2,0))
        window.blit(pygame.font.Font.render(textfont, f"Time: {round(duration,2)}s", True, self.black, None), (2,120))
        window.blit(pygame.font.Font.render(textfont, "1m", True, self.black, None), (100,b.ball_r.y+10))

def mainloop():
    pygame.init()
    run = True
    down = False
    duration = 0
    mousex = width/2
    mousey = height/2
    i = 0
    ball_r2 = pygame.Rect(5,ground.y-10,10,10)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #gr.velocitytime()
                c.graphs(time,velocities)
                run = False
        mousex,mousey = b.controls(mousex,mousey)
        leny = (height-((mousey+b.ball_r.y)-380))/10
        lenx = (mousex+(b.ball_r.x+10))/10
        g.draw(ball_r2)
        pygame.draw.line(window,g.red,pygame.math.Vector2(ball_r2.x+10,ball_r2.y),pygame.math.Vector2(mousex,mousey),5)
        hdistance,vdistance = c.distance(lenx,leny)
        angle = c.angle(lenx,leny)
        vvelocity,hvelocity = c.velocity(vdistance,hdistance)
        x,y,h_max = c.trajectory(vvelocity,hvelocity,angle)
        g.text(vvelocity,hvelocity,angle,duration)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            duration,ball_r2.x,ball_r2.y = b.reset()
        if keys[pygame.K_SPACE]:
            while pygame.Rect.contains(ground,ball_r2) == False:
                duration,ball_r2,i,down = b.movement(ball_r2,hvelocity,vvelocity,duration,mousex,mousey,angle,i,h_max,down)
                i+=1
                if pygame.Rect.contains(g.bounds,ball_r2) == False:
                    ball_r2 = g.bounds_rect(ball_r2)
        if pygame.Rect.contains(ground,ball_r2) or i > 50:
            duration,ball_r2 = b.collision(duration,ball_r2)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()

c = Calculations()
b = Ball()
g = Graphics()