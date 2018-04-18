import nltk
from tokenizer import MyTokenizer
from frequencesCounter import FrequencesCounter
import codecs

f = codecs.open('sqliAll.txt', "r", "utf_8")
out = open("out_variable.csv","w")
out_another_token = open("out_another_token.txt","w")

tokenizer = MyTokenizer()
freq_counter = FrequencesCounter()
for line in f:
    line = line.lower().replace('\n', '').replace('\r', '')
    s = tokenizer.tokenize(line)
    freq = freq_counter.get_frequences(s)
    freq_counter.get_other_param(line, freq)
    res = '\t'.join(['%s' % value for (key, value) in freq.items()]) + '\n'
    if not line.endswith('\t'):
        out.write(line + '\t' + res)
    else:
        out.write(line + res)

out_another_token.write('\n'.join(freq_counter.another_token))

