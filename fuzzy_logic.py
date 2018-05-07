import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class FuzzyVariable:
    def __init__(self, name, max, middle):
        self.max = max
        self.middle = middle
        universum = np.arange(0, max, 1)
        self.var = ctrl.Antecedent(universum, name)

        triangle = [0,0, middle]
        self.var['L'] = fuzz.trimf(universum, triangle)
        triangle = [0, self.middle, self.max]
        self.var['M'] = fuzz.trimf(universum, triangle)
        triangle = [self.middle, self.max, self.max]
        self.var['H'] = fuzz.trimf(universum, triangle)


class FuzzySystem:
    def __init__(self):
        self.inputs = []
        self.inputs.append(FuzzyVariable('d_char', 11, 4))
        self.inputs.append(FuzzyVariable('d_token_sqli', 13, 2))
        self.inputs.append(FuzzyVariable('d_token_xss', 31, 6))
        self.inputs.append(FuzzyVariable('d_token_ci', 8, 4))
        self.inputs.append(FuzzyVariable('punck', 38, 4))
        self.inputs.append(FuzzyVariable( 's_token', 15, 2))
        self.inputs.append(FuzzyVariable( 'space', 26, 4))
        self.inputs.append(FuzzyVariable('length', 196, 40))

        self.attack = FuzzyVariable('attack', 100, 50)
        self.rules = []

    def add_rule(self, inputs_levels, output_level):
        for variable in self.inputs:
            if inputs_levels[variable.name]:
                if antecedent:
                    antecedent = antecedent & variable[inputs_levels[variable.name]]
                else:
                    antecedent = variable[inputs_levels[variable.name]]

        self.rules.append(ctrl.Rule(antecedent, self.attack[output_level]))

    def start_system(self):
        system_control = ctrl.ControlSystem(self.rules)
        self.system = ctrl.ControlSystemSimulation(system_control)

    def compute(self, data):
        for var in self.inputs:
            self.system.input[var.name] = data[var.name]
        self.system.compute()
        return self.system.output['attack']







# New Antecedent/Consequent objects hold universe variables and membership
# functions
# quality = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')
# service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')
# tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')
#
# # Auto-membership function population is possible with .automf(3, 5, or 7)
# quality.automf(3)
# service.automf(3)
#
# # Custom membership functions can be built interactively with a familiar,
# # Pythonic API
# tip['low'] = fuzz.trimf(tip.universe, [0, 0, 13])
# tip['medium'] = fuzz.trimf(tip.universe, [0, 13, 25])
# tip['high'] = fuzz.trimf(tip.universe, [13, 25, 25])
#
#
# rule1 = ctrl.Rule(quality['poor'] | service['poor'], tip['low'])
# rule2 = ctrl.Rule(service['average'], tip['medium'])
# rule3 = ctrl.Rule(service['good'] | quality['good'], tip['high'])
# ant  = quality['poor']
# ant = ant | service['poor']
# rule4 = ctrl.Rule(ant, tip['high'])
#
# tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
# tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
#
# tipping.input['quality'] = 6.5
# tipping.input['service'] = 9.8
#
# # Crunch the numbers
# tipping.compute()
#
# print (tipping.output['tip'])