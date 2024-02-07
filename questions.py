import pygame
import pygame_gui
import pygame.freetype
import sqlite3
import random

pygame.init()
pygame.freetype.init()
pygame.display.set_caption('Projectile Motion Simulator')
window_surface = pygame.display.set_mode((800,600))
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#787878'))
black = (0, 0, 0)
font = pygame.font.SysFont("Comic Sans MS", 40)
font2 = pygame.font.SysFont("Comic Sans MS", 15)
manager = pygame_gui.UIManager((800, 600))

questions = []
answers = []

class Buttons():
    def __init__(self):
        self.quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 475), (250, 75)),text='Quit',manager=manager)
        self.start = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 400), (250, 75)),text='Start Questions',manager=manager)
        self.textinput = pygame_textinput.TextInputVisualizer()
    def checkpressed(self,button):
        if button == self.quit:
            return False
        if button == self.start:
            window_surface.blit(b.textinput.surface, (10,300))
            return True, find_question()

def load_db():
    with sqlite3.connect("saves/database.db") as db:
        cursor = db.cursor()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS Questions(
QuestionID INTEGER PRIMARY KEY,
Answer TEXT NOT NULL,
Question FLOAT NOT NULL);''')
    db.commit()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS Progress(
UserID INTEGER PRIMARY KEY,
QuestionsAnswered INTEGER NOT NULL,
CorrectQuestions INTEGER NOT NULL);''')
    db.commit()
    for i in range(len(questions)):
        cursor.execute('''
INSERT INTO Questions(QuestionID,Question,Answer)
VALUES(?,?,?)
ON CONFLICT DO NOTHING;''', [(i), (questions[i]), (answers[i])])
        db.commit()
     
def load_questiontxt():
    with open("saves/questions.txt") as file:
        list = [line.strip() for line in file.readlines()]
    for i in range(len(list)):
        if i % 2 == 0:
            questions.append(list[i])
        else:
            answers.append(list[i])

def select_randomquestion():
    range = len(questions)-1
    return random.randint(0,range)

def find_question():
    with sqlite3.connect("saves/database.db") as db:
        cursor = db.cursor()
    cursor.execute("""
SELECT Question
FROM Questions
WHERE QuestionID = ?;
""",[(select_randomquestion())])
    question = str(cursor.fetchall())
    question.replace('[','')
    question.replace(']','')
    return question

def start():
    load_questiontxt()
    load_db()
    clock = pygame.time.Clock()
    is_running = True
    question = ""
    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                is_running,question = b.checkpressed(event.ui_element)
        manager.update(time_delta)
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)
        window_surface.blit(font.render("Questions", True, black, None),(300,75))
        window_surface.blit(font2.render(str(question), True, black, None),(10,150))
        pygame.display.update()
    return True

b = Buttons()