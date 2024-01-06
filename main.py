import pygame
import pygame_gui
import projectile_simulator
import teach
import settings
import load
from sys import exit

pygame.init()
pygame.freetype.init()
pygame.display.set_caption('Projectile Motion Simulator')
window_surface = pygame.display.set_mode((800, 600))
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#787878'))
black = (0, 0, 0)
font = pygame.font.SysFont("Comic Sans MS", 40)
font2 = pygame.font.SysFont("Comic Sans MS", 20)
manager = pygame_gui.UIManager((800, 600))

class Buttons():
    def __init__(self):
        self.gcse = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 175), (250, 50)),text='Start As GCSE',manager=manager)
        self.alevel = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 225), (250, 50)),text='Start As A-Level',manager=manager)
        self.sandbox = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 275), (250, 50)),text='Sandbox Mode',manager=manager)
        self.load = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 325), (250, 50)),text='Load',manager=manager)
        self.settings = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 375), (250, 50)),text='Settings',manager=manager)
        self.quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 425), (250, 50)),text='Quit',manager=manager)
        self.finished = False
        self.teachfinished = False

    def checkpressed(self,button):
        if button == self.gcse:
            self.teachfinished = teach.menu(True)
        if button == self.alevel:
            self.teachfinished = teach.menu(False)
        if button == self.sandbox:
            self.finished = projectile_simulator.mainloop()
        if button == self.load:
            self.loadfinished = load.menu()
        if button == self.settings:
            self.settingsfinished = settings.menu()
        if button == self.quit:
            pygame.quit()
            exit()

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
    if b.finished == True:
        pygame.init()
        b.finished = False
    if b.teachfinished == True:
        pygame.init()
        b.teachfinished = False
    manager.update(time_delta)
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    window_surface.blit(font.render("Projectile Motion Simulator", True, black, None),(150,75))
    pygame.display.update()

pygame.quit()