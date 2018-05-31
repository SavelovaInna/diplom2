from gaDEAP import GeneticLearning

types = ['sqli', 'xss', 'ci']
for type in types:
    learn = GeneticLearning(type)
    rules = learn.get_optimal_rules()
    file = open('data/rules/' + type + '_rules.txt', 'w')
    for rule in rules:
        file.write(str(rule))
    file.close()