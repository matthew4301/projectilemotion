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
        #self.x = []
        #self.y = []
        self.x2 = []
        self.y2 = []
        self.velocities = []
        self.time = []
        self.duration = 0
        self.angle = 0
        self.down = False
        self.f = self.trajectory()

    def velocity(self,angle,power):
        v_velocity = math.sin(angle)*power
        h_velocity = math.cos(angle)*power
        return v_velocity,h_velocity
    
    def distance(self,len_x,len_y):
        h_distance = len_x/int(scale) # depending on scale
        v_distance = len_y/int(scale)
        return h_distance,v_distance
    
    def power(self,len_x,len_y):
        power = math.sqrt((len_x**2)+(len_y**2))/int(scale)
        return power
    
    def angle(self,len_x,len_y):
        try:
            self.angle = math.degrees(math.atan(len_y/len_x))
        except ZeroDivisionError:
            self.angle = 90

    
    def trajectory(self):
        return self.new_x * math.tan(self.angle) - self.f * self.new_x ** 2
    
    def movement(self,h_velocity,v_velocity,angle,len_x,len_y,i,h_max): # backwards???
        g.draw_rect()
        b.bounds_rect()
        g.draw_text(v_velocity,h_velocity,angle,len_x,len_y)
        mag_velocity = math.sqrt(v_velocity**2+h_velocity**2)
        try:
            self.new_x=(self.new_x+(self.x[i-1]-self.x[i]))
            self.x2.append(self.new_x)
            self.new_y=(self.new_y-(self.y[i]-self.y[i-1]))
            self.y2.append(self.new_y)
        except IndexError:
            pass
        i+=1
        if self.y[i]<= height-h_max:
            self.down = True
        if self.down == True:
            self.velocities.append(-mag_velocity)
        else:
            self.velocities.append(mag_velocity)
        self.time.append(self.duration)
        self.duration+=0.10
        #t.sleep(0.10)
        b.ball = pygame.Rect(self.new_x,self.new_y,10,10)
        window.fill(g.grey)
        pygame.draw.rect(window,g.black,b.ball)
        pygame.display.flip()
        clock.tick(fps)
        return i

class Graphics:
    def __init__(self) -> None:
        self.font = pygame.font.SysFont("Arial", 30, False)
        self.bounds = pygame.Rect(0,0,width,height)
        self.reset_var = False
        self.launch_var = False
        self.white = (255,255,255)
        self.green = (0,100,0)
        self.red = (255,0,0)
        self.black = (0,0,0)
        self.grey = (207,207,207)

    def draw_rect(self):
        pygame.draw.rect(window,self.green,ground)
        pygame.draw.rect(window,self.black,b.ball)
    
    def draw_line(self,mouse_x,mouse_y):
        pygame.draw.line(window,g.red,pygame.math.Vector2(b.ball.x+5,b.ball.y+5),pygame.math.Vector2(mouse_x,mouse_y),5)
        
    def draw_text(self,v_velocity,h_velocity,angle,len_x,len_y):
        textfont = pygame.font.Font(None,30)
        window.blit(pygame.font.Font.render(textfont, f"Vertical Velocity: {round(v_velocity/50,2)}m/s", True, self.black, None), (2,40))
        window.blit(pygame.font.Font.render(textfont, f"Horizontal Velocity: {round(h_velocity/50,2)}m/s", True, self.black, None), (2,80))
        window.blit(pygame.font.Font.render(textfont, f"Angle: {round(angle,0)}°", True, self.black, None), (2,0))
        window.blit(pygame.font.Font.render(textfont, f"{round(c.new_x,2)}, {round(c.new_y,2)}", True, self.black, None), (2,120))
        window.blit(pygame.font.Font.render(textfont, "1m", True, self.black, None), (5+int(scale),ground.y))
        window.blit(pygame.font.Font.render(textfont, "Space - Launch Projectile", True, self.black, None), (530,10))
        window.blit(pygame.font.Font.render(textfont, "A - Reset Launch", True, self.black, None), (530,30))
        window.blit(pygame.font.Font.render(textfont, "ESC - Return to Menu", True, self.black, None), (530,50))
    
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

def plot(x,y): # temp
    plt.plot(x,y)
    plt.savefig("saves/xy.png")
    plt.close()
    plt.plot(c.time,c.velocities)
    plt.savefig("saves/veloctime.png")

class Loop:
    def __init__(self) -> None:
        self.units_type, self.units, self.object, self.acceleration, self.scale = load_settings()
        self.back = False

    def calculations(self,mouse_x,mouse_y):
        len_y = b.ball.y-mouse_y
        len_x = mouse_x-(b.ball.x+10)
        g.draw_rect()
        g.draw_line(mouse_x,mouse_y)
        v_distance, h_distance = c.distance(len_y,len_x)
        angle, self.back = c.angle(self.back,len_x,len_y)
        power = c.power()
        v_velocity, h_velocity = c.velocity(angle,power)
        return len_x,len_y,angle,v_velocity,h_velocity
    
    def launch(self,v_velocity,h_velocity,angle,len_x,len_y):
        c.new_x = b.ball.x
        c.new_y = b.ball.y
        i = 0
        #x,y,h_max = c.trajectory(v_velocity,h_velocity,angle)
        while pygame.Rect.contains(ground,b.ball) == False and i < 100:
            i = c.movement(h_velocity,v_velocity,angle,len_x,len_y,i,h_max)
            i+=1
        b.ball = pygame.Rect(c.new_x,c.new_y-10,10,10)
        plot(c.x2,c.y2)
        pygame.draw.rect(window,g.black,b.ball)
        c.down = False

    def mainloop(self): #1m = 38.3333333333 px 500 scale
        pygame.init()
        run = True
        mouse_x = width/2
        mouse_y = height/2
        button_pressed = None
        while run:
            time_delta = clock.tick(60)/1000.0
            window.fill(g.grey)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    file = open("arrays.txt","w")
                    for i in range(len(c.x)):
                        file.write(str(c.x[i]) + "\n")
                    file.write("\n")
                    for i in range(len(c.y)):
                        file.write(str(c.y[i]) + "\n")
                    file.close()
                    run = False
            mouse_x,mouse_y = b.controls(mouse_x,mouse_y)
            len_x,len_y,angle,v_velocity,h_velocity = self.calculations(mouse_x,mouse_y)
            g.draw_text(v_velocity,h_velocity,angle,len_x,len_y)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                run = False
            if keys[pygame.K_SPACE]:
                self.launch(v_velocity,h_velocity,angle,len_x,len_y)
            if keys[pygame.K_a]:
                b.reset()
            manager.update(time_delta)
            manager.draw_ui(window)
            pygame.display.update()
            clock.tick(fps)
        return True


b = Ball()
g = Graphics()
c = Calculations()
l = Loop()

def start():
    global units_type,units,object,acceleration,scale
    end = False
    units_type,units,object,acceleration,scale = load_settings()
    end = l.mainloop()
    return end