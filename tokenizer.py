from nltk.tokenize import TreebankWordTokenizer, re
class MyTokenizer:
    def __init__(self):
        self.tokenizer = TreebankWordTokenizer()
        self.tokenizer.STARTING_QUOTES = [
            (re.compile(r'^\"'), r'``'),
            (re.compile(r'(``)'), r' \1 '),
            (re.compile(r'([ (\[{<])"'), r'\1 " '),
            (re.compile(r'([ (\[{<])\''), r'\1 \' '),
        ]
        self.tokenizer.PUNCTUATION = [
            (re.compile(r'([:,])([^\d])'), r' \1 \2'),
            (re.compile(r'([:,])$'), r' \1 '),
            (re.compile(r'\.\.\.'), r' ... '),
            (re.compile(r'%20'), r' \g<0> '),
            (re.compile(r'[:;@#$%&=+.\-\']'), r' \g<0> '),
            (re.compile(r'/\*'), r' \g<0> '),
            (re.compile(r'\*/'), r' \g<0> '),
            (re.compile(r'([^\.])(\.)([\]\)}>"\']*)\s*$'), r'\1 \2\3 '),  # Handles the final period.
            (re.compile(r'[?!]'), r' \g<0> '),
            (re.compile(r"([^'])' "), r"\1 ' "),
        ]

    def tokenize(self, string):
        return self.tokenizer.tokenize(string)
