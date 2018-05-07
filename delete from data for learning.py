from tokenizer import MyTokenizer
from frequencesCounter import FrequencesCounter
from urllib.parse import unquote
import codecs

dataNames = ['xssAll.txt', 'sqliAll.txt', 'ciAll.txt']

tokenizer = MyTokenizer()
freq_counter = FrequencesCounter()

for name in dataNames:
    f = codecs.open('data/' + name, 'r', 'utf-8')
    out = codecs.open('data/new_' + name, 'w', 'utf-8')

    for line in f:
        input = line.lower().replace('\n', '').replace('\r', '')
        input = unquote(input)
        s = tokenizer.tokenize(input)
        freq = freq_counter.get_frequences(s)
        k = 0
        for key in ['d_char', 'd_token_sqli', 'd_token_xss', 'd_token_ci']:
            k = k + freq[key]
        if k > 3 and k < 100:
            out.write(line)