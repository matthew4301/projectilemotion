import pygame
import pygame_gui

window_surface = pygame.display.set_mode((800, 600))
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#787878'))
black = (0, 0, 0)
font = pygame.font.Font(None, 40)
font2 = pygame.font.Font(None, 20)
manager = pygame_gui.UIManager((800, 600))

questions = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 175), (250, 50)),text='Questions',manager=manager)
tutorial = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 225), (250, 50)),text='Tutorial',manager=manager)
load = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 275), (250, 50)),text='Load Progress',manager=manager)
settings = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 325), (250, 50)),text='Settings',manager=manager)
mainmenu = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 375), (250, 50)),text='Main Menu',manager=manager)

def menu(gcse):
    is_running = True
    clock = pygame.time.Clock()
    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            manager.process_events(event)
        manager.update(time_delta)
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)
        if gcse == True:
            window_surface.blit(font.render("Teaching GCSE", True, black, None),(250,75))
        else:
            window_surface.blit(font.render("Teaching A-Level", True, black, None),(250,75))
        pygame.display.update()


def checkpressed(button):
    if button == questions:
        pass
    if button == tutorial:
        pass
    if button == load:
        pass
    if button == settings:
        pass
    if button == mainmenu:
        pass