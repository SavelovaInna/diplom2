import codecs
def get_tokens(file_name):
    f = codecs.open(file_name, "r", "utf_8")
    arr = []
    for line in f:
        line = line.replace('\r\n', '')
        arr.append(line)
    return arr

class FrequencesCounter:
    def __init__(self):
        self.dangerous_char = ['--', '#', '/*', '*/', "'", "''", '||', '\\\\', '=', '/**/', '@@', '%', '``', '<',
                               '>', '$', '//']
        self.dangerous_token_sqli = ['rename', 'drop', 'delete', 'insert', 'create', 'exec', 'update', 'union', 'set',
                                'alter', 'database', 'and', 'or', 'information_schema', 'load_file', 'select',
                                'shutdown', 'cmdshell', 'hex', 'ascii', 'asc', 'sleep', 'exec', 'concat',
                                'char', 'tuncat', 'group  by', 'order', 'join', 'var', 'limit', 'ord', 'benchmark',
                                'varchar', 'waitfor', 'nvarchar', 'variable', 'print', 'pg_sleep', 'elt', 'xp_regread',
                                'isnull', 'null', 'ping', '/etc/passwd', 'microsoftversione', 'mysql.user', 'procedure',
                                'localhost', 'execute', 'ipconfig', 'delay', 'sys', 'tablespace', 'xp_cmdshell',
                                'to_timestamp_tz', 'utl_http',  'current_user',  'session_user', 'current_setting',
                                'pg_shadow', 'pg_group', 'utl_inaddr', 'get_host_address', 'md5', 'bin']
        self.dangerous_token_xss = []

        self.dangerous_token_xss.extend([token.replace('<', "").replace('>', "")
                                         for token in get_tokens('data/tokens/html tegs.txt')])
        self.dangerous_token_xss.extend(get_tokens('data/tokens/html attribute.txt'))
        self.dangerous_token_xss.extend(get_tokens('data/tokens/svg tags.txt'))
        self.dangerous_token_xss.extend(get_tokens('data/tokens/js events.txt'))
        self.dangerous_token_xss.extend(get_tokens('data/tokens/js function.txt'))
        self.dangerous_token_xss.extend(get_tokens('data/tokens/character.txt'))


        self.dangerous_token_ci = ['echo', 'print(`echo', 'shell_exec', 'proc_open', 'popen', 'str', 'str1',
                                   'sleep']
        self.dangerous_substr_ci = ['exec(print', 'system(print', 'passthru(print']

        self.suspicious_token = ['from', 'all', 'as', 'declare', 'version', 'where', 'table', 'like', 'values', 'into',
                                 'any', 'distinct', 'in', 'count', 'users', 'identified', 'top', 'load',
                                 'between', 'begin', 'truncate', 'is', 'by', 'copy',  'having', 'if', 'then', 'else']
        self.punctuation = ['*', ';', '_', '-', '(', ')', '=', '{', '}', '@', '.', ',', '&', '[', ']', '+',
                            '-', '?', '!', ':', '\\', '/']

        self.another_token = set()

    def __get_frequence(self, array, tokenized_str):
        freq = 0
        for item in array:
            if item in tokenized_str:
                freq = freq + 1
        return freq;

    def create_freq_dict(self):
        freq = dict()
        freq['d_char'] = 0
        freq['d_token_sqli'] = 0
        freq['d_token_xss'] = 0
        freq['d_token_ci'] = 0
        freq['punck'] = 0
        freq['s_token'] = 0
        freq['space'] = 0
        freq['length'] = 0
        return freq

    def is_always_true(self, s):  # add 'whatever' in ('whatever')
        sp = s.split('=')  # replace("\'", "").replace("+", "")
        if len(sp) == 2:
            if sp[0] == '' or sp[1] == '':
                return False
            for i in range(0, len(sp) - 1):
                last_char = sp[i][-1]
                pos = sp[i + 1].find(last_char)
                if pos > -1:
                    left_token = sp[i + 1][:pos + 1]
                    right_token = sp[i][len(sp[i]) - pos - 1:]
                    if left_token == right_token:
                        return True
        return False

    def isNumeric(self, token):
        if token.isdigit():
            return True
        try:
            int(token, 16)
            return True
        except:
            return False

    def get_frequences(self, tokenized_str):
        freq = self.create_freq_dict()
        for token in tokenized_str:
            if token in self.dangerous_char:
                freq['d_char'] = freq['d_char'] + 1
            elif token in self.dangerous_token_ci or [s for s in self.dangerous_substr_ci if token == s]:
                freq['d_token_ci'] = freq['d_token_ci'] + 1
            elif token in self.dangerous_token_sqli or self.is_always_true(token):
                freq['d_token_sqli'] = freq['d_token_sqli'] + 1
            elif token in self.dangerous_token_xss:
                freq['d_token_xss'] = freq['d_token_xss'] + 1
            elif token in self.punctuation:
                freq['punck'] = freq['punck'] + 1
            elif token in self.suspicious_token or self.isNumeric(token):
                freq['s_token'] = freq['s_token'] + 1
            else:
                self.another_token.add(token)
        return freq

    def get_other_param(self, str, freq):
        freq['space'] = str.count(' ')
        freq['length'] = len(str)

