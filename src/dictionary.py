from flask import json
from src.word_otd import custom_dictionary


dictionary_path = 'assets/dictionary.json'


def merge_dictionaries():
    dictionary = json.load(open(dictionary_path))
    merged_dictionary = list(set(dictionary['dictionary'] + custom_dictionary['dictionary']))
    
    return {
        "dictionary": sorted(merged_dictionary)
    }


dictionary = merge_dictionaries()

def get_dictionary():
    return dictionary