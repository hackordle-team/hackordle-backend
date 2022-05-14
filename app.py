from flask import Flask, jsonify, json
from flask_cors import CORS
from src.utils import *

app = Flask(__name__)
CORS(app)

dictionary_path = 'assets/dictionary.json'
quizes_path = 'assets/quizes.json'
custom_dictionary_path = 'assets/custom_dictionary.json'
dictionary = json.load(open(dictionary_path))
quizes = json.load(open(quizes_path))
custom_dictionary = json.load(open(custom_dictionary_path))

@app.route('/dictionary')
def get_dictionary():
    return dictionary

@app.route('/quizes')
def get_quizes():
    return quizes

@app.route('/word_otd')
def get_word_otd():
    return choose_word(custom_dictionary)


@app.route('/')
def homepage():
    return """
    <h1>Hello heroku XDD</h1>
    """

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)