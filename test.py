from fuzzy_logic import FuzzySystem
from create_rules import create_rules
from ga import chromosome_to_rule, get_input_from_file

# fs = FuzzySystem()
# rules = create_rules('sqli')
# for rule in rules:
#     fs.add_rules(rule, 'sqli')
#
# print('sfd')

# sqli rules

# x = [256293.35406428, 215883.56895036, 238862.00979164, 257533.7033801 ,
#        205322.27489684]

# x = [207110.2701135 , 197066.34231817, 237834.86427123, 206203.17207551,
#        105142.59168532, 237069.11241751, 102361.59558646] # 218 pop = 7 iter  = 30

# x = [ 29293.76924455, 233474.88346135, 235529.50946856, 219653.22141773,
#        233738.02008281] # 252 from 264 pop = 5 iter=100

#xss rules

x = [174001.76288437,  78065.49331034, 200999.00727646, 218642.46866059,
       200692.94748058,  59300.98611445, 206413.95121078] #314 from pop = 7 iter = 10
fs = FuzzySystem()

print('rules')
for r in x:
    r = int(r)
    levels = chromosome_to_rule(r)
    fs.add_rule(levels, 'sqli')
    print(levels)

fs.start_system('sqli')
print('results')

data = get_input_from_file('data/new_sqliAll.txt')
for line in data:
    try:
        res = fs.compute(line)
        print(line, res)
    except Exception:
        print(line)
