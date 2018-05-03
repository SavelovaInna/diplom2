class FrequencesCounter:
    def __init__(self):
        self.dangerous_char = ['--', '#', '/*', '*/', "'", "''", '||', '\\\\', '=', '/**/', '@@', '%']
        self.dangerous_token = ['rename', 'drop', 'delete', 'insert', 'create', 'exec', 'update', 'union', 'set',
                                'alter', 'database', 'and', 'or', 'information_schema', 'load_file', 'select',
                                'shutdown', 'cmdshell', 'hex', 'ascii', 'asc', '__time__', 'sleep', 'exec', 'concat',
                                'char', 'tuncat', 'group  by', 'order', 'join', 'var', 'limit', 'ord', 'benchmark',
                                'varchar', 'waitfor', 'nvarchar', 'variable', 'print', 'pg_sleep', 'elt', 'xp_regread',
                                'isnull', 'null', 'ping', '/etc/passwd', 'microsoftversione', 'mysql.user', 'procedure',
                                'localhost', 'execute', 'ipconfig', 'delay', 'sys', 'tablespace', 'xp_cmdshell',
                                'to_timestamp_tz', 'utl_http',  'current_user',  'session_user', 'current_setting',
                                'pg_shadow', 'pg_group', 'utl_inaddr', 'get_host_address', 'md5']

        self.suspicious_token = ['from', 'all', 'as', 'declare', 'version', 'where', 'table', 'like', 'values', 'into',
                                 'any', 'distinct', 'in', 'count', 'users', 'identified', 'top', 'load',
                                 'between', 'begin', 'truncate', 'is', 'by', 'copy',  'having']
        self.punctuation = ['<', '>', '*', ';', '_', '-', '(', ')', '=', '{', '}', '@', '.', ',', '&', '[', ']', '+',
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
        freq['d_token'] = 0
        freq['punck'] = 0
        freq['s_token'] = 0
        freq['space'] = 0
        freq['length'] = 0
        freq['alw_true'] = False
        return freq

    def is_always_true(self, s):  # add 'whatever' in ('whatever')
        sp = s.split('=')  # replace("\'", "").replace("+", "")
        if len(sp) > 1:
            if sp[0] == "":
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

    def get_frequences(self, tokenized_str):
        freq = self.create_freq_dict()
        for token in tokenized_str:
            if token in self.dangerous_char:
                freq['d_char'] = freq['d_char'] + 1
            elif token in self.dangerous_token:
                freq['d_token'] = freq['d_token'] + 1
            elif token in self.punctuation:
                freq['punck'] = freq['punck'] + 1
            elif token in self.suspicious_token:
                freq['s_token'] = freq['s_token'] + 1
            elif self.is_always_true(token):
                freq['alw_true'] = True
            else:
                self.another_token.add(token)
        return freq

    def get_other_param(self, str, freq):
        freq['space'] = str.count(' ')
        freq['length'] = len(str)
        freq['alw_true'] = self.is_always_true(str)

