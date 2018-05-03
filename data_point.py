from tokenizer import MyTokenizer
from frequencesCounter import FrequencesCounter
from fuzzy_variable import FuzzyVariable

class DataPoint:
    def __init__(self):
        self.fuzzy_vars = dict()
        self.fuzzy_vars['d_char'] = FuzzyVariable('d_char', 11, 2, 3)
        self.fuzzy_vars['d_token'] = FuzzyVariable('d_token', 13, 2, 3)
        self.fuzzy_vars['punck'] = FuzzyVariable('punck', 38, 4, 3)
        self.fuzzy_vars['s_token'] = FuzzyVariable('s_token', 15, 2, 3)
        self.fuzzy_vars['space'] = FuzzyVariable('space', 26, 4, 3)
        self.fuzzy_vars['length'] = FuzzyVariable('length', 196, 40, 3)
        self.fuzzy_vars['alw_true'] = FuzzyVariable('alw_true', 2, 0.5, 2)
        self.output = ''
        self.memberships = []

    def __max_level(self, levels):
        if not levels:
            return ''
        levels_high = ['VL', 'L', 'ML', 'M', 'MH', 'H', 'VH']
        indexes = [levels_high.index(l) for l in levels]
        return levels_high[max(indexes)]

    def  __create_out(self):
        count_h = 0
        count_l = 0
        count_m = 0
        for var in self.fuzzy_vars:
            if self.fuzzy_vars[var] == 'H':
                count_h = count_h + 1
            if self.fuzzy_vars[var] == 'M':
                count_m = count_m + 1
            if self.fuzzy_vars[var] == 'L':
                count_l = count_l + 1

        out = []
        if count_h > 3:
            out.append('H')
        if count_m > 3:
            out.append('H')
        if count_l > 3:
            out.append('L')
        if self.fuzzy_vars['alw_true'] == 'H' and \
                (self.fuzzy_vars['d_char'] == 'H' or self.fuzzy_vars['d_token'] == 'H'):
            out.append('H')
        if self.fuzzy_vars['alw_true'] == 'H' and \
                (self.fuzzy_vars['d_char'] == 'M' and self.fuzzy_vars['d_token'] == 'M'):
            out.append('H')
        if self.fuzzy_vars['d_char'] == 'H' and self.fuzzy_vars['d_token'] == 'H':
            out.append('H')
        if self.fuzzy_vars['alw_true'] == 'H' or \
                (self.fuzzy_vars['d_char'] == 'H' or self.fuzzy_vars['d_token'] == 'H'):
            out.append('M')
        if self.fuzzy_vars['d_char'] == 'M' and self.fuzzy_vars['d_token'] == 'M':
            out.append('M')

        return self.__max_level(out)

    def get_output(self, input):
        self.memberships = []
        for var in self.fuzzy_vars:
            self.fuzzy_vars[var].create_level(input[var])
            self.memberships.append(self.fuzzy_vars[var].get_word_level())
        self.output = self.__create_out()
        return self.output

    def __eq__(self, other):
        for key in self.fuzzy_vars:
            if self.fuzzy_vars[key] != other.fuzzy_vars[key]:
                return False
        return True
