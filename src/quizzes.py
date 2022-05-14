from flask import json

quizzes_path = 'assets/quizzes.json'
quizzes = json.load(open(quizzes_path))

def get_quizzes():
    return quizzes
