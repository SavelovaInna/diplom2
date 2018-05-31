from fuzzy_logic_custom import FuzzySystem
import codecs
from urllib.parse import unquote
from tokenizer import MyTokenizer
from frequencesCounter import FrequencesCounter

class LearningRule:
    def __init__(self):
        self.variables = ['d_char', 'd_token_sqli', 'd_token_xss', 'd_token_ci', 'punck', 's_token', 'space', 'length',
                          'attack']
        self.trans_from_lv = {'L': 0, 'M': 1, 'H': 3}
        self.trans_from_ch = {0: 'L', 1: 'M', 2: 'H'}
        self.levels = {}
        self.chromosome = {}

    def set_from_chromosome(self, chromosome):
        self.chromosome = chromosome
        gens = [chromosome[i:i + 2] for i in range(0, len(chromosome), 2)]
        for i in range(0, len(gens)):
            self.levels[self.variables[i]] = self.trans_from_ch[gens[i].count(1)]
        return self.levels

    def set_from_levels(self, levels):
        self.levels = levels
        self.chromosome = []
        for var in levels:
            gen = self.trans_from_lv[levels[var]]
            self.chromosome.append((gen & 10) >> 1)
            self.chromosome.append(gen & 1)
        return self.chromosome

    def __eq__(self, other):
        for var in self.levels:
            if self.levels[var] != other.levels[var]:
                return False
        return True

    def __str__(self):
        return str(self.levels)


class LearningUtils:
    def __init__(self, implication='mamdani'):
        self.attack_data = {}
        self.valid_data = self.get_input_from_file('data/valid_data.txt')
        self.implication = implication

    def setType(self, type):
        self.type = type
        self.attack_data[type] = self.get_input_from_file('data/new_' + type + 'All.txt')

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

    def get_attack_count(self, fs, data):
        count = 0
        for line in data:
            try:
                res = fs.compute_for_type(line, self.type)
                if res > 50:
                    count = count + 1
            except ValueError:
                pass
        return count

    def fitness_function(self, individual):
        fs = FuzzySystem()
        rule = LearningRule()
        rule.set_from_chromosome(individual)
        fs.add_rule(rule.levels, self.type)
        fs.set_implication(self.implication)
        fs.start_system(self.type)

        detected_attack_line = self.get_attack_count(fs, self.attack_data[self.type])
        detected_valid_line = self.get_attack_count(fs, self.valid_data)
        all_attack_line = len(self.attack_data[self.type])
        all_valid_line = len(self.valid_data)

        res = (all_attack_line * 100 - detected_attack_line) / all_attack_line + detected_valid_line / all_valid_line
        print(detected_attack_line, detected_valid_line, res)
        return (res,)

