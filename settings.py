import pygame
import pygame_gui

pygame.freetype.init()
window_surface = pygame.display.set_mode((800, 600))
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#787878'))
black = (0, 0, 0)
manager = pygame_gui.UIManager((800, 600))

class Save:
    def __init__(self) -> None:
        self.units_type = "Metric" 
        self.units = "M"
        self.object = "Ball"
        self.acceleration = 9.81
        self.scale = 50

    def save(self): # order: type, units, object, accel, scale
        file = open("saves/settings.txt", "w")
        file.write(f"{self.units_type}\n{self.units}\n{self.object}\n{self.acceleration}\n{self.scale}")
        file.close()

    def load(self):
        try:
            with open("saves/settings.txt") as f:
                settings_list = f.read().splitlines()
            print(settings_list)
            self.units_type = settings_list[0]
            self.units = settings_list[1]
            self.object = settings_list[2]
            self.acceleration = settings_list[3]
            self.scale = settings_list[4]
        except IndexError:
            pass            

class Buttons:
    def __init__(self) -> None:
        self.metric = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((25, 125), (150, 50)),text='Metric',manager=manager)
        self.imperial = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((225, 125), (150, 50)),text='Imperial',manager=manager)
        self.cm = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((25, 225), (150, 50)),text='Centimeters',manager=manager)
        self.meters = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((25, 275), (150, 50)),text='Meters',manager=manager)
        self.km = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((25, 325), (150, 50)),text='Kilometers',manager=manager)
        self.inch = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((225, 225), (150, 50)),text='Inches',manager=manager)
        self.ft = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((225, 275), (150, 50)),text='Feet',manager=manager)
        self.miles = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((225, 325), (150, 50)),text='Miles',manager=manager)
        self.ball = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((25, 425), (150, 50)),text='Ball',manager=manager)
        self.rocket = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((225, 425), (150, 50)),text='Rocket',manager=manager)
        self.gravity = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((475, 225), (250, 50)),text='Set to Gravity (9.81)',manager=manager)
        self.acceleration_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((475, 175), (250,25)), start_value=9.81, value_range=(1,20),manager=manager)
        self.scale_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((475, 375), (250,25)), start_value=50, value_range=(1,100),manager=manager)
        self.mainmenu = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((270, 500), (250, 50)),text='Main Menu',manager=manager)

    def checkpressed(self,button):
        if button == self.mainmenu:
            return False
        if button == self.metric:
            s.units_type = "Metric"
        if button == self.imperial:
            s.units_type = "Imperial"
        if button == self.cm:
            s.units = "CM"
        if button == self.meters:
            s.units = "M"
        if button == self.km:
            s.units = "KM"
        if button == self.inch:
            s.units = "IN"
        if button == self.ft:
            s.units = "FT"
        if button == self.miles:
            s.units = "MI"
        if button == self.ball:
            s.object = "Ball"
        if button == self.rocket:
            s.object = "Rocket"
        if button == self.gravity:
            s.acceleration = 9.81
        s.save()

def menu():
    pygame.init()
    s.load()
    font = pygame.font.SysFont("Comic Sans MS", 40)
    font2 = pygame.font.SysFont("Comic Sans MS", 30)
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
        acceleration = str(round(b.acceleration_slider.get_current_value(),2))
        scale = str(round(b.scale_slider.get_current_value(),0))
        s.acceleration = acceleration
        s.scale = scale
        window_surface.blit(font.render("Settings", True, black, None),(320,15))
        window_surface.blit(font2.render("Units", True, black, None),(25,75))
        window_surface.blit(font2.render("Distance Unit", True, black, None),(25,175))
        window_surface.blit(font2.render("Object", True, black, None),(25,375))
        window_surface.blit(font2.render(f"Scale - {scale}", True, black, None),(475,325))
        window_surface.blit(font2.render(f"Acceleration - {acceleration}", True, black, None),(475,125))
        pygame.display.update()
    return True

b = Buttons()
s = Save()