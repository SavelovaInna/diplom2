import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import operator


class FuzzyVariable:
    def __init__(self, name, max, middle, step=1):
        self.name = name
        self.max = max
        self.middle = middle

        self.terms = {}
        self.universum = np.arange(0, max, step)
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

    def get_word_level_max(self):
        return max(self.levels, key=lambda key: self.levels[key])

    def __eq__(self, other):
        return self.get_word_level_max() == other

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

class Implication:
    def calc_implication(self, a,b):
        pass


class ImplicationLukacevich(Implication):
    def __init__(self):
        self.antecedentOperator = np.fmax
        self.ruleOperator = np.fmin

    def calc_implication(self, a, b):
        return min(1, 1 - a + b)


class ImplicationMamdani(Implication):
    def __init__(self):
        self.antecedentOperator = np.fmin
        self.ruleOperator = np.fmax

    def calc_implication(self, a, b):
        return min(a, b)

class ImplicationGedel(Implication):
    def __init__(self):
        self.antecedentOperator = np.fmax
        self.ruleOperator = np.fmin

    def calc_implication(self, a, b):
        if a <= b:
            return 1
        return b

class ImplicationZade(Implication):
    def __init__(self):
        self.antecedentOperator = np.fmax
        self.ruleOperator = np.fmin

    def calc_implication(self, a, b):
        return max(min(a,b), 1-a)

class ImplicationResher(Implication):
    def __init__(self):
        self.antecedentOperator = np.fmax
        self.ruleOperator = np.fmin

    def calc_implication(self, a, b):
        if a <= b:
            return 1
        return 0


class FuzzySystem:
    def __init__(self):
        self.inputs = {}
        self.inputs['d_char'] = FuzzyVariable('d_char', 63, 4,1)
        self.inputs['d_token_sqli'] = FuzzyVariable('d_token_sqli', 13, 2)
        self.inputs['d_token_xss'] = FuzzyVariable('d_token_xss', 31, 5)
        self.inputs['d_token_ci'] = FuzzyVariable('d_token_ci', 8, 4)
        self.inputs['punck'] = FuzzyVariable('punck', 56, 2)
        self.inputs['s_token'] = FuzzyVariable('s_token', 346, 6)
        self.inputs['space'] = FuzzyVariable('space', 85, 6)
        self.inputs['length'] = FuzzyVariable('length', 969, 63)

        self.output = FuzzyVariable('attack', 100, 50)

        self.rules = {}
        self.rules['sqli'] = []
        self.rules['xss'] = []
        self.rules['ci'] = []

        self.implication = ImplicationLukacevich()

    def add_input(self, name, max, middle, step = 1):
        self.inputs[name] = FuzzyVariable(name, max, middle, step)

    def add_output(self, name, max, middle, step = 1):
        self.output = FuzzyVariable(name, max, middle, step)

    def set_implication(self, impl_name):
        if impl_name == 'mamdani':
            self.implication = ImplicationMamdani()
        elif impl_name == 'gedel':
            self.implication = ImplicationGedel()
        elif impl_name == 'lukasevich':
            self.implication = ImplicationLukacevich()
        elif impl_name == 'zade':
            self.implication = ImplicationZade()
        elif impl_name == 'resher':
            self.implication = ImplicationResher()

    def add_rule(self, inputs_levels, type):
        rule = Rule()
        for var in self.inputs:
            if var in inputs_levels:
                rule.add_antecedent(var, inputs_levels[var])
        rule.set_consequent(inputs_levels[self.output.name])
        self.rules[type].append(rule)

    def start_system(self, type):
        pass

    def modus_ponens(self, antecedent_var_level, consequent_set_level):
        return [self.implication.calc_implication(antecedent_var_level, x) for x in consequent_set_level]

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
                cons_term = self.output.terms[rule.consequent_level]
                rule_arr.append(self.modus_ponens(ant_level, cons_term))
            implications.append(self.agredate(rule_arr, self.implication.antecedentOperator))
        try:
            res = self.agredate(implications, self.implication.ruleOperator)
            return fuzz.defuzz(self.output.universum, res, 'centroid')
        except Exception:
            return 0

    def compute(self, data):
        res = {}
        for type in self.rules.keys():
           res[type] = self.compute_for_type(data, type)
        sorted_res = sorted(res.items(), key=operator.itemgetter(1), reverse=True)
        if abs(sorted_res[0][1] - sorted_res[1][1]) < 5 and \
                data['d_token_' + sorted_res[0][0]] < data['d_token_' + sorted_res[1][0]]:
                return sorted_res[1]
        return sorted_res[0]
