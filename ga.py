from fuzzy_logic import FuzzySystem
import codecs
from urllib.parse import unquote
from tokenizer import MyTokenizer
from frequencesCounter import FrequencesCounter


def int_to_level(a):
    if a==1:
        return 'L'
    elif a==2:
        return 'M'
    elif a==3:
        return 'H'
    else:
        return ''


def fitness_function(x):
    variables = ['d_char', 'd_token_sqli', 'd_token_xss', 'd_token_ci','punck', 's_token', 'space', 'length']
    fs = FuzzySystem()
    for r in x:
        levels = dict()
        for var in variables:
            levels[var] = int_to_level(r & 0b11)
            r = r >> 2
        fs.add_rule(levels, int_to_level(r & 0b11))

    tokenizer = MyTokenizer()
    freq_counter = FrequencesCounter()
