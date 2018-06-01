import array
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from learningUtils import LearningUtils, LearningRule
from create_rules import create_rules
from fuzzy_logic_custom import FuzzySystem
from random import randint


class GeneticLearning:
    def create_params(self, max):
        return [max//2, 0, max//2, max, max//2]

    def init_individual(self, creator, count_rules):
        rules_ch = []
        for i in range(0, count_rules):
            rule = LearningRule()
            rule.set_from_levels(self.initial_rules[randint(0, len(self.initial_rules)-1)])
            rules_ch.append(rule.int_value)
        return creator(self.initial_membersips + rules_ch)

    def init_population(self, pcls, ind_init, pop_size, count_rules):
        return pcls(ind_init(count_rules) for i in range(0, pop_size))

    def __init__(self, type, implication_type='mamdani'):
        self.utils = LearningUtils(implication_type)
        self.utils.setType(type)
        self.initial_rules = create_rules(self.utils.type)
        self.initial_membersips  = []
        for x in [63, 13, 31, 8, 56, 346, 85, 969]:
            self.initial_membersips.extend(self.create_params(x))

        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin)
        self.toolbox = base.Toolbox()

        self.toolbox.register("individual_guess", self.init_individual, creator.Individual)
        self.toolbox.register("population_guess", self.init_population, list, self.toolbox.individual_guess, 30, 5)

        self.toolbox.register("evaluate", self.utils.fitness_function)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def ga(self):
        pop = self.toolbox.population_guess()
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)

        pop, log = algorithms.eaSimple(pop, self.toolbox, cxpb=0.5, mutpb=0.2, ngen=10,
                                       stats=stats, halloffame=hof, verbose=False)

        return hof

    def delete_attack_check(self, fs, data):
        i = 0
        while i < len(data):
            try:
                res = fs.compute(data[i])
                if res[1] > 50:
                    del data[i]
                    i = i - 1
            except ValueError:
                pass
            i = i + 1

    def get_optimal_rules(self):
        rules = []
        fs = FuzzySystem()
        fs.set_implication(self.utils.implication)
        while True:
            res = self.ga()
            rule = LearningRule()
            rule.set_from_chromosome(res.items[0])
            print(rule.levels)
            if not rule in rules:
                fs.add_rule(rule.levels, self.utils.type)
                fs.start_system(self.utils.type)
                lastLen = len(self.utils.attack_data[self.utils.type])
                self.delete_attack_check(fs, self.utils.attack_data[self.utils.type])
                newLen = len(self.utils.attack_data[self.utils.type])
                if lastLen != newLen:
                    rules.append(rule)
                print(newLen)
                if not len(self.utils.attack_data[self.utils.type]):
                    break
        for rule in rules:
            print(rule.levels)
        return rules

l = GeneticLearning('sqli')
l.get_optimal_rules()

