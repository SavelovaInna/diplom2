import numpy as np
import skfuzzy as fuzz

class FuzzyVariable:
    def __init__(self, name, max, middle, count_term):
        self.name = name
        self.max = max
        self.middle = middle
        self.count_term = count_term
        self.terms = []
        self.f_arr = np.arange(0, max, 1)
        if count_term == 3:
            self.create_terms_with_middle()
        else:
            self.create_even_terms()

    def __eq__(self, other):
        return self.get_word_level() == other

    def create_terms_with_middle(self):
        triangle = [0, 0, self.middle]
        self.terms.append(fuzz.trimf(self.f_arr, triangle))
        triangle = [0, self.middle, self.max]
        self.terms.append(fuzz.trimf(self.f_arr, triangle))
        triangle = [self.middle, self.max, self.max]
        self.terms.append(fuzz.trimf(self.f_arr, triangle))

    def create_even_terms(self):
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