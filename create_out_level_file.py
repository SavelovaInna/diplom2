import codecs
from urllib.parse import unquote
from tokenizer import MyTokenizer
from frequencesCounter import FrequencesCounter
from data_point import DataPoint

d = DataPoint()
tokenizer = MyTokenizer()
freq_counter = FrequencesCounter()

dataNames = ['xss', 'sqli', 'ci']
for name in dataNames:
    f = codecs.open('data/new_' + name + 'All.txt', 'r', 'utf-8')
    out = codecs.open('data/' + name + '_fuzzy_level.csv', 'w', 'utf-8')
    out.write('attack' + '\t' + '\t'.join(d.fuzzy_vars.keys()) + '\t' + 'output' + '\n')

    for line in f:
        line = line.lower().replace('\n', '').replace('\r', '')
        line = unquote(line)
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



