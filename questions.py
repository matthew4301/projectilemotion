import pygame
import pygame_gui
import pygame.freetype
import sqlite3
import random
import re
import save
import load

pygame.init()
pygame.freetype.init()
pygame.display.set_caption('Projectile Motion Simulator')
window_surface = pygame.display.set_mode((800,600))
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#787878'))
black = (0, 0, 0)
font = pygame.font.SysFont("Comic Sans MS", 40)
font2 = pygame.font.SysFont("Comic Sans MS", 13)
font3 = pygame.font.SysFont("Comic Sans MS", 30)
manager = pygame_gui.UIManager((800, 600))

questions = []
answers = []

class Inputs():
    def __init__(self):
        self.quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((25, 500), (250, 75)),text='Quit',manager=manager)
        self.save = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 500), (250, 75)),text='Save Progress',manager=manager)
        self.load = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((525, 500), (250, 75)),text='View Stats',manager=manager)
    
    def check_button(self,button,is_running,correct_questions,questions_answered):
        if button == self.quit:
            is_running = False
        if button == self.save:
            save.menu(correct_questions,questions_answered)
        if button == self.load:
            load.menu()
        return is_running
    
    def check_keyboard(self,correct_button,button_selected,correct_selectedbutton,correct_questions,questions_answered):
       keys = pygame.key.get_pressed()
       if keys[pygame.K_1]:
           button_selected = 1
       if keys[pygame.K_2]:
           button_selected = 2
       if keys[pygame.K_3]:
           button_selected = 3
       if keys[pygame.K_4]:
           button_selected = 4
       if button_selected == correct_button:
           correct_selectedbutton = True
           correct_questions+=1
           questions_answered+=1
       if (keys[pygame.K_1] or keys[pygame.K_2] or keys[pygame.K_3] or keys[pygame.K_4]) and button_selected != correct_button:
           correct_selectedbutton = False
           questions_answered+=1
       return correct_selectedbutton,correct_questions,questions_answered

def load_db():
    with sqlite3.connect("saves/database.db") as db:
        cursor = db.cursor()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS Questions(
QuestionID INTEGER PRIMARY KEY,
Question TEXT,
Answer1 FLOAT,
Answer2 FLOAT,
Answer3 FLOAT,
Answer4 FLOAT);''')
    db.commit()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS Progress(
UserID INTEGER PRIMARY KEY,
QuestionsAnswered INTEGER NOT NULL,
CorrectQuestions INTEGER NOT NULL);''')
    db.commit()
    n = 0
    m = 0
    while m < len(questions):
        cursor.execute('''
INSERT OR REPLACE INTO Questions(QuestionID,Question,Answer1,Answer2,Answer3,Answer4)
VALUES(?,?,?,?,?,?);''', [(m), (questions[m]), (answers[n]), (answers[n+1]), (answers[n+2]), (answers[n+3])])
        db.commit()
        m+=1
        n+=4
        
def load_questiontxt():
    with open("saves/questions.txt") as file:
        list = [line.strip() for line in file.readlines()]
    for i in range(len(list)):
        questions.append(list[i])

def load_answerstxt():
    with open("saves/answers.txt") as file:
        list = [line.strip() for line in file.readlines()]
    for i in range(len(list)):
        answers.append(list[i])

def update_questionsanswered(uID,answered):
    with sqlite3.connect("saves/database.db") as db:
        cursor = db.cursor()
    cursor.execute(f"""
INSERT OR REPLACE INTO Progress(UserID, QuestionsAnswered)
VALUES(?,?);""", [(uID),(answered)])
    db.commit()

def update_correctquestions(uID,correct_questions):
    with sqlite3.connect("saves/database.db") as db:
        cursor = db.cursor()
    cursor.execute(f"""
INSERT OR REPLACE INTO Progress(UserID, CorrectQuestions)
VALUES(?,?);""", [(uID),(correct_questions)])
    db.commit()

def split_multichoice(ID): # Answer1 is always correct in db
    ans = []
    with sqlite3.connect("saves/database.db") as db:
        cursor = db.cursor()
    for i in range(1,5):
        cursor.execute(f"""
    SELECT Answer{i}
    FROM Questions
    WHERE QuestionID = ?;""", [(ID)])
        ans.append(re.sub("['',()]","",str(cursor.fetchone())))
    return ans

def find_correctans(ID):
    with sqlite3.connect("saves/database.db") as db:
        cursor = db.cursor()
    cursor.execute("""
SELECT Answer1
FROM Questions
Where QuestionID = ?;""", [(ID)])
    result = re.sub("[()',]","",str(cursor.fetchone()))
    return result
    
def shuffle_ans(ans): # fisher-yates shuffle O(n)
    n = len(ans)
    for i in range(n-2):
        j = random.randint(0,i)
        ans[i], ans[j] = ans[j], ans[i]
    return ans

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
    question = str(cursor.fetchone())
    correct_ans = find_correctans(ID)
    ans = shuffle_ans(ans)
    try:
        if ans[0] == correct_ans:
            correct_button = 1
        elif ans[1] == correct_ans:
            correct_button = 2
        elif ans[2] == correct_ans:
            correct_button = 3
        elif ans[3] == correct_ans:
            correct_button = 4
        else:
            correct_button = None # error
    except TypeError:
        pass
    a = ans[0]
    b = ans[1]
    c = ans[2]
    d = ans[3]
    question = re.sub("[()',]",'',question)
    return question,correct_button,a,b,c,d

def start():
    clock = pygame.time.Clock()
    window_surface.blit(background, (0, 0))
    is_running = True
    correct_button = ""
    question = ""
    button_selected = None
    correct_selectedbutton = None
    correct_questions = 0
    questions_answered = 0
    question,correct_button,a,b,c,d = find_question()
    while is_running:
        time_delta = clock.tick(10)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                is_running = i.check_button(event.ui_element,is_running,correct_questions,questions_answered)
        correct_selectedbutton,correct_questions,questions_answered = i.check_keyboard(correct_button,button_selected,correct_selectedbutton,correct_questions,questions_answered)
        manager.update(time_delta)
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)
        window_surface.blit(font.render("Questions", True, black, None),(300,25))
        window_surface.blit(font2.render(str(question), True, black, None),(10,150))
        window_surface.blit(font.render(f"1 - {a}", True, black, None),(375,250))
        window_surface.blit(font.render(f"2 - {b}", True, black, None),(375,300))
        window_surface.blit(font.render(f"3 - {c}", True, black, None),(375,350))
        window_surface.blit(font.render(f"4 - {d}", True, black, None),(375,400))
        if correct_selectedbutton == True:
            window_surface.blit(font2.render("Correct", True, black, None),(375,200))
            correct_selectedbutton = None
            question,correct_button,a,b,c,d = find_question()
        if correct_selectedbutton == False:
            window_surface.blit(font2.render("Incorrect", True, black, None),(375,200))
            correct_selectedbutton = None
            question,correct_button,a,b,c,d = find_question()
        pygame.display.update()

i = Inputs()