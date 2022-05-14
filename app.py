from flask import Flask, jsonify, json
from flask_cors import CORS

from src.dictionary import get_dictionary
from src.quizzes import get_quizzes
from src.word_otd import get_word_otd

app = Flask(__name__)
CORS(app)



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
    app.run(debug=True, use_reloader=True)