import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import codecs
from tokenizer import MyTokenizer
from frequencesCounter import FrequencesCounter


danger_char = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')
danger_token = ctrl.Antecedent(np.arange(0, 13, 1), 'danger_token')
punck = ctrl.Antecedent(np.arange(0, 38, 1), 'punck')
susp_token = ctrl.Antecedent(np.arange(0, 8, 1), 'susp_token')
space = ctrl.Antecedent(np.arange(0, 26, 1), 'space')
length = ctrl.Antecedent(np.arange(0, 196, 1), 'length')
alw_true = ctrl.Antecedent(np.arange(0, 2, 1), 'alw_true')
x_injection = np.arange(0, 100, 1)


danger_char.automf(3)
danger_token.automf(3)
punck.automf(3)
susp_token.automf(3)
space.automf(3)
length.automf(3)
alw_true.automf(3)
x_injection.automf(3)

f = codecs.open('sqliAll.txt', "r", "utf_8")
tokenizer = MyTokenizer()
freq_counter = FrequencesCounter()

for line in f:
    line = line.lower().replace('\n', '').replace('\r', '')
    s = tokenizer.tokenize(line)
    freq = freq_counter.get_frequences(s)
    freq_counter.get_other_param(line, freq)




# rule1 = ctrl.Rule(quality['poor'] | service['poor'], tip['low'])
# rule2 = ctrl.Rule(service['average'], tip['medium'])
# rule3 = ctrl.Rule(service['good'] | quality['good'], tip['high'])
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