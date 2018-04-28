import numpy as np
import skfuzzy as fuzz
import codecs
from tokenizer import MyTokenizer
from frequencesCounter import FrequencesCounter


class FuzzyVariable:
    def __init__(self, name, max, count_term):
        self.name = name
        self.max = max
        self.count_term = count_term
        self.terms = []
        self.f_arr = np.arange(0, max, 1)
        self.create_terms()

    def __eq__(self, other):
        return self.get_word_level() == other

    def create_terms(self):
        step = (self.max - 1) // (self.count_term - 1)
        triangle = [0, 0, step]
        for i in range(0, self.count_term):
            self.terms.append(fuzz.trimf(self.f_arr, triangle))
            triangle[0] = triangle[1]
            triangle[1] = triangle[2]
            if triangle[2] + step < self.max - 1:
                triangle[2] = triangle[2] + step
            else:
                triangle[2] = self.max - 1

    def create_level(self, input):
        self.membership = []
        for term in self.terms:
            self.membership.append(fuzz.interp_membership(self.f_arr, term, input))

    def get_word_level(self):
        levels_lower = ['very low', 'low', 'medium low', 'medium', 'medium high', 'high', 'very high']
        levels_high = ['VL', 'L', 'ML', 'M', 'MH', 'H', 'VH']
        max_level = self.membership.index(max(self.membership)) + 1
        if self.count_term == 7:
            return levels_high[max_level - 1]
        elif self.count_term == 5:
            return levels_high[max_level]
        elif self.count_term == 3:
            return levels_high[max_level * 2 - 1]
        elif self.count_term == 2:
            if max_level == 2:
                return levels_high[max_level + 3]
            return levels_high[max_level]


fuzzy_vars = dict()
fuzzy_vars['d_char'] = FuzzyVariable('d_char', 11, 3)
fuzzy_vars['d_token'] = FuzzyVariable('d_token', 13, 3)
fuzzy_vars['punck'] = FuzzyVariable('punck', 38, 3)
fuzzy_vars['s_token'] = FuzzyVariable('s_token', 8, 3)
fuzzy_vars['space'] = FuzzyVariable('space', 26, 3)
fuzzy_vars['length'] = FuzzyVariable('length', 196, 3)
fuzzy_vars['alw_true'] = FuzzyVariable('alw_true', 2, 2)


def create_out():
    count_h = 0
    count_l = 0
    count_m = 0
    for var in fuzzy_vars:
        if fuzzy_vars[var] == 'H':
            count_h = count_h + 1
        if fuzzy_vars[var] == 'M':
            count_m = count_m + 1
        if fuzzy_vars[var] == 'L':
            count_l = count_l + 1

    out = []
    if count_h > 3:
        out.append('H')
    if count_l > 3:
        out.append('L')
    if fuzzy_vars['alw_true'] == 'H':
        out.append('H')
    if fuzzy_vars['d_char'] == 'M' or fuzzy_vars['d_token'] == 'M':
        out.append('M')
    return '-'.join(out)

f = codecs.open('sqliAll.txt', "r", "utf_8")
out = open("out_variable_fuzzy_level.csv","w")
out.write('sqli' + '\t' + '\t'.join(fuzzy_vars.keys()) + '\t' + 'output' + '\n')
tokenizer = MyTokenizer()
freq_counter = FrequencesCounter()

for line in f:
    line = line.lower().replace('\n', '').replace('\r', '')
    s = tokenizer.tokenize(line)
    freq = freq_counter.get_frequences(s)
    freq_counter.get_other_param(line, freq)
    memberships = []

    for var in fuzzy_vars:
        fuzzy_vars[var].create_level(freq[var])
        memberships.append(fuzzy_vars[var].get_word_level())

    res = '\t'.join(memberships) + '\t' + create_out() + '\n'
    if not line.endswith('\t'):
        out.write(line + '\t' + res)
    else:
        out.write(line + res)



