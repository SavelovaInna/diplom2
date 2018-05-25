import array
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from learningUtils import LearningUtils, LearningRule
from create_rules import create_rules
from fuzzy_logic import FuzzySystem


class GeneticLearning:
    def init_individual(self, creator, levels):
        rule = LearningRule()
        rule.set_from_levels(levels)
        return creator(rule.chromosome)

    def init_population(self, pcls, ind_init):
        return pcls(ind_init(x) for x in create_rules(self.utils.type))

    def __init__(self, type):
        self.utils = LearningUtils()
        self.utils.setType(type)

        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", array.array, typecode='b', fitness=creator.FitnessMin)
        self.toolbox = base.Toolbox()

        self.toolbox.register("individual_guess", self.init_individual, creator.Individual)
        self.toolbox.register("population_guess", self.init_population, list, self.toolbox.individual_guess)

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
                if res > 50:
                    del data[i]
                    i = i - 1
            except ValueError:
                pass
            i = i + 1

    def get_optimal_rules(self):
        rules = []
        fs = FuzzySystem()
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

