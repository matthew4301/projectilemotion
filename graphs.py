import pygame
import pygame_gui

pygame.freetype.init()
window_surface = pygame.display.set_mode((800, 600))
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#FFFFFF'))
black = (0, 0, 0)
manager = pygame_gui.UIManager((800, 600))

class Buttons():
    def __init__(self) -> None:
        self.mainmenu = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 525), (250, 50)),text='Back to simulator',manager=manager)

    def checkpressed(self,button):
        if button == self.mainmenu:
            return False

def menu():
    veltime_img = pygame.image.load("saves/vel_time.png").convert()
    veltime_img = pygame.transform.scale(veltime_img,(400,300))
    acceltime_img = pygame.image.load("saves/accel_time.png").convert()
    acceltime_img = pygame.transform.scale(acceltime_img,(400,300))
    displtime_img = pygame.image.load("saves/displ_time.png").convert()
    displtime_img = pygame.transform.scale(displtime_img,(400,300))
    pygame.init()
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
        window_surface.blit(background, (0, 200))
        manager.draw_ui(window_surface)
        window_surface.blit(veltime_img, (0,0))
        window_surface.blit(acceltime_img, (400,0))
        window_surface.blit(displtime_img, (0,300))
        pygame.display.update()
    return True
     
b = Buttons()