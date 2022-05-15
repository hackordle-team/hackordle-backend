from time import sleep
from flask import Flask
from flask_cors import CORS
from flask_sock import Sock

from threading import Thread

from src.dictionary import get_dictionary
from src.quizzes import get_quizzes
from src.word_otd import get_word_otd
from src.websocket import MatchManager

app = Flask(__name__)
CORS(app)
sock = Sock(app)

# global match_manager
match_manager = MatchManager()

@sock.route('/multiplayer')
def route_ws_test(ws):
    match_manager.new_client(ws)


@app.route('/dictionary')
def route_dictionary():
    return get_dictionary()

@app.route('/quizzes')
def route_quizzes():
    return get_quizzes()

@app.route('/word_otd')
def route_word_otd():
    return get_word_otd()


@app.route('/')
def homepage():
    return """
    <h1>Hello heroku XDD</h1>
    """

if __name__ == '__main__':
    # match_manager.create_match_manager()
    # kill_thread = create_match_manager()
    try:
        app.run(use_reloader=True)
    finally:
        match_manager.kill()

    