import numpy as np
import skfuzzy as fuzz

x_danger_char = np.arange(0, 11, 1)
x_danger_token = np.arange(0, 13, 1)
x_punck = np.arange(0, 38, 1)
x_susp_token = np.arange(0, 8, 1)
x_space = np.arange(0, 26, 1)
x_lenth = np.arange(0, 196, 1)
x_alw_true = np.arange(0, 2, 1)

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
    return terms;


danger_char_terms = create_terms(x_danger_char, 10, 3)
danger_tokens_terms = create_terms(x_danger_token, 12, 3)
punct_terms = create_terms(x_punck, 37, 3)
susp_token_terms = create_terms(x_susp_token, 7, 3)
space_terms = create_terms(x_space, 25, 3)
lenth_terms = create_terms(x_lenth, 195, 3)
alw_true_terms = create_terms(x_alw_true, 1, 2)



x_qual = np.arange(0, 11, 1)
x_serv = np.arange(0, 11, 1)
x_tip  = np.arange(0, 26, 1)

qual_lo = fuzz.trimf(x_qual, [0, 0, 5])
qual_md = fuzz.trimf(x_qual, [0, 5, 10])
qual_hi = fuzz.trimf(x_qual, [5, 10, 10])
serv_lo = fuzz.trimf(x_serv, [0, 0, 5])
serv_md = fuzz.trimf(x_serv, [0, 5, 10])
serv_hi = fuzz.trimf(x_serv, [5, 10, 10])
tip_lo = fuzz.trimf(x_tip, [0, 0, 13])
tip_md = fuzz.trimf(x_tip, [0, 13, 25])
tip_hi = fuzz.trimf(x_tip, [13, 25, 25])

qual_level_lo = fuzz.interp_membership(x_qual, qual_lo, 6.5)
qual_level_md = fuzz.interp_membership(x_qual, qual_md, 6.5)
qual_level_hi = fuzz.interp_membership(x_qual, qual_hi, 6.5)

serv_level_lo = fuzz.interp_membership(x_serv, serv_lo, 9.8)
serv_level_md = fuzz.interp_membership(x_serv, serv_md, 9.8)
serv_level_hi = fuzz.interp_membership(x_serv, serv_hi, 9.8)

active_rule1 = np.fmax(qual_level_lo, serv_level_lo)
tip_activation_lo = np.fmin(active_rule1, tip_lo)

tip_activation_lo = np.fmin(active_rule1, tip_lo)  # removed entirely to 0

# For rule 2 we connect acceptable service to medium tipping
tip_activation_md = np.fmin(serv_level_md, tip_md)

# For rule 3 we connect high service OR high food with high tipping
active_rule3 = np.fmax(qual_level_hi, serv_level_hi)
tip_activation_hi = np.fmin(active_rule3, tip_hi)
tip0 = np.zeros_like(x_tip)


