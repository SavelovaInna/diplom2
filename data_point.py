from tokenizer import MyTokenizer
from frequencesCounter import FrequencesCounter
from fuzzy_variable import FuzzyVariable

class DataPoint:
    def __init__(self):
        self.fuzzy_vars = dict()
        self.fuzzy_vars['d_char'] = FuzzyVariable('d_char', 63, 4, 3)
        self.fuzzy_vars['d_token_sqli'] = FuzzyVariable('d_token_sqli', 13, 2, 3)
        self.fuzzy_vars['d_token_xss'] = FuzzyVariable('d_token_xss', 31, 5, 3)
        self.fuzzy_vars['d_token_ci'] = FuzzyVariable('d_token_ci', 8, 4, 3)
        self.fuzzy_vars['punck'] = FuzzyVariable('punck', 56, 2, 3)
        self.fuzzy_vars['s_token'] = FuzzyVariable('s_token', 346, 6, 3)
        self.fuzzy_vars['space'] = FuzzyVariable('space', 85, 6, 3)
        self.fuzzy_vars['length'] = FuzzyVariable('length', 969, 63, 3)
        self.output = ''
        self.memberships = []

    @staticmethod
    def __max_level(levels):
        if not levels:
            return ''
        levels_high = ['VL', 'L', 'ML', 'M', 'MH', 'H', 'VH']
        indexes = [levels_high.index(l) for l in levels]
        return levels_high[max(indexes)]

    def __create_out(self):
        out = []

        if self.fuzzy_vars['d_char'] == 'H' or self.fuzzy_vars['d_token_sqli'] == 'H':
            out.append('H')
        if self.fuzzy_vars['d_char'] == 'M' or self.fuzzy_vars['d_token_sqli'] == 'M':
            out.append('H')
        if self.fuzzy_vars['d_char'] == 'L' and self.fuzzy_vars['d_token_sqli'] == 'L'\
                and (self.fuzzy_vars['s_token'] == 'M' or self.fuzzy_vars['space'] == 'M' or
                     self.fuzzy_vars['punck'] == 'M' or self.fuzzy_vars['s_token'] == 'H' or
                     self.fuzzy_vars['space'] == 'H' or self.fuzzy_vars['punck'] == 'H'):
            out.append('M')

        if self.fuzzy_vars['d_char'] == 'L' and self.fuzzy_vars['d_token_sqli'] == 'L'\
                and self.fuzzy_vars['s_token'] == 'L' and self.fuzzy_vars['space'] == 'L' and \
                     self.fuzzy_vars['punck'] == 'L':
            out.append('L')

        return self.__max_level(out)

    def get_output(self, input):
        self.memberships = []
        for var in self.fuzzy_vars:
            self.fuzzy_vars[var].create_level(input[var])
            self.memberships.append(self.fuzzy_vars[var].get_word_level())
        self.output = self.__create_out()
        #return self.output

    def __eq__(self, other):
        for key in self.fuzzy_vars:
            if self.fuzzy_vars[key] != other.fuzzy_vars[key]:
                return False
        return True

    def to_dict_levels(self):
        d = dict()
        for var in self.fuzzy_vars:
            d[var] = self.fuzzy_vars[var].get_word_level()

        d['attack'] = self.output
        return d
