from fuzzy_logic_custom import FuzzySystem

rules = [{'d': 'H', 'r': 'H', 'm': 'H'}, {'d': 'L', 'r': 'M', 'm': 'M'}]

fs = FuzzySystem()
fs.inputs = {}
fs.add_input('d', 1001, 500, 100)
fs.add_input('r', 101, 50, 10)
fs.add_output('m', 501, 250, 50)

#fs.set_implication('gedel')
for r in rules:
    fs.add_rule(r, 'sqli')
res = fs.compute({'d':600, 'r':70})
print(res)