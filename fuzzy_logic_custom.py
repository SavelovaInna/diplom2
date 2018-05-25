import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt


class FuzzyVariable:
    def __init__(self, name, max, middle):
        self.name = name
        self.max = max
        self.middle = middle

        self.terms = {}
        self.universum = np.arange(0, max, 1)
        self.levels = {}

        triangle = [0, 0, middle]
        self.terms['L'] = fuzz.trimf(self.universum, triangle)
        triangle = [0, self.middle, self.max]
        self.terms['M'] = fuzz.trimf(self.universum, triangle)
        triangle = [self.middle, self.max, self.max]
        self.terms['H'] = fuzz.trimf(self.universum, triangle)

    def set_input(self, input):
        self.levels['L'] = fuzz.interp_membership(self.universum, self.terms['L'], input)
        self.levels['M'] = fuzz.interp_membership(self.universum, self.terms['M'], input)
        self.levels['H'] = fuzz.interp_membership(self.universum, self.terms['H'], input)

    def graph(self):
        fig, ax = plt.subplots(figsize=(8, 9))
        ax.plot(self.universum, self.terms['L'], 'b', linewidth=1.5, label='Low')
        ax.plot(self.universum, self.terms['M'], 'g', linewidth=1.5, label='Middle')
        ax.plot(self.universum, self.terms['H'], 'r', linewidth=1.5, label='High')
        ax.set_title(self.name)
        ax.legend()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        plt.tight_layout()
        plt.show()

    def __repr__(self):
        return self.name + ':' + str(self.levels)


class Rule:
    def __init__(self):
        self.antecedents_levels = {}
        self.consequent_level = None

    def add_antecedent(self, name, level):
        self.antecedents_levels[name] = level

    def set_consequent(self, level):
        self.consequent_level = level

    def __repr__(self):
        return str(self.antecedents_levels) + ' - attack:' + self.consequent_level


class FuzzySystem:
    def __init__(self):
        self.inputs = {}
        self.inputs['d_char'] = FuzzyVariable('d_char', 63, 4)
        self.inputs['d_token_sqli'] = FuzzyVariable('d_token_sqli', 13, 2)
        self.inputs['d_token_xss'] = FuzzyVariable('d_token_xss', 31, 5)
        self.inputs['d_token_ci'] = FuzzyVariable('d_token_ci', 8, 4)
        self.inputs['punck'] = FuzzyVariable('punck', 56, 2)
        self.inputs['s_token'] = FuzzyVariable('s_token', 346, 6)
        self.inputs['space'] = FuzzyVariable('space', 85, 6)
        self.inputs['length'] = FuzzyVariable('length', 969, 63)

        self.attack = FuzzyVariable('attack', 100, 50)

        self.rules = {}
        self.rules['sqli'] = []
        self.rules['xss'] = []
        self.rules['ci'] = []

        self.implication = self.implication_Lukacevich

    def implication_Lukacevich(self, a, b):
        return min(1, 1 - a + b)

    def implicationMamdani(self, a, b):
        return min(a, b)

    def set_implication(self, impl_name):
        if impl_name == 'mamdani':
            self.implication = self.implicationMamdani

    def add_rule(self, inputs_levels, out_level, type):
        rule = Rule()
        for var in inputs_levels:
            rule.add_antecedent(var, inputs_levels[var])
        rule.set_consequent(out_level)
        self.rules[type].append(rule)

    def start_system(self, type):
        pass

    def modus_ponens(self, antecedent_var_level, consequent_set_level):
        return [self.implication(antecedent_var_level,x) for x in consequent_set_level]

    def agredate(self, array, func):
        agg = array[0]
        for i in range(1, len(array)):
            agg = func(agg, array[i])
        return agg

    def compute_for_type(self, data, type):
        for var in self.inputs.keys():
            self.inputs[var].set_input(data[var])
        implications = []
        for rule in self.rules[type]:
            rule_arr = []
            for var in rule.antecedents_levels:
                ant_level = self.inputs[var].levels[rule.antecedents_levels[var]]
                cons_term = self.attack.terms[rule.consequent_level]
                rule_arr.append(self.modus_ponens(ant_level, cons_term))
            implications.append(self.agredate(rule_arr, np.fmax))
        res = self.agredate(implications, np.fmin)
        return fuzz.defuzz(self.attack.universum, res, 'centroid')

    def compute(self, data):
        #for type in self.rules.keys():
        type = 'sqli'
        print (self.compute_for_type(data, type))



