import numpy as np
import skfuzzy as fuzz
import codecs
from tokenizer import MyTokenizer
from frequencesCounter import FrequencesCounter

fuzzy_vars = dict()

fuzzy_vars['d_char'] = dict()
fuzzy_vars['d_char']['max'] = 11
fuzzy_vars['d_char']['count_term'] = 3

fuzzy_vars['d_token'] = dict()
fuzzy_vars['d_token']['max'] = 13
fuzzy_vars['d_token']['count_term'] = 3

fuzzy_vars['punck'] = dict()
fuzzy_vars['punck']['max'] = 38
fuzzy_vars['punck']['count_term'] = 3

fuzzy_vars['s_token'] = dict()
fuzzy_vars['s_token']['max'] = 8
fuzzy_vars['s_token']['count_term'] = 3

fuzzy_vars['space'] = dict()
fuzzy_vars['space']['max'] = 8
fuzzy_vars['space']['count_term'] = 3

fuzzy_vars['length'] = dict()
fuzzy_vars['length']['max'] = 196
fuzzy_vars['length']['count_term'] = 3

fuzzy_vars['alw_true'] = dict()
fuzzy_vars['alw_true']['max'] = 2
fuzzy_vars['alw_true']['count_term'] = 2

for var in fuzzy_vars:
    fuzzy_vars[var]["f_arr"] = np.arange(0, fuzzy_vars[var]["max"], 1)

x_injection = np.arange(0, 100, 1)

def create_terms(fuzzy_var, max_value, count):
    step = max_value//(count-1)
    triangle = [0, 0, step]
    terms = []
    for i in range(0, count):
        terms.append(fuzz.trimf(fuzzy_var, triangle))
        triangle[0] = triangle[1]
        triangle[1] = triangle[2]
        if triangle[2] + step < max_value:
            triangle[2] = triangle[2] + step
        else:
            triangle[2] = max_value
    return terms

for var in fuzzy_vars:
    fuzzy_vars[var]["terms"] = create_terms(fuzzy_vars[var]["f_arr"], fuzzy_vars[var]["max"] - 1,
                                            fuzzy_vars[var]["count_term"])


def create_level(fuzzy_var, terms, input):
    memberships = []
    for term in terms:
        memberships.append(fuzz.interp_membership(fuzzy_var, term, input))
    return memberships

def get_word_level(membership):
    levels_lower = ['very low', 'low', 'medium low', 'medium', 'medium high', 'high', 'very high']
    levels_high = ['VL', 'L', 'ML', 'M', 'MH', 'H', 'VH']
    max_level = membership.index(max(membership))
    step = 7 // len(membership)
    level = 1
    if len(membership) == 2:
        for i in range(0, max_level):
            level = level + step

        return levels_high[level]
    else:
        return levels_high[max_level]


f = codecs.open('sqliAll.txt', "r", "utf_8")
out = open("out_variable_fuzzy_level.csv","w")
tokenizer = MyTokenizer()
freq_counter = FrequencesCounter()

for line in f:
    line = line.lower().replace('\n', '').replace('\r', '')
    s = tokenizer.tokenize(line)
    freq = freq_counter.get_frequences(s)
    freq_counter.get_other_param(line, freq)
    memberships = []

    for var in fuzzy_vars:
        membership = create_level(fuzzy_vars[var]["f_arr"],fuzzy_vars[var]["terms"], freq[var])
        memberships.append(get_word_level(membership))

    res = '\t'.join(memberships) + '\n'
    if not line.endswith('\t'):
        out.write(line + '\t' + res)
    else:
        out.write(line + res)


# active_rule1 = np.fmax(qual_level_lo, serv_level_lo)
# tip_activation_lo = np.fmin(active_rule1, tip_lo)
#
# tip_activation_lo = np.fmin(active_rule1, tip_lo)  # removed entirely to 0
#
# # For rule 2 we connect acceptable service to medium tipping
# tip_activation_md = np.fmin(serv_level_md, tip_md)
#
# # For rule 3 we connect high service OR high food with high tipping
# active_rule3 = np.fmax(qual_level_hi, serv_level_hi)
# tip_activation_hi = np.fmin(active_rule3, tip_hi)
# tip0 = np.zeros_like(x_tip)
#
# aggregated = np.fmax(tip_activation_lo,
#                      np.fmax(tip_activation_md, tip_activation_hi))
#
# # Calculate defuzzified result
# tip = fuzz.defuzz(x_tip, aggregated, 'centroid')



