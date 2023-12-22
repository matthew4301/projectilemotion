import pygame
import pygame_gui
import projectile_simulator
import teaching
from sys import exit

pygame.init()
pygame.display.set_caption('Projectile Motion Simulator')
window_surface = pygame.display.set_mode((800, 600))
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#787878'))
black = (0, 0, 0)
font = pygame.font.SysFont("Comic Sans MS", 40, False)
font2 = pygame.font.SysFont("Comic Sans MS", 20, False)
manager = pygame_gui.UIManager((800, 600))

class Buttons:
    def __init__(self):
        self.gcse = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 175), (250, 50)),text='Start As GCSE',manager=manager)
        self.alevel = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 225), (250, 50)),text='Start As A-Level',manager=manager)
        self.sandbox = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 275), (250, 50)),text='Sandbox Mode',manager=manager)
        self.load = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 325), (250, 50)),text='Load',manager=manager)
        self.settings = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 375), (250, 50)),text='Settings',manager=manager)
        self.quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 425), (250, 50)),text='Quit',manager=manager)

    def checkpressed(self,button):
        if button == self.gcse or button == self.alevel:
            teaching.start()
        if button == self.sandbox:
            projectile_simulator.start()
        if button == self.load:
            print("load")
        if button == self.settings:
            print("settings")
        if button == self.quit:
            pygame.quit()
            exit()

class Teaching:
    def __init__(self):
        pass
    
    def menu(self,button):
        window_surface.blit(background, (0, 0))
        window_surface.blit(font.render("Teaching", True, black, None),(150,75))
        if button == b.gcse:
            window_surface.blit(font2.render("GCSE", True, black, None),(150,125))
        if button == b.alevel:
            window_surface.blit(font2.render("A-Level", True, black, None),(150,125))

clock = pygame.time.Clock()
is_running = True
b = Buttons()

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            b.checkpressed(event.ui_element)
        manager.process_events(event)
    manager.update(time_delta)
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    window_surface.blit(font.render("Projectile Motion Simulator", True, black, None),(150,75))
    pygame.display.update()

