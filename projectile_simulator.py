import pygame
import pygame.freetype
import pygame_gui
import math
import pylab as plb
import matplotlib.pyplot as plt
import os.path

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

image_path = "saves/xy.png"
timestamp = os.path.getmtime(image_path)

class UpdatedImage:
    def __init__(self, filename):
        self.filename = filename
        self.last_update = 0         
        self.image = pygame.image.load(filename).convert()      
        self.reload_image()
    
    def draw_image(self, window, position):
        window.blit(self.image, position)

    def reload_image(self):
        current_file_time = os.path.getmtime(self.filename)
        if (current_file_time > self.last_update):
            self.last_update = current_file_time
            self.draw_image(window,(0,0))

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
        return x,y # h_max?
    
    def scale(self,x,y):
        for i in range(len(x)):
            x[i]/=int(scale)
        for i in range(len(y)):
            y[i]/=int(scale)
        return x,y

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
        if units == "M":
            window.blit(pygame.font.Font.render(textfont, f"Horizontal Velocity: {h_velocity}m/s", True, self.black, None), (410,550))
            window.blit(pygame.font.Font.render(textfont, f"Vertical Velocity: {v_velocity}m/s", True, self.black, None), (160,550))
        if units == "CM":
            window.blit(pygame.font.Font.render(textfont, f"Horizontal Velocity: {h_velocity}cm/s", True, self.black, None), (410,550))
            window.blit(pygame.font.Font.render(textfont, f"Vertical Velocity: {v_velocity}cm/s", True, self.black, None), (160,550))
        if units == "KM":
            window.blit(pygame.font.Font.render(textfont, f"Horizontal Velocity: {h_velocity}km/h", True, self.black, None), (410,550))
            window.blit(pygame.font.Font.render(textfont, f"Vertical Velocity: {v_velocity}km/h", True, self.black, None), (160,550))
        if units == "IN":
            window.blit(pygame.font.Font.render(textfont, f"Horizontal Velocity: {h_velocity}in/s", True, self.black, None), (410,550))
            window.blit(pygame.font.Font.render(textfont, f"Vertical Velocity: {v_velocity}in/s", True, self.black, None), (160,550))
        if units == "FT":
            window.blit(pygame.font.Font.render(textfont, f"Horizontal Velocity: {h_velocity}ft/m", True, self.black, None), (410,550))
            window.blit(pygame.font.Font.render(textfont, f"Vertical Velocity: {v_velocity}ft/m", True, self.black, None), (160,550))
        if units == "MI":
            window.blit(pygame.font.Font.render(textfont, f"Horizontal Velocity: {h_velocity}mph", True, self.black, None), (410,550))
            window.blit(pygame.font.Font.render(textfont, f"Vertical Velocity: {v_velocity}mph", True, self.black, None), (160,550))
        window.blit(pygame.font.Font.render(textfont, f"Angle: {angle}°", True, self.black, None), (10,550))
    
    def keyboard(self,v_velocity,h_velocity,angle):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run = False
        else:
            run = True
        if keys[pygame.K_SPACE]:
            window.fill(g.grey)
            x,y = c.trajectory(angle,v_velocity,h_velocity)
            x,y = c.scale(x,y)
            plot(x,y)
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
    plt.xlim(0,100/int(scale))
    plt.ylim(0,100/int(scale))
    plt.plot(x,y)
    plt.savefig("saves/xy.png")

def mainloop():
    pygame.init()
    image = UpdatedImage("saves/xy.png")
    run = True
    v_velocity = 0
    h_velocity = 0
    angle = 0
    while run:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        run,v_velocity,h_velocity,angle = g.keyboard(v_velocity,h_velocity,angle)
        window.fill(g.white)
        g.draw_text(v_velocity,h_velocity,angle)
        image.reload_image()
        image.draw_image(window,(0,0))
        manager.update(time_delta)
        manager.draw_ui(window)
        pygame.display.update()
        clock.tick(fps)
    return True

g = Graphics()
c = Calculations()
units_type,units,object,acceleration,scale = load_settings()
