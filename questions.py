import pygame
import pygame_gui
import pygame.freetype
import math
import sqlite3

pygame.init()
pygame.freetype.init()
pygame.display.set_caption('Projectile Motion Simulator')
window_surface = pygame.display.set_mode((800,600))
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#787878'))
black = (0, 0, 0)
font = pygame.font.SysFont("Comic Sans MS", 40)
manager = pygame_gui.UIManager((800, 600))

questions = []
answers = []

def load_db():
    with sqlite3.connect("saves/database.db") as db:
        cursor = db.cursor()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS Questions(
QuestionID INTEGER PRIMARY KEY,
Question TEXT NOT NULL,
Answer FLOAT NOT NULL);''')
    db.commit()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS Progress(
UserID INTEGER PRIMARY KEY,
QuestionsAnswered INTEGER NOT NULL);''')
    db.commit()
    cursor.execute(f'''
INSERT INTO Questions(QuestionID,Question,Answer)
VALUES(0,{questions[0]},{answers[0]}),
(1,{questions[1]},{answers[1]}),
(2,{questions[2]},{answers[2]}),
(3,{questions[3]},{answers[3]}),
(4,{questions[4]},{answers[4]}),
(5,{questions[5]},{answers[5]}),
(6,{questions[6]},{answers[6]}),
(7,{questions[7]},{answers[7]});''')
    db.commit()
     
def load_questiontxt():
    with open("saves/questions.txt") as file:
        list = file.readlines()
    for i in range(len(list)):
        if i % 2 == 0:
            answers.append(list[i])
            print(list[i])
        else:
            questions.append(list[i])
            print(list[i])

def start():
    load_questiontxt()
    load_db()
    clock = pygame.time.Clock()
    is_running = True
    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
        manager.update(time_delta)
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)
        window_surface.blit(font.render("Questions", True, black, None),(150,75))
        pygame.display.update()