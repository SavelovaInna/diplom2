import nltk
import codecs
from collections import Counter

dangerous_char = ['--', '#', '/*', "'", "''", '||', '\\\\', '=', '/**/','@@']
dangerous_token = ['rename',  'drop',  'delete',  'insert',  'create',  'exec',  'update', 'union', 'set', 'alter',
                   'database', 'and', 'or', 'information_schema', 'load_file', 'select', 'shutdown', 'cmdshell', 'hex',
                   'ascii']
punctuation = ['<', '>', '*', ';', '_', '-', '(', ')', '=', '{', '}', '@', '.', ',', '&', '[', ']', '+', '-', '?', '%',
                '!', ':', '\\', '/']


def get_frequence(array, tokenized_str):
    freq = 0
    for item in array:
        if item in tokenized_str:
            freq = freq + 1
    return freq;


def is_always_true(s):
    sp = s
    s = s.replace("\'", "").replace("+", "").split('=')
    if len(s) > 1:
        for i in range(0, len(s) - 1):
            last_char = s[i][-1]
            pos = s[i+1].find(last_char)
            if pos > -1:
                left_token = s[i+1][:pos+1]
                right_token = s[i][len(s[i]) - pos - 1:]
                if left_token == right_token:
                    return True
    return False


f = codecs.open('D:\diplom\sqliAll.txt', "r", "utf_8")
out = open("out_variable.csv","w")
k = 0
for line in f:
    line = line.lower().replace('\n', '')
    s = nltk.word_tokenize(line)
    freq_danger_char = get_frequence(dangerous_char, s)
    freq_danger_token = get_frequence(dangerous_token, s)
    freq_punct = get_frequence(punctuation, s)
    freq_space = line.count(' ')
    exist_always_true = is_always_true(line)
    out.write(line + '\t' + str(freq_danger_char) + '\t' + str(freq_danger_token) + '\t' + str(freq_punct) + '\t' +
            str(len(line)) +'\t' + str(freq_space) + '\t' + str(exist_always_true) + '\n')
    k = k + 1
    print(k)




