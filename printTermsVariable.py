from fuzzy_logic_custom import FuzzySystem
fs = FuzzySystem()
for var in fs.inputs.keys():
    fs.inputs[var].graph()