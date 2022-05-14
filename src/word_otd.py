from flask import json
import random
import datetime

custom_dictionary_path = 'assets/custom_dictionary.json'
custom_dictionary = json.load(open(custom_dictionary_path))

def get_word_otd():
    seed = int(datetime.datetime.now().date().strftime("%Y%m%d"))
    random.seed(seed)
    word = random.choice(custom_dictionary['dictionary'])
    return {
        "word_otd": word
    }

