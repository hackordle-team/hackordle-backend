from flask import Flask, jsonify, json
app = Flask(__name__)

dictionary_path = 'assets/dictionary.json'

dictionary = json.load(open(dictionary_path))

@app.route('/dictionary')
def get_dictionary():
    return dictionary

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

