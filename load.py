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

class Inputs():
    def __init__(self) -> None:
        self.mainmenu = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 475), (250, 50)),text='Back',manager=manager)
        self.input_rect = pygame.Rect(300, 150, 140, 32) 

    def checkpressed(self,button):

        if button == self.mainmenu:
            return False

def menu():
    pygame.init()
    text = ""
    font = pygame.font.SysFont("Comic Sans MS", 40)
    font2 = pygame.font.SysFont("Comic Sans MS", 20)
    clock = pygame.time.Clock()
    is_running = True
    answered = None
    correct = None
    usernames = get_usernames(usernames)
    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                is_running = i.checkpressed(event.ui_element)
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_BACKSPACE: 
                    text = text[:-1] 
                if event.key == pygame.K_RETURN:
                    valid = check_username(text,usernames)
                    if valid:
                        answered,correct = get_stats(text)
                else: 
                    text+=event.unicode
        manager.update(time_delta)
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)
        window_surface.blit(font.render("Load", True, black, None),(350,25))
        window_surface.blit(font2.render("Enter your username: ", True, black, None),(50,150))
        window_surface.blit(font2.render(answered, True, black, None),(50,250))
        window_surface.blit(font2.render(correct, True, black, None),(50,350))
        text_surface = font2.render(text, True, (255, 255, 255)) 
        i.input_rect.w = max(100, text_surface.get_width()+10) 
        pygame.draw.rect(window_surface, black, i.input_rect) 
        window_surface.blit(text_surface,(i.input_rect.x, i.input_rect.y))
        pygame.display.update()
    return True

def load_db():
	with sqlite3.connect("saves/database.db") as db:
		cursor = db.cursor()
	cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
userID INTEGER PRIMARY KEY,
username TEXT);''')
	db.commit()

def check_username(userinput,usernames):
    if userinput in usernames:
        return True
    else:
        return False
     
def get_usernames(usernames):
    with sqlite3.connect("saves/database.db") as db:
        cursor = db.cursor()
    cursor.execute("""
SELECT count(*)
FROM users;""")
    result = cursor.fetchall()
    n = result[0][0]
    for i in range(n):
        cursor.execute("""
SELECT username
FROM users
WHERE userID = ?;""", [(i)])
        usernames.append(re.sub("['',()]", "", str(cursor.fetchone())))
    return usernames

def get_stats(userinput):
    with sqlite3.connect("saves/database.db") as db:
        cursor = db.cursor()
    cursor.execute("""
SELECT userID
FROM users
WHERE username = ?;""", [(userinput)])
    id = re.sub("['',()]", "", str(cursor.fetchone()))
    cursor.execute("""
SELECT QuestionsAnswered,CorrectQuestions
FROM Progress
WHERE userID = ?;""", [(id)])
    stats = cursor.fetchall()
    answered = stats[0][0]
    correct = stats[0][1]
    return answered,correct
     
i = Inputs()