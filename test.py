from fuzzy_logic_custom import FuzzySystem
from learningUtils import LearningUtils
import json


def read_rule(fs, type):
    file = open('data/rules/' + type + '_rules.txt', 'r')
    for line in file:
        fs.add_rule(json.loads(line), type)

def get_statistic_learning_data(fs, type, file_name):
    utils = LearningUtils()
    utils.type = type
    data = utils.get_input_from_file('data/new_' + type + 'All.txt')
    count_valid_detect_type = 0
    count_valid_detect = 0
    count_all = 0
    for line in data:
        try:
            res = fs.compute(line)
            if res[0] == type:
                count_valid_detect_type = count_valid_detect_type + 1
            if res[1] > 50:
                count_valid_detect = count_valid_detect + 1
            count_all = count_all + 1
        except ValueError:
            pass
    return (count_valid_detect_type/ count_all * 100, count_valid_detect/count_all * 100)

def get_false_alarm(fs):
    utils = LearningUtils()
    utils.type = type
    data = utils.get_input_from_file('data/valid_data.txt')
    count_detect = 0
    count_all = 0
    for line in data:
        try:
            res = fs.compute(line)
            if res[1] > 50:
                count_detect = count_detect + 1
            count_all = count_all + 1
        except ValueError:
            pass
    return count_detect/count_all * 100

def test(type):
    fs = FuzzySystem()
    read_rule(fs, 'sqli')
    read_rule(fs, 'xss')
    read_rule(fs, 'ci')

    fs.start_system(type)
    # fs.set_implication('resher')
    # print(get_statistic_learning_data(fs, 'sqli', 'data/new_sqliAll.txt'))
    # print(get_statistic_learning_data(fs, 'xss', 'data/new_xssAll.txt'))
    # print(get_statistic_learning_data(fs, 'ci', 'data/new_ciAll.txt'))
    # print(get_false_alarm(fs))

    #print(get_statistic_learning_data(fs, 'sqli', 'data/test_data/sql.txt'))
    #print(get_statistic_learning_data(fs, 'xss', 'data/test_data/xss.txt'))
    print(get_statistic_learning_data(fs, 'ci', 'data/test_data/ci.txt'))

test('sqli')
