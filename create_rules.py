import codecs
from tokenizer import MyTokenizer
from frequencesCounter import FrequencesCounter
from data_point import DataPoint

def create_rules(type):
    data_points = []

    f = codecs.open('data/new_' +type +'All.txt', "r", "utf_8")
    tokenizer = MyTokenizer()
    freq_counter = FrequencesCounter()

    def contains_point(d):
        for point in data_points:
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
            data_points.append(d)

    return [point.memberships for point in data_points]

