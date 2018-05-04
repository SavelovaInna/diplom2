import nltk
from tokenizer import MyTokenizer
from frequencesCounter import FrequencesCounter
from urllib.parse import unquote
import codecs

#f = codecs.open('data/xssAll.txt', "r", "utf_8")
f = codecs.open('data/sqliAll.txt', "r", "utf_8")
#f = codecs.open('data/ciAll.txt', "r", "utf_8")
out = codecs.open("out_variable.csv", "w")
out_another_token = codecs.open("out_another_token.txt", "w", "utf-8")

tokenizer = MyTokenizer()
freq_counter = FrequencesCounter()
out.write('attack' + '\t' + '\t'.join(['%s' % key for (key, value) in freq_counter.get_frequences('').items()]) + '\n')
for line in f:
    line = line.lower().replace('\n', '').replace('\r', '')
    line = unquote(line)
    s = tokenizer.tokenize(line)
    freq = freq_counter.get_frequences(s)
    freq_counter.get_other_param(line, freq)
    res = '\t'.join(['%s' % value for (key, value) in freq.items()]) + '\n'
    try:
        if not line.endswith('\t'):
            out.write(line + '\t' + res)
        else:
            out.write(line + res)
    except:
        print(line)

    out_another_token.write(line + '\t' + '\n'.join(freq_counter.another_token))
    freq_counter.another_token = set()

#out_another_token.write('\n'.join(freq_counter.another_token))

