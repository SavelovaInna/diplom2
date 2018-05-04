import codecs
# f = codecs.open('data/html tegs.txt', "r", "utf_8")
# arr = []
# for line in f:
#     line = line.replace('<', "'").replace('>', "'").replace('\r\n', '')
#     arr.append(line)
# print(', '.join(arr))

f = codecs.open('data/js events.txt', "r", "utf_8")
arr = []
for line in f:
    line = line.replace('\r\n', '')
    line = "'" + line + "'"
    arr.append(line)
print(', '.join(arr))
