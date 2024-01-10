import pygame
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
        self.ball = pygame.Rect(5,ground.y-10,10,10)
    
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
    
class Calculations:
    def __init__(self) -> None:
        self.new_x = b.ball.x
        self.new_y = b.ball.y
        self.x = []
        self.y = []
        self.velocities = []
        self.time = []
        self.duration = 0

    def velocity(self,v_distance,h_distance):
        try:
            v_velocity = round(math.sqrt(2*float(acceleration)*v_distance),2)
        except ValueError:
            v_velocity = 0
        try:
            h_velocity = round(math.sqrt(2*float(acceleration)*h_distance),2)
        except ValueError:
            h_velocity = 0
        return v_velocity,h_velocity
    
    def distance(self,len_x,len_y):
        h_distance = len_x/int(scale) # depending on scale
        v_distance = len_y/int(scale)
        return h_distance,v_distance
    
    def angle(self,back,len_x,len_y):
        try:
            angle = math.degrees(math.atan(len_y/len_x))
            if angle < 0:
                back = True
        except ZeroDivisionError:
            angle = 90
        return angle,back
    
    def trajectory(self,v_velocity,h_velocity,angle):
        y0=100
        mag = math.sqrt(v_velocity**2+h_velocity**2)       
        b=-2*mag*math.sin(angle)
        c=-2*y0
        coeff=plb.array([float(acceleration),b,c])
        t1,t2=plb.roots(coeff)
        h1=mag**2*(math.sin(angle))**2/(2*float(acceleration))
        h_max=h1*10+y0
        R=mag*math.cos(angle)*plb.max(t1,t2)
        self.x=plb.linspace(0,R,50)
        self.y=self.x*math.tan(angle)-(1/2)*(float(acceleration)*self.x**2)/(mag**2*(math.cos(angle))**2)
        return self.x, self.y, h_max
    
    def movement(self,h_velocity,v_velocity,angle,len_x,len_y,i,h_max,down): # backwards???
        mag_velocity = math.sqrt(v_velocity**2+h_velocity**2)*10
        if self.x[i] < 0:
            self.new_x = (b.ball.x+self.x[i])*-1 # *int(scale)
        else:
            self.new_x = b.ball.x+self.x[i]
        self.new_y = b.ball.y-self.y[i] # *int(scale)
        if self.new_y <= height-h_max:
            down = True
        if down == True:
            self.velocities.append(-mag_velocity)
        else:
            self.velocities.append(mag_velocity)
        self.time.append(self.duration)
        self.duration+=0.05
        t.sleep(0.05)
        b.ball = pygame.Rect(self.new_x,self.new_y,10,10)
        window.fill(g.grey)
        g.draw_rect()
        g.draw_text(v_velocity,h_velocity,angle,len_x,len_y)
        pygame.draw.rect(window,g.black,b.ball)
        pygame.display.flip()
        clock.tick(fps)
        i+=1
        return i,down

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
        window.blit(pygame.font.Font.render(textfont, f"{len_x}, {len_y}", True, self.black, None), (2,120))
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
        v_velocity, h_velocity = c.velocity(v_distance,h_distance)
        return len_x,len_y,v_distance,h_distance,angle,v_velocity,h_velocity
    
    def launch(self,v_velocity,h_velocity,angle,len_x,len_y):
        i = 0
        down = False
        x,y,h_max = c.trajectory(v_velocity,h_velocity,angle)
        while pygame.Rect.contains(ground,b.ball) == False and i <= 50:
            i,down = c.movement(h_velocity,v_velocity,angle,len_x,len_y,i,h_max,down)
            i+=1
        b.ball = pygame.Rect(c.new_x,c.new_y-10,10,10)
        pygame.draw.rect(window,g.black,b.ball)
        #plot(x,y)

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
                    file = open("temp/arrays.txt","w")
                    for i in range(len(c.x)):
                        file.write(str(c.x[i]) + "\n")
                    file.write("\n")
                    for i in range(len(c.y)):
                        file.write(str(c.y[i]) + "\n")
                    file.close()
                    run = False
            mouse_x,mouse_y = b.controls(mouse_x,mouse_y)
            len_x,len_y,v_distance,h_distance,angle,v_velocity,h_velocity = self.calculations(mouse_x,mouse_y)
            g.draw_text(v_velocity,h_velocity,angle,len_x,len_y)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                run = False
            if keys[pygame.K_SPACE]:
                self.launch(v_velocity,h_velocity,angle,len_x,len_y)
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