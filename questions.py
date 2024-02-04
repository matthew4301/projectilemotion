import pygame
import pygame.freetype
import math
import sqlite3

questions = []
answers = []

#https://replit.com/@matthew43011/sqllite-quiz#data.py

def load_db(questions,answers):
	with sqlite3.connect("saves/database.db") as db:
		cursor = db.cursor()
	cursor.execute('''
CREATE TABLE IF NOT EXISTS Questions(
QuestionID INTEGER PRIMARY KEY,
Question VARCHAR(100) NOT NULL,
Answer VARCHAR(5) NOT NULL);''')
	db.commit()
    cursor.execute(f'''
INSERT INTO Questions(QuestionID,Question,Answer)
VALUES(0,),
(1,)
(2,)
(3,);''')
		
def load_questiontxt():
    with open("saves/questions.txt") as file:
        list = file.readlines()
    for i in range(len(list)):
        if i % 2 == 0:
            answers.append(list[i])
        else:
            questions.append(list[i])
    return questions,answers