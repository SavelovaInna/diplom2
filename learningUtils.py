from fuzzy_logic import FuzzySystem
import codecs
from urllib.parse import unquote
from tokenizer import MyTokenizer
from frequencesCounter import FrequencesCounter


class LearningUtils:
    def __init__(self):
        self.attack_data = {}
        self.valid_data = self.get_input_from_file('data/valid_data.txt')

    def get_input_from_file(self, file_name):
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


    def int_to_level(self, a):
        if a == 0:
            return 'L'
        elif a == 1 or a == 2:
            return 'M'
        elif a == 3:
            return 'H'


    def get_attack_count(self, fs, data):
        count = 0
        for line in data:
            try:
                res = fs.compute(line)
                if res > 50:
                    count = count + 1
            except ValueError:
                pass
        return count


    def chromosome_to_rule(self,r):
        variables = ['d_char', 'd_token_sqli', 'd_token_xss', 'd_token_ci', 'punck', 's_token', 'space', 'length']
        levels = dict()
        for var in variables:
            levels[var] = self.int_to_level(r & 0b11)
            r = r >> 2
        levels['attack'] = self.int_to_level(r & 0b11)
        if not levels['attack']:
            levels['attack'] = 'L'
        return levels

    def fitness_function_sciPy(self, x, *args):
        fs = FuzzySystem()
        type = ''.join(args)
        for r in x:
            r = int(r)
            levels = self.chromosome_to_rule(r)
            fs.add_rule(levels, type)

        fs.start_system(type)

        detected_attack_line = self.get_attack_count(fs, self.attack_data[type])
        detected_valid_line = self.get_attack_count(fs, self.valid_data)
        all_attack_line = len(self.attack_data[type])
        all_valid_line = len(self.valid_data)

        res = (all_attack_line - detected_attack_line)/all_attack_line + detected_valid_line/all_valid_line
        print(detected_attack_line, detected_valid_line, res)

        return res

