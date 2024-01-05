import pygame
import pygame.freetype
import pygame_gui
from sys import exit

pygame.freetype.init()
window_surface = pygame.display.set_mode((800, 600))
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#787878'))
black = (0, 0, 0)
manager = pygame_gui.UIManager((800, 600))

class Buttons():
    def __init__(self) -> None:
        self.questions = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 175), (250, 50)),text='Questions',manager=manager)
        self.tutorial = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 225), (250, 50)),text='Tutorial',manager=manager)
        self.load = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 275), (250, 50)),text='Load Progress',manager=manager)
        self.settings = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 325), (250, 50)),text='Settings',manager=manager)
        self.mainmenu = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 375), (250, 50)),text='Main Menu',manager=manager)

    def checkpressed(self,button):
        if button == self.questions:
            pass
        if button == self.tutorial:
            pass
        if button == self.load:
            pass
        if button == self.settings:
            pass
        if button == self.mainmenu:
            return False

def menu(gcse):
    pygame.init()
    font = pygame.font.SysFont("Comic Sans MS", 40)
    clock = pygame.time.Clock()
    is_running = True
    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                is_running = b.checkpressed(event.ui_element)
        manager.update(time_delta)
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)
        if gcse == True:
            window_surface.blit(font.render("Teaching GCSE", True, black, None),(250,75))
        else:
            window_surface.blit(font.render("Teaching A-Level", True, black, None),(250,75))
        pygame.display.update()
    return True

b = Buttons()