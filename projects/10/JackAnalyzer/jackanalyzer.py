import glob
import sys
import re


class JackTokenizer:

    keyword_list = ['class', 'constructor', 'function', 'field', 'static', 'var', 'int', 'char', 'boolean',
                    'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
    symbols = '{}()[].,;+-*/&|<>=-'
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = '0123456789'
    whitespaces = ' \r\n\t'
    token_list = []
    token_position = 0

    def __init__(self, filename):
        input_file = open(filename, 'r')
        current_token = ""
        self.token_list = []
        for line in input_file:
            self.parse_tokens(line)
        input_file.close()
        self.token_position = 0
        for token in self.token_list:
            self.print_xml_tokens(token)


    def print_xml_tokens(self, token):
        token_type = self.token_type(token)
        if token_type == 'KEYWORD':
            print('<keyword>', token, '</keyword>')
        if token_type == 'IDENTIFIER':
            print('<identifier>', token, '</identifier>')

    def parse_tokens(self, line):
        current_token = ""
        comment_line = re.search('^//', line)
        if comment_line is not None:
            return
        comment_line = re.search('^/\*', line)
        if comment_line is not None:
            return
        char_count = 0
        in_quoted_string = False

        for c in line:
            # Check for trailing comments
            if self.is_inline_comment(c, line, char_count + 1):
                    break

            # quoted string constants.
            if c == '"':
                if in_quoted_string:
                    current_token = '"' + current_token + '"'
                    in_quoted_string = False
                else:
                    in_quoted_string = True


            if self.is_alpha(c) | self.is_digit(c):
                current_token = current_token + c

            if self.is_symbol(c):
                if len(current_token) > 0:
                    self.token_list.append(current_token)
                current_token = c
                self.token_list.append(current_token)
                current_token = ""

            if self.is_whitespace(c):
                if in_quoted_string:
                    current_token = current_token + c
                else:
                    if len(current_token) > 0:
                        self.token_list.append(current_token)
                    current_token = ""
            char_count = char_count + 1

    def is_inline_comment(self, c, line, char_count):
        if len(line) > char_count:
            if c == '/':
                if line[char_count] == '/' or line[char_count] == '*':
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def is_alpha(self, c):
        if c in self.letters:
            return True
        else:
            return False

    def is_digit(self, c):
        if c in self.digits:
            return True
        else:
            return False

    def is_whitespace(self, c):
        if c in self.whitespaces:
            return True
        else:
            return False

    def is_symbol(self, c):
        if c in self.symbols:
            return True
        else:
            return False

    def has_more_tokens(self):
        if self.token_position < len(self.token_list):
            return True
        else:
            return False

    def advance(self):
        give_token = self.token_list[self.token_position]
        self.token_position = self.token_position + 1
        return give_token

    def token_type(self, token):
        test_value = 99999

        if token in self.symbols:
            return "SYMBOL"
        if token in self.keyword_list:
            return "KEYWORD"
        if '"' in token:
            return "STRING_CONSTANT"
        try:
            test_value = int(token)
        except ValueError:
            test_value = 99999
        if test_value < 99999:
            return "INT_CONSTANT"

        return "IDENTIFIER"


class JackCompiler:

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def run(self):
        while self.tokenizer.has_more_tokens():
            print(self.tokenizer.advance())

    def compileExpression(self):
        print("compile expression")

    def compileStatements(self):
        print("compile statements")

    def compileIfStatement(self):
        print("compile if statement")

    def compileWhileStatement(self):
        print("compile while statement")

    def compileTerm(self):
        print("compile term")

    def eat(self, string):
        if self.current_token != string:
            return False
        else:
            self.current_token = self.tokenizer.advance


# Main program.
if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " vm_prog")
    exit(-1)

def analyze_file(source_file):
    tokenizer = JackTokenizer(source_file)
    compiler = JackCompiler(tokenizer)
    compiler.run()


def analyze_directory(source_dir):
    for file in glob.glob("*.jack"):
        analyze_file(file)


compareCounter = 1
returnCounter = 1

source_filename = sys.argv[1]
# is this dir name or file name?
if source_filename.endswith('.jack'):
    analyze_file(source_filename)
else:
    analyze_directory(source_filename)


