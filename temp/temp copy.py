import pygame
import pygame.freetype
import pygame_gui
import math
import pylab as plb
import matplotlib.pyplot as plt
import time as t

pygame.freetype.init()
pygame.font.init()
width = 800
height = 600
window = pygame.display.set_mode((width,height))
pygame.display.set_caption("Projectile Motion Simulator")
manager = pygame_gui.UIManager((width,height))
ground = pygame.Rect(-5,height-100,width+5,100)
clock = pygame.time.Clock()
fps = 60

# default settings state
units_type = "Metric"
units = "M"
object = "Ball"
acceleration = 9.81
scale = 50

class Ball:
    def __init__(self) -> None:
        self.ball = pygame.Rect(15,ground.y-10,10,10)
    
    def controls(self,mouse_x,mouse_y):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            mouse_x-=5
        if keys[pygame.K_RIGHT]:
            mouse_x+=5
        if keys[pygame.K_UP]:
            mouse_y-=5
        if keys[pygame.K_DOWN]:
            mouse_y+=5
        return mouse_x,mouse_y
    
    def reset(self):
        c.duration = 0
        self.ball.x = 15
        self.ball.y = ground.y-10

    def bounds_rect(self):
        if self.ball.y > 600:
            self.ball.y = 590
        if self.ball.y < 0:
            self.ball.y = 10
        if self.ball.x > 800:
            self.ball.x = 790
        if self.ball.x < 0:
            self.ball.x = 10
        
class Calculations:
    def __init__(self) -> None:
        self.new_x = 15
        self.new_y = ground.y-10
        self.x = []
        self.y = []
        self.duration = 0
        self.angle = 0
        self.down = False

    def magnitude(self,v_velocity,h_velocity):
        return math.sqrt(v_velocity**2+h_velocity**2)

    def trajectory(self,angle,v_velocity,h_velocity):
        mag_velocity = self.magnitude(v_velocity,h_velocity)
        R = mag_velocity**2*math.sin(2*angle)/float(acceleration)
        h = mag_velocity**2*(math.sin(angle))**2/(2*float(acceleration))
        x = plb.linspace(0,R,50)
        y = x*math.tan(angle)-(1/2)*(float(acceleration)*x**2)/(mag_velocity**2*(math.cos(angle))**2 )
        plot(x,y)

class Graphics:
    def __init__(self) -> None:
        self.font = pygame.font.SysFont("Arial", 30, False)
        self.bounds = pygame.Rect(0,0,width,height)
        self.white = (255,255,255)
        self.green = (0,100,0)
        self.red = (255,0,0)
        self.black = (0,0,0)
        self.grey = (207,207,207)
    
    def draw_text(self,v_velocity,h_velocity,angle):
        textfont = pygame.font.Font(None,30)
        window.blit(pygame.font.Font.render(textfont, f"Horizontal Velocity: {h_velocity}", True, self.black, None), (410,550))
        window.blit(pygame.font.Font.render(textfont, f"Vertical Velocity: {v_velocity}", True, self.black, None), (160,550))
        window.blit(pygame.font.Font.render(textfont, f"Angle: {angle}", True, self.black, None), (10,550))
    
    def keyboard(self,img,no_image,v_velocity,h_velocity,angle):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run = False
        else:
            run = True
        if keys[pygame.K_SPACE] and no_image == False:
            window.fill(g.grey)
            c.trajectory(angle,v_velocity,h_velocity)
        if keys[pygame.K_UP]:
            v_velocity+=0.5
        if keys[pygame.K_DOWN]:
            v_velocity-=0.5
        if keys[pygame.K_RIGHT]:
            h_velocity+=0.5
        if keys[pygame.K_LEFT]:
            h_velocity-=0.5
        if keys[pygame.K_w]:
            angle+=1
        if keys[pygame.K_s]:
            angle-=1
        return run,v_velocity,h_velocity,angle
    
def load_settings():
    try:
        with open("saves/settings.txt") as f:
            settings_list = f.read().splitlines()
        units_type = settings_list[0]
        units = settings_list[1]
        object = settings_list[2]
        acceleration = settings_list[3]
        scale = settings_list[4]
    except IndexError:
        pass
    return units_type,units,object,acceleration,scale

def plot(x,y):
    plt.xlim(0,100)
    plt.ylim(0,100)
    plt.plot(x,y)
    plt.savefig("saves/xy.png")

class Loop:
    def __init__(self) -> None:
        self.units_type, self.units, self.object, self.acceleration, self.scale = load_settings()
        self.back = False
    
    def mainloop(self): #1m = 38.3333333333 px 500 scale
        run = True
        mouse_x = width/2
        mouse_y = height/2
        no_image = False
        button_pressed = None
        v_velocity = 0
        h_velocity = 0
        angle = 0
        try:
            img = pygame.image.load("saves/xy.png").convert()
        except:
            no_image = True
        while run:
            time_delta = clock.tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            run,v_velocity,h_velocity,angle = g.keyboard(img,no_image,v_velocity,h_velocity,angle)
            window.fill(g.white)
            g.draw_text(v_velocity,h_velocity,angle)
            window.blit(img, (0, 0))
            manager.update(time_delta)
            manager.draw_ui(window)
            pygame.display.update()
            clock.tick(fps)

b = Ball()
g = Graphics()
c = Calculations()
l = Loop()

pygame.init()
units_type,units,object,acceleration,scale = load_settings()
l.mainloop()
