import pygame
import pygame_gui
import pygame.freetype
import sqlite3
import random
import re

pygame.init()
pygame.freetype.init()
pygame.display.set_caption('Projectile Motion Simulator')
window_surface = pygame.display.set_mode((800,600))
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#787878'))
black = (0, 0, 0)
font = pygame.font.SysFont("Comic Sans MS", 40)
font2 = pygame.font.SysFont("Comic Sans MS", 12)
manager = pygame_gui.UIManager((800, 600))

questions = []
answers = []

class Buttons():
    def __init__(self):
        self.quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((25, 500), (250, 75)),text='Quit',manager=manager)
        self.start = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 500), (250, 75)),text='Start Questions',manager=manager)
        
    def show_choices(self,a,b,c,d):
        self.a_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 250), (250, 50)),text=a,manager=manager)
        self.b_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 300), (250, 50)),text=b,manager=manager)
        self.c_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 350), (250, 50)),text=c,manager=manager)
        self.d_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 400), (250, 50)),text=d,manager=manager)

    def checkpressed(self,button,correct_button):
        try:
            if button == self.a_button:
                if correct_button == "a":
                    print("correct")
                else:
                    print("false")
            if button == self.b_button:
                if correct_button == "b":
                    print("correct")
                else:
                    print("false")
            if button == self.c_button:
                if correct_button == "c":
                    print("correct")
                else:
                    print("false")
            if button == self.d_button:
                if correct_button == "d":
                    print("correct")
                else:
                    print("false")
        except AttributeError:
            pass
        if button == self.quit:
            return False, "", ""
        if button == self.start:
            question,correct_button = find_question()
            return True, question, correct_button
        else:
            return True, "", ""

def load_db():
    with sqlite3.connect("saves/database.db") as db:
        cursor = db.cursor()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS Questions(
QuestionID INTEGER PRIMARY KEY,
Answer1 TEXT NOT NULL,
Answer2 TEXT NOT NULL,
Answer3 TEXT NOT NULL,
Answer4 TEXT NOT NULL,
Question FLOAT NOT NULL);''')
    db.commit()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS Progress(
UserID INTEGER PRIMARY KEY,
QuestionsAnswered INTEGER NOT NULL,
CorrectQuestions INTEGER NOT NULL);''')
    db.commit()
    for i in range(0,5,len(questions)):
        cursor.execute('''
INSERT INTO Questions(QuestionID,Question,Answer1,Answer2,Answer3,Answer4)
VALUES(?,?,?,?,?,?)
ON CONFLICT DO NOTHING;''', [(i), (questions[i]), (answers[i]), (answers[i+1]), (answers[i+2]), (answers[i+3])])
        db.commit()
     
def load_questiontxt():
    with open("saves/questions.txt") as file:
        list = [line.strip() for line in file.readlines()]
    for i in range(len(list)):
        if i % 5 == 0:
            questions.append(list[i])
        else:
            answers.append(list[i])

def split_multichoice(ID): # Answer1 is always correct in db
    with sqlite3.connect("saves/database.db") as db:
        cursor = db.cursor()
    cursor.execute("""
SELECT Answer1,Answer2,Answer3,Answer4
FROM Questions
Where QuestionID = ?;""", [(ID)])
    ans = [*re.sub("[()',]",'',str(cursor.fetchall()))]
    ans.pop(0)
    ans.pop(len(ans)-1)
    return ans

def find_correctans(ID):
    with sqlite3.connect("saves/database.db") as db:
        cursor = db.cursor()
    cursor.execute("""
SELECT Answer1
FROM Questions
Where QuestionID = ?;""", [(ID)])
    return str(cursor.fetchall())
    
def shuffle_ans(ans):
    random.shuffle(ans)
    return ans

def show_choices(ans,correct_ans):
    try:
        if ans[0] == correct_ans:
            correct_button = "a"
        elif ans[1] == correct_ans:
            correct_button = "b"
        elif ans[2] == correct_ans:
            correct_button = "c"
        elif ans[3] == correct_ans:
            correct_button = "d"
        b.show_choices(ans[0],ans[1],ans[2],ans[3])
        return correct_button
    except TypeError:
        pass

def select_randomquestion():
    range = len(questions)-1
    return random.randint(0,range)

def find_question():
    with sqlite3.connect("saves/database.db") as db:
        cursor = db.cursor()
    ID = select_randomquestion()
    ans = split_multichoice(ID)
    cursor.execute("""
SELECT Question
FROM Questions
WHERE QuestionID = ?;
""",[(ID)])
    correct_ans = find_correctans(ID)
    print(ans)
    ans = shuffle_ans(ans)
    print(ans)
    correct_button = show_choices(ans,correct_ans)
    question = re.sub("[()',]",'',str(cursor.fetchall()))
    return question,correct_button

def start():
    load_questiontxt()
    load_db()
    clock = pygame.time.Clock()
    is_running = True
    correct_button = ""
    question = ""
    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                is_running,question,correct_button = b.checkpressed(event.ui_element,correct_button)
        manager.update(time_delta)
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)
        window_surface.blit(font.render("Questions", True, black, None),(300,25))
        window_surface.blit(font2.render(str(question), True, black, None),(10,150))
        pygame.display.update()
    return True

b = Buttons()