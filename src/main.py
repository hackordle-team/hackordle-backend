from flask import Flask, jsonify, json
app = Flask(__name__)

dictionary_path = 'assets/dictionary.json'

dictionary = json.load(open(dictionary_path))

@app.route('/dictionary')
def get_dictionary():
    print('Got request')
    return dictionary

@app.route('/')
def homepage():
    print('Asked for main page')
    return """
    <h1>Hello heroku XDD</h1>
    """

def main():
    print('Main func')
    app.run(debug=True, use_reloader=True)