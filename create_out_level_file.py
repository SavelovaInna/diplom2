import codecs
from tokenizer import MyTokenizer
from frequencesCounter import FrequencesCounter
from data_point import DataPoint

d = DataPoint()
f = codecs.open('sqliAll.txt', "r", "utf_8")
out = open("out_variable_fuzzy_level.csv","w")
out.write('sqli' + '\t' + '\t'.join(d.fuzzy_vars.keys()) + '\t' + 'output' + '\n')
tokenizer = MyTokenizer()
freq_counter = FrequencesCounter()

for line in f:
    line = line.lower().replace('\n', '').replace('\r', '')
    s = tokenizer.tokenize(line)
    freq = freq_counter.get_frequences(s)
    freq_counter.get_other_param(line, freq)

    d.get_output(freq)

    # res = '    '.join(s) + '\t' + \
    #       '\t'.join('{}'.format(value) for key, value in freq.items()) +\
    #       '\t' + '\t'.join(d.memberships) + '\n' #+ '\t' + create_out() + '\n'

    res = '\t'.join(d.memberships) + '\t' + d.output + '\n'
    if not line.endswith('\t'):
        out.write(line + '\t' + res)
    else:
        out.write(line + res)



