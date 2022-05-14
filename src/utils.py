import random
import datetime
def choose_word(custom_dictionary):
    seed = int(datetime.datetime.now().date().strftime("%Y%m%d"))
    random.seed(seed)
    word = random.choice(custom_dictionary['dictionary'])
    return word