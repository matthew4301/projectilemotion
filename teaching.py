import pygame
import pygame_gui

def start():
    pygame.init()
    pygame.display.set_caption('Projectile Motion Simulator')
    window_surface = pygame.display.set_mode((800, 600))
    background = pygame.Surface((800, 600))
    background.fill(pygame.Color('#787878'))
    black = (0, 0, 0)
    font = pygame.font.SysFont("Comic Sans MS", 40, False)
    font2 = pygame.font.SysFont("Comic Sans MS", 20, False)
    manager = pygame_gui.UIManager((800, 600))

    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            #if event.type == pygame_gui.UI_BUTTON_PRESSED:
            #    event = b.checkpressed(event.ui_element)
            manager.process_events(event)
        manager.update(time_delta)
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)
        window_surface.blit(font.render("Teaching", True, black, None),(150,75))
        pygame.display.update()