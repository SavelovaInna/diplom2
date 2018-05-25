from fuzzy_logic import FuzzySystem
from gaDEAP import GeneticLearning
from learningUtils import LearningUtils


def test(type):
    fs = FuzzySystem()
    learn = GeneticLearning(type)
    rules = learn.get_optimal_rules()
    for rule in rules:
        fs.add_rule(rule.levels, type)

    fs.start_system(type)
    print('results')

    utils = LearningUtils()
    utils.type = type
    data = utils.get_input_from_file('data/new_' + type + 'All.txt')
    for line in data:
        try:
            res = fs.compute(line)
            #print(line, res)
        except ValueError:
            print(line)

test('ci')
