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
font2 = pygame.font.SysFont("Comic Sans MS", 13)
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

    def check_correctbutton_pressed(self,button,correct_button):
        try:
            print(correct_button)
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
            pass # choices not shown yet

    def check_button_pressed(self,button,question,correct_button):
        if button == self.start:
            question,correct_button = find_question()
            return question, correct_button
        else:
            return question,correct_button

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

def assign_userid():
    with sqlite3.connect("saves/database.db") as db:
        cursor = db.cursor()

def update_questionsanswered(uID):
    with sqlite3.connect("saves/database.db") as db:
        cursor = db.cursor()
    cursor.execute(f"""
SELECT QuestionsAnswered
FROM Progress
WHERE UserID = ?;""", [(uID)])
    answered = re.sub("['',()]", "", str(cursor.fetchone()))
    answered+=1
    cursor.execute(f"""
INSERT OR REPLACE INTO Progress(UserID, QuestionsAnswered)
VALUES(?,?);""", [(uID),(answered)])
    db.commit()

def update_score(uID):
    with sqlite3.connect("saves/database.db") as db:
        cursor = db.cursor()
    cursor.execute(f"""
SELECT CorrectQuestions
FROM Progress
WHERE UserID = ?;""", [(uID)])
    score = re.sub("['',()]", "", str(cursor.fetchone()))
    score+=1
    cursor.execute(f"""
INSERT OR REPLACE INTO Progress(UserID, CorrectQuestions)
VALUES(?,?);""", [(uID),(score)])
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
        else:
            correct_button = None # error
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
    question = str(cursor.fetchone())
    correct_ans = find_correctans(ID)
    ans = shuffle_ans(ans)
    correct_button = show_choices(ans,correct_ans)
    question = re.sub("[()',]",'',question)
    return question,correct_button

def start():
    clock = pygame.time.Clock()
    is_running = True
    correct_button = ""
    question = ""
    while is_running:
        time_delta = clock.tick(10)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                b.check_correctbutton_pressed(event.ui_element,correct_button)
                question, correct_button = b.check_button_pressed(event.ui_element,question,correct_button)
        manager.update(time_delta)
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)
        window_surface.blit(font.render("Questions", True, black, None),(300,25))
        window_surface.blit(font2.render(str(question), True, black, None),(10,150))
        pygame.display.update()
    return True

b = Buttons()