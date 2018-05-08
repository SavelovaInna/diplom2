from fuzzy_logic import FuzzySystem
import codecs
from urllib.parse import unquote
from tokenizer import MyTokenizer
from frequencesCounter import FrequencesCounter
from scipy.optimize import differential_evolution

def get_input_from_file(file_name):
    f = codecs.open(file_name, "r", "utf_8")
    tokenizer = MyTokenizer()
    freq_counter = FrequencesCounter()
    input = []
    for line in f:
        line = line.lower().replace('\n', '').replace('\r', '')
        line = unquote(line)
        s = tokenizer.tokenize(line)
        freq = freq_counter.get_frequences(s)
        freq_counter.get_other_param(line, freq)
        input.append(freq)
    return input

attack_data ={}
attack_data['sqli'] = get_input_from_file('data/new_sqliAll.txt')
valid_data = get_input_from_file('data/valid_data.txt')

def int_to_level(a):
    if a == 1:
        return 'L'
    elif a == 2:
        return 'M'
    elif a == 3:
        return 'H'
    else:
        return ''

def get_attack_count(fs, data):
    count = 0
    for line in data:
        try:
            res = fs.compute(line)
            if res > 40:
                count = count + 1
        except:
            pass
    return count

def fitness_function(x, *args):
    variables = ['d_char', 'd_token_sqli', 'd_token_xss', 'd_token_ci','punck', 's_token', 'space', 'length']
    fs = FuzzySystem()
    for r in x:
        r = int(r)
        levels = dict()
        for var in variables:
            levels[var] = int_to_level(r & 0b11)
            r = r >> 2
        levels['attack'] = int_to_level(r & 0b11)
        if not levels['attack']:
            levels['attack'] = 'L'
        fs.add_rule(levels, 'sqli')

    fs.start_system(''.join(args))

    detected_attack_line = get_attack_count(fs, attack_data['sqli'])
    detected_valid_line = get_attack_count(fs, valid_data)
    all_attack_line = len(attack_data['sqli'])
    all_valid_line = len(valid_data)

    print(detected_attack_line, detected_valid_line,
          1 / (detected_attack_line/all_attack_line - detected_valid_line/all_valid_line))
    return 1 / abs(detected_attack_line/all_attack_line - detected_valid_line/all_valid_line)


bounds = [(0, 262144) for i in range(0, 200)]
result = differential_evolution(fitness_function, bounds, 'sqli')
print(result)



