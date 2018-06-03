import re
import os

def get_payload_xml(file_name):
    f = open('data/test_data/sqlmap/' + file_name, 'r')
    data = f.read()
    f.close()
    res = re.findall(r'<vector>([\s\S]*?)<\/vector>', data)
    f = open('data/test_data/sql.txt', 'a')
    for r in res:
        f.write(r + '\n')
    f.close()

def get_payload_xss(file_name):
    f = open('data/test_data/xss/' + file_name, 'r')
    data = f.read()
    f.close()
    res = re.findall(r'Exploit String:([\s\S]*?)Exploit Description:', data)
    f = open('data/test_data/xss.txt', 'a')
    for r in res:
        f.write(r)
    f.close()

# for filename in os.listdir('data/test_data/sqlmap'):
#     get_payload_xml(filename)

get_payload_xss('XSS-WITH-CONTEXT-JHADDIX.txt')