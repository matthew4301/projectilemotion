import pygame
import math
import time as t
import matplotlib.pyplot as plt

class Loop:
    def __init__(self) -> None:
        pygame.init()
        self.width = 800
        self.height = 600
        self.window = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("Projectile Motion")
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.velocities = []
        self.time = []
        self.x = []
        self.y = []
        self.ground = pygame.Rect(5,self.height-100,self.width,100)

    def mainloop(self):
        run = True
        back = False
        first = True
        duration = 0
        mousex = self.width/2
        mousey = self.height/2
        ball_r2 = pygame.Rect(5,self.ground.y-10,10,10)
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    c.graphs(self.x,self.y)
                    run = False
            mousex,mousey = b.controls(mousex,mousey)
            leny = (self.height-((mousey+b.ball_r.y)-380))/10
            if back == True:
                lenx = (mousex+(b.ball_r.x+10))/10
            else:
                lenx = (mousex-(b.ball_r.x+10))/10
            g.draw(ball_r2)
            pygame.draw.line(self.window,g.red,pygame.math.Vector2(ball_r2.x+10,ball_r2.y),pygame.math.Vector2(mousex,mousey),5)
            hdistance,vdistance = c.distance(lenx,leny)
            angle,back = c.angle(back,lenx,leny)
            if first == True:
                vvelocity,hvelocity = c.velocity(c.gravity,vdistance,hdistance,angle)
            g.text(vvelocity,hvelocity,mousex,mousey,angle,duration)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                first,duration,ball_r2.x,ball_r2.y = b.reset()
            if keys[pygame.K_SPACE]:
                while pygame.Rect.contains(self.ground,ball_r2) == False:
                    duration,ball_r2,back = b.movement(ball_r2,hvelocity,vvelocity,duration,first,back,mousex,mousey,angle)
                    if pygame.Rect.contains(g.bounds,ball_r2) == False:
                        ball_r2 = g.bounds(ball_r2)
            if pygame.Rect.contains(self.ground,ball_r2):
                first,duration,ball_r2 = b.collision(first,duration,ball_r2)
            pygame.display.update()
            self.clock.tick(self.fps)
        pygame.quit()

l = Loop()

class Ball():
    def __init__(self) -> None:
        self.ball_r = pygame.Rect(5,l.ground.y-10,10,10)
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
    
    def movement(self,ball_r2,hvelocity,vvelocity,duration,first,back,mousex,mousey,angle):
        pygame.draw.rect(l.window,g.black,ball_r2) # movement does not work after first throw
        if first == True:
            mag = math.sqrt(hvelocity**2+vvelocity**2)
            l.velocities.append(mag)
            first = False
        duration+=0.1
        l.time.append(duration)
        distancex = (hvelocity/2)*duration            
        distancey = ((vvelocity/2)*duration)+((-4.9 * (duration**2))/2)
        if back == True:
            newx = ((b.ball_r.x)-distancex)
            back = False
        else:
            newx = ((b.ball_r.x)+distancex)
        l.x.append(newx)
        l.x = (b.ball_r.y-distancey)
        l.y.append(l.height-self.newy)
        ball_r2 = pygame.Rect(newx,self.newy,10,10)
        l.window.fill(g.white)
        g.draw(ball_r2)
        g.text(vvelocity,hvelocity,mousex,mousey,angle,duration)
        pygame.display.flip()
        l.clock.tick(l.fps)
        t.sleep(0.01)
        return duration,ball_r2,back
    
    def collision(self,first,duration,ball_r2):
        first = True
        duration = 0
        b.ball_r.x = ball_r2.x
        b.ball_r.y = ball_r2.y-15
        return first,duration,ball_r2

    def reset(self): # reset if goes oob or allow for frame to be extended
        duration = 0
        b.ball_r.x = 5
        b.ball_r.y = l.height-110
        self.newx = b.ball_r.x
        self.newy = b.ball_r.y
        self.stop = False
        first = True
        return first,duration,5,(l.height-110)

class Calculations():
    def __init__(self) -> None:
        self.gravity = 9.81

    def velocity(self,gravity,vdistance,hdistance,angle):
        try:
            vvelocity = round(math.sqrt(2*gravity*vdistance),2)
        except ValueError:
            vvelocity = 0
        try:
            hvelocity = round(math.sqrt(2*gravity*hdistance),2)
        except ValueError:
            hvelocity = 0
        return vvelocity,hvelocity
    
    def angle(self,back,lenx,leny):
        try:
            angle = round(math.degrees(math.atan(leny/lenx)))
            if angle < 0:
                back = True
        except ZeroDivisionError:
            angle = 90
        return angle,back
    
    def distance(self,lenx,leny):
        hdistance = round(lenx*10,2)
        vdistance = round(leny*10,2)
        return hdistance,vdistance
    
    def graphs(self,x,y):
        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.plot(x,y)
        ax2.plot(l.velocities,l.time)
        fig.savefig("saves/graphs/velocitytime.png")

class Graphics():
    def __init__(self) -> None:
        self.font = pygame.font.SysFont("Comic Sans MS", 30, False)
        self.bounds = pygame.Rect(0,0,l.width,l.height)
        self.white = (255,255,255)
        self.green = (0,100,0)
        self.red = (255,0,0)
        self.black = (0,0,0)

    def draw(self,ball_r2):
        pygame.draw.rect(l.window,self.white,self.bounds)
        pygame.draw.rect(l.window,self.green,l.ground)
        pygame.draw.rect(l.window,self.white,b.ball_r)
        pygame.draw.rect(l.window,self.black,ball_r2)

    def bounds(self,ball_r2):
        if ball_r2.y > 600:
            ball_r2.y = 590
        if ball_r2.y < 0:
            ball_r2.y = 10
        if ball_r2.x > 800:
            ball_r2.x = 790
        if ball_r2.x < 0:
            ball_r2.x = 10
        return ball_r2

    def text(self,vvelocity,hvelocity,mousex,mousey,angle,duration):
        l.window.blit(self.font.render(f"Vertical Velocity: {round(vvelocity/50,2)}m/s", True, self.black, None), (2,40))
        l.window.blit(self.font.render(f"Horizonal Velocity: {round(hvelocity/50,2)}m/s", True, self.black, None), (2,80))
        l.window.blit(self.font.render(f"Angle: {angle}°", True, self.black, None),(2,0))
        l.window.blit(self.font.render(f"Time: {round(duration,2)}s", True, self.black, None),(2,120))
        l.window.blit(self.font.render("1m", True, self.black, None),((100),b.ball_r.y+10))
        l.window.blit(self.font.render(f"x: {mousex} y: {mousey}", True, self.black, None),(2,160))

def start():
    l.mainloop()

c = Calculations()
b = Ball()
g = Graphics()