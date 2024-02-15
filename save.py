import pygame
import pygame_gui
import sqlite3
import re

pygame.freetype.init()
window_surface = pygame.display.set_mode((800, 600))
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#787878'))
black = (0, 0, 0)
manager = pygame_gui.UIManager((800, 600))

class Buttons(): # https://www.geeksforgeeks.org/how-to-create-a-text-input-box-with-pygame/
    def __init__(self) -> None:
        self.mainmenu = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 375), (250, 50)),text='Main Menu',manager=manager)

    def checkpressed(self,button):

        if button == self.mainmenu:
            return False

def menu(): # may not need
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
        window_surface.blit(font.render("Save", True, black, None),(350,75))
        pygame.display.update()
    return True

def save_progress(ID,QuestionsAnswered,CorrectQuestions): # need to pass values from questions.py
    with sqlite3.connect("saves/database.db") as db:
        cursor = db.cursor()
    cursor.execute("""
INSERT OR REPLACE INTO Progress(UserID,QuestionsAnswered,CorrectQuestions)
VALUES(?,?,?);""", [(ID), (QuestionsAnswered), (CorrectQuestions)])
    db.commit()
     
b = Buttons()