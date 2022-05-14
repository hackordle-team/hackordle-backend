from flask import Flask, jsonify


app = Flask(__name__)

@app.route('/dictionary')
def dictionary():
    data = {
        "dictionary" : [
            "word1",
            "word2",
            "word3",
            "word4",
            "word5",
        ]
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

