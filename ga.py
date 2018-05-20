from scipy.optimize import differential_evolution
from learningUtils import LearningUtils


def create_rule(type):
    utils = LearningUtils()
    utils.setType('xss')


    bounds = [(0, 262144) for i in range(0, 2)]
    result = differential_evolution(utils.fitness_function_sciPy, bounds)
    print(result)


    for r in result.x:
        r = int(r)
        levels = utils.chromosome_to_rule(r)
        print('  '.join(['%s:: %s' % (key, value) for (key, value) in levels.items()]))


create_rule('xss')
