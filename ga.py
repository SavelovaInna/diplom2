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
    if a == 0:
        return 'L'
    elif a == 1 or a == 2:
        return 'M'
    elif a == 3:
        return 'H'

def get_attack_count(fs, data):
    count = 0
    for line in data:
        try:
            res = fs.compute(line)
            if res > 50:
                count = count + 1
        except:
            pass
    return count

def chromosome_to_rule(r):
    variables = ['d_char', 'd_token_sqli', 'd_token_xss', 'd_token_ci', 'punck', 's_token', 'space', 'length']
    levels = dict()
    for var in variables:
        levels[var] = int_to_level(r & 0b11)
        r = r >> 2
    levels['attack'] = int_to_level(r & 0b11)
    if not levels['attack']:
        levels['attack'] = 'L'
    return levels

@profile
def fitness_function(x, *args):
    fs = FuzzySystem()
    for r in x:
        r = int(r)
        levels = chromosome_to_rule(r)
        fs.add_rule(levels, 'sqli')

    fs.start_system(''.join(args))

    detected_attack_line = get_attack_count(fs, attack_data['sqli'])
    detected_valid_line = get_attack_count(fs, valid_data)
    all_attack_line = len(attack_data['sqli'])
    all_valid_line = len(valid_data)

    res = (all_attack_line - detected_attack_line)/all_attack_line + detected_valid_line/all_valid_line
    print(detected_attack_line, detected_valid_line, res)

    return res


bounds = [(0, 262144) for i in range(0, 20)]
result = differential_evolution(fitness_function, bounds, 'sqli', 'best1bin', 7)
print(result)


# x = [199440.18040827, 160453.31339275,  74459.43200463, 172040.17706042,
#        215591.37279189,  40273.20229866, 155553.71674261, 119051.02637304,
#         18116.22680483, 127598.9181293]
for r in result.x:
    r = int(r)
    levels = chromosome_to_rule(r)
    print('  '.join(['%s:: %s' % (key, value) for (key, value) in levels.items()]))
