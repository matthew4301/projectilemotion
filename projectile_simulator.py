import pygame
import math
import time as t

height = 800   
width = 600

green = (0,100,0)
pygame.init()
window = pygame.display.set_mode((height,width))
pygame.display.set_caption('Projectile Motion')
ground = pygame.Rect(0,500,800,100)
textfont = pygame.font.Font(None,30)

# default settings state
units_type = "Metric"
units = "M"
object = "Ball"
acceleration = 9.81
scale = 50

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

class ball():
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, window):
        pygame.draw.circle(window, (0,0,0), (self.x,self.y), self.radius)
        pygame.draw.circle(window, self.color, (self.x,self.y), self.radius-1)
        pygame.draw.rect(window,green,ground)

    def ballPath(start_x,start_y,power,angle,time):
        vel_x = (math.cos(angle) * power)/int(scale)
        vel_y = (math.sin(angle) * power)/int(scale)
        dist_x = vel_x * time
        dist_y = (vel_y * time) + ((-4.9 * (time ** 2)) / 2)
        new_x = round(dist_x + start_x)
        new_y = round(start_y - dist_y)
        return (new_x, new_y),(vel_x, vel_y)
    
    def bounds_rect(self):
        if Ball.y > 600:
            Ball.y = 590
        if Ball.y < 0:
            Ball.y = 10
        if Ball.x > 800:
            Ball.x = 790
        if Ball.x < 0:
            Ball.x = 10

def findAngle(pos):
    sX = Ball.x
    sY = Ball.y
    try:
        angle = math.atan((sY - pos[1]) / (sX - pos[0]))
    except:
        angle = math.pi / 2
    if pos[1] < sY and pos[0] > sX:
        angle = abs(angle)
    elif pos[1] < sY and pos[0] < sX:
        angle = math.pi - angle
    elif pos[1] > sY and pos[0] < sX:
        angle = math.pi + abs(angle)
    elif pos[1] > sY and pos[0] > sX:
        angle = (math.pi * 2) - angle
    return angle

Ball = ball(15,494,5,(255,255,255))

def mainloop():
    run = True
    time = 0
    power = 0
    angle = 0
    vel_x = 0
    vel_y = 0
    shoot = False
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        if shoot:
            if Ball.y > 494:
                Ball.y = 499
                time = 0
                shoot = False
            time += 0.1
            po, vel = ball.ballPath(x, y, power, angle, time)
            Ball.x = po[0]
            Ball.y = po[1]
            vel_x = vel[0]
            vel_y = vel[1]
            ball.bounds_rect(Ball)
        line = [(Ball.x, Ball.y), pygame.mouse.get_pos()]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not shoot:
                    x = Ball.x
                    y = Ball.y
                    pos = pygame.mouse.get_pos()
                    shoot = True
                    power = math.sqrt((line[1][1]-line[0][1])**2 +(line[1][0]-line[0][1])**2)*int(scale)
                    angle = findAngle(pos)
        window.fill((207,207,207))
        Ball.draw(window)
        if shoot == False:
            pygame.draw.line(window, (0,0,0),line[0], line[1])
        pygame.draw.rect(window,green,ground)
        window.blit(pygame.font.Font.render(textfont, f"Angle: {round(math.degrees(angle),0)}°", True, (0,0,0), None), (2,0))
        window.blit(pygame.font.Font.render(textfont, f"Vertical Velocity: {round(vel_y,2)}m/s", True, (0,0,0), None), (2,20))
        window.blit(pygame.font.Font.render(textfont, f"Horizontal Velocity: {round(vel_x,2)}m/s", True, (0,0,0), None), (2,40))
        window.blit(pygame.font.Font.render(textfont, f"Time: {round(time,2)}s", True, (0,0,0), None), (2,60))
        mousex,mousey = pygame.mouse.get_pos()
        window.blit(pygame.font.Font.render(textfont, f"{mousex}, {mousey}", True, (0,0,0), None), (2,80))
        pygame.display.update()
    return True

units_type,units,object,acceleration,scale = load_settings()