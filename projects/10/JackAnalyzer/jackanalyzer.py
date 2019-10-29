import glob
import sys
import re


class JackTokenizer:

    keyword_list = ['class', 'constructor', 'function', 'field', 'static', 'var', 'int', 'char', 'boolean',
                    'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
    symbols_list = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '-']
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
        if c in self.symbols_list:
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

        if token in self.symbols_list:
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
            self.current_token = self.tokenizer.advance()
            if self.current_token == 'while':
                self.compileWhileStatement()

    def compileTerm(self):
        print("<term>")
        print(self.current_token)
        self.eat(self.current_token)
        print("<term>")

    def compileExpression(self):
        print("<expression>")
        if self.tokenizer.token_type(self.current_token) == "SYMBOL":
            print("<symbol>", self.current_token, "</symbol>")
            self.eat(self.current_token)
        else:
            self.compileTerm()
        if self.tokenizer.token_type(self.current_token) == "SYMBOL":
            print("<symbol>", self.current_token, "</symbol>")
            self.eat(self.current_token)
            self.compileTerm()

        print("</expression>")

    def compileStatements(self):
        print("compile statements")

    def compileIfStatement(self):
        print("compile if statement")

    def compileWhileStatement(self):
        if self.eat('while'):
            print("<whileStatement>")
            print("<keyword> while </keyword")
        else:
            print("Error processing while statement>> while", self.current_token)
            exit(-1)
        if self.eat('('):
            print ("<symbol> ( </symbol>")
        else:
            print("Error processing while statement >> while", self.current_token)
            exit(-1)
        self.compileExpression()
        print("</whileStatement>")

    def advance(self):
        if self.tokenizer.has_more_tokens():
            self.current_token = self.tokenizer.advance()

    def eat(self, test_token):
        if self.current_token == test_token:
            if self.tokenizer.has_more_tokens():
                self.current_token = self.tokenizer.advance()
            return True
        else:
            return False



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