rules = [
{'d_char': 'M', 'd_token_sqli': 'M', 'd_token_xss': 'L', 'd_token_ci': 'L', 'punck': 'M', 's_token': 'L', 'space': 'M', 'length': 'M'},
{'d_char': 'M', 'd_token_sqli': 'M', 'd_token_xss': 'L', 'd_token_ci': 'L', 'punck': 'M', 's_token': 'M', 'space': 'M', 'length': 'M'},
{'d_char': 'M', 'd_token_sqli': 'M', 'd_token_xss': 'L', 'd_token_ci': 'L', 'punck': 'L', 's_token': 'L', 'space': 'M', 'length': 'L'},
{'d_char': 'L', 'd_token_sqli': 'M', 'd_token_xss': 'L', 'd_token_ci': 'L', 'punck': 'M', 's_token': 'L', 'space': 'L', 'length': 'M'},
{'d_char': 'M', 'd_token_sqli': 'L', 'd_token_xss': 'L', 'd_token_ci': 'L', 'punck': 'M', 's_token': 'L', 'space': 'L', 'length': 'L'},
{'d_char': 'L', 'd_token_sqli': 'M', 'd_token_xss': 'L', 'd_token_ci': 'L', 'punck': 'M', 's_token': 'L', 'space': 'M', 'length': 'M'},
{'d_char': 'M', 'd_token_sqli': 'L', 'd_token_xss': 'L', 'd_token_ci': 'L', 'punck': 'M', 's_token': 'L', 'space': 'M', 'length': 'M'},
]

fs = FuzzySystem()
for r in rules:
    fs.add_rule(r, 'H', 'sqli')


data = [
    {'d_char': 1, 'd_token_sqli': 2, 'd_token_xss': 0, 'd_token_ci': 0, 'punck': 5, 's_token': 0, 'space': 2, 'length': 26},
{'d_char': 1, 'd_token_sqli': 2, 'd_token_xss': 0, 'd_token_ci': 0, 'punck': 6, 's_token': 0, 'space': 2, 'length': 27},
{'d_char': 1, 'd_token_sqli': 2, 'd_token_xss': 0, 'd_token_ci': 0, 'punck': 6, 's_token': 0, 'space': 2, 'length': 27},
{'d_char': 4, 'd_token_sqli': 1, 'd_token_xss': 0, 'd_token_ci': 0, 'punck': 3, 's_token': 0, 'space': 2, 'length': 12},
{'d_char': 8, 'd_token_sqli': 1, 'd_token_xss': 0, 'd_token_ci': 0, 'punck': 4, 's_token': 0, 'space': 8, 'length': 45},
{'d_char': 1, 'd_token_sqli': 2, 'd_token_xss': 0, 'd_token_ci': 0, 'punck': 5, 's_token': 2, 'space': 0, 'length': 27},
{'d_char': 3, 'd_token_sqli': 2, 'd_token_xss': 0, 'd_token_ci': 0, 'punck': 6, 's_token': 2, 'space': 2, 'length': 32},
{'d_char': 1, 'd_token_sqli': 5, 'd_token_xss': 0, 'd_token_ci': 0, 'punck': 17, 's_token': 5, 'space': 0, 'length': 43},
{'d_char': 11, 'd_token_sqli': 1, 'd_token_xss': 2, 'd_token_ci': 0, 'punck': 2, 's_token': 0, 'space': 2, 'length': 21},
{'d_char': 2, 'd_token_sqli': 1, 'd_token_xss': 0, 'd_token_ci': 1, 'punck': 2, 's_token': 0, 'space': 2, 'length': 21},
{'d_char': 2, 'd_token_sqli': 1, 'd_token_xss': 0, 'd_token_ci': 0, 'punck': 0, 's_token': 2, 'space': 3, 'length': 9} ,
{'d_char': 1, 'd_token_sqli': 1, 'd_token_xss': 0, 'd_token_ci': 1, 'punck': 3, 's_token': 1, 'space': 2, 'length': 22},
{'d_char': 4, 'd_token_sqli': 1, 'd_token_xss': 2, 'd_token_ci': 0, 'punck': 3, 's_token': 0, 'space': 2, 'length': 12},
{'d_char': 0, 'd_token_sqli': 4, 'd_token_xss': 0, 'd_token_ci': 0, 'punck': 4, 's_token': 2, 'space': 8, 'length': 40},
{'d_char': 1, 'd_token_sqli': 3, 'd_token_xss': 0, 'd_token_ci': 0, 'punck': 7, 's_token': 3, 'space': 2, 'length': 34},
{'d_char': 5, 'd_token_sqli': 1, 'd_token_xss': 1, 'd_token_ci': 0, 'punck': 2, 's_token': 2, 'space': 2, 'length': 14},
{'d_char': 2, 'd_token_sqli': 3, 'd_token_xss': 0, 'd_token_ci': 0, 'punck': 5, 's_token': 2, 'space': 2, 'length': 32}
]

fs.set_implication('mamdani')
for d in data:
    print(fs.compute_for_type(d, 'sqli'))




