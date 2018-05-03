import codecs
from tokenizer import MyTokenizer
from frequencesCounter import FrequencesCounter
from data_point import DataPoint

input_data = []
f = codecs.open('sqliAll.txt', "r", "utf_8")
tokenizer = MyTokenizer()
freq_counter = FrequencesCounter()

def contains_point(d):
    for point in input_data:
        if d == point:
            return True
    return False

for line in f:
    line = line.lower().replace('\n', '').replace('\r', '')
    s = tokenizer.tokenize(line)
    freq = freq_counter.get_frequences(s)
    freq_counter.get_other_param(line, freq)

    d = DataPoint()
    d.get_output(freq)
    if not contains_point(d):
        input_data.append(d)

    print(len(input_data))

