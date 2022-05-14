from flask import json

dictionary_path = 'assets/dictionary.json'
dictionary = json.load(open(dictionary_path))


def get_dictionary():
    return dictionary