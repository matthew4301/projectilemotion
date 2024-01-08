import pygame
import pygame_gui
import math
# not working for menu
pygame.freetype.init()
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
        pass

    def velocity(self,v_distance,h_distance): # wrong way round?
        try:
            v_velocity = round(math.sqrt(2*acceleration*v_distance),2)
        except ValueError:
            v_velocity = 0
        try:
            h_velocity = round(math.sqrt(2*acceleration*h_distance),2)
        except ValueError:
            h_velocity = 0
        return v_velocity,h_velocity
    
    def distance(self,len_x,len_y):
        h_distance = len_x*10 # depending on scale
        v_distance = len_y*10
        return h_distance,v_distance
    
    def angle(self,back,len_x,len_y):
        try:
            angle = math.degrees(math.atan(len_y/len_x))
            if angle < 0:
                back = True
        except ZeroDivisionError:
            angle = 90
        return angle,back
    
class Graphics:
    def __init__(self) -> None:
        self.font = pygame.font.SysFont("Arial", 30, False)
        self.bounds = pygame.Rect(0,0,width,height)
        self.launch = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((690,10),(100,50)), text="Launch", manager=manager)
        self.reset_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((690,70),(100,50)), text="Reset", manager=manager)
        self.menu = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((690,130), (100,50)), text="Main Menu", manager=manager)
        self.reset_var = False
        self.launch_var = False
        self.white = (255,255,255)
        self.green = (0,100,0)
        self.red = (255,0,0)
        self.black = (0,0,0)

    def draw(self,mouse_x,mouse_y):
        pygame.draw.rect(window,self.green,ground)
        pygame.draw.rect(window,self.black,b.ball)
        pygame.draw.line(window,g.red,pygame.math.Vector2(b.ball.x+10,b.ball.y),pygame.math.Vector2(mouse_x,mouse_y),5)

    def text(self,v_velocity,h_velocity,angle):
        textfont = pygame.font.Font(None,40)
        window.blit(pygame.font.Font.render(textfont, f"Vertical Velocity: {round(v_velocity/50,2)}m/s", True, self.black, None), (2,40))
        window.blit(pygame.font.Font.render(textfont, f"Horizontal Velocity: {round(h_velocity/50,2)}m/s", True, self.black, None), (2,80))
        window.blit(pygame.font.Font.render(textfont, f"Angle: {round(angle,0)}°", True, self.black, None), (2,0))
        window.blit(pygame.font.Font.render(textfont, "1m", True, self.black, None), (5+scale,b.ball.y+10))

    def button_checkpressed(self,button):
        if button == self.launch:
            button_pressed = "launch"
            print("launch")
        if button == self.reset_button:
            button_pressed = "reset"
            print("reset")
        if button == self.menu:
            button_pressed = "menu"
            print("menu")
        return button_pressed
    
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

class Loop:
    def __init__(self) -> None:
        self.units_type, self.units, self.object, self.acceleration, self.scale = load_settings()
        self.back = False

    def calculations(self,mouse_x,mouse_y):
        len_y = mouse_y-b.ball.y
        len_x = mouse_x-(b.ball.x+10)
        g.draw(mouse_x,mouse_y)
        v_distance, h_distance = c.distance(len_x,len_y)
        angle, self.back = c.angle(self.back,len_x,len_y)
        v_velocity, h_velocity = c.velocity(v_distance,h_distance)
        return len_x,len_y,v_distance,h_distance,angle,v_velocity,h_velocity

    def mainloop(self):
        run = True
        mouse_x = width/2
        mouse_y = height/2
        while run:
            time_delta = clock.tick(60)/1000.0
            window.fill((207, 207, 207))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    button_pressed = g.button_checkpressed(event.ui_element)
            mouse_x,mouse_y = b.controls(mouse_x,mouse_y)
            len_x,len_y,v_distance,h_distance,angle,v_velocity,h_velocity = self.calculations(mouse_x,mouse_y)
            g.text(v_velocity,h_velocity,angle)
            manager.update(time_delta)
            manager.draw_ui(window)
            pygame.display.update()
            clock.tick(fps)
        #return True


pygame.init()
b = Ball()
g = Graphics()
c = Calculations()
l = Loop()


l.mainloop()