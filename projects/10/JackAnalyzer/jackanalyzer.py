import glob
import sys
import re


class JackTokenizer:

    keyword_list = ['class', 'constructor', 'method', 'function', 'field', 'static', 'var', 'int', 'char', 'boolean',
                    'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
    symbols_list = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '-', '~']
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = '0123456789'
    whitespaces = ' \r\n\t'
    token_list = []
    token_type = []
    token_position = 0

    def __init__(self, filename):
        input_file = open(filename, 'r')
        output_file = open(filename + 'T.xml', 'w')
        current_token = ""
        self.token_list = []
        for line in input_file:
            self.parse_tokens(line)
        input_file.close()
        self.rewind_token_list()
        self.save_tokens(output_file)

    def rewind_token_list(self):
        self.token_position = 0

    def save_tokens(self, output_file):
        output_file.write('<tokens>\n')
        while self.has_more_tokens():
            token, type  = self.advance()
            self.print_xml_token(output_file, token, type)
        output_file.write('</tokens>\n')
        self.rewind_token_list()

    def add_token(self, token):
        self.token_list.append(token)
        self.token_type.append(self.get_token_type(token))

    def print_xml_token(self, output_file, token, token_type):
        if token_type == 'KEYWORD':
            output_file.write('<keyword> {0} </keyword>\n'.format(token))
        if token_type == 'IDENTIFIER':
            output_file.write('<identifier> {0} </identifier>\n'.format(token))
        if token_type == 'SYMBOL':
            output_file.write('<symbol> {0} </symbol>\n'.format(token))
        if token_type == 'STRING_CONSTANT':
            output_file.write('<stringConstant> {0} </stringConstant>\n'.format(token[1:]))
        if token_type == 'INT_CONSTANT':
            output_file.write('<integerConstant> {0} </integerConstant>\n'.format(token))

    def parse_tokens(self, line):
        current_token = ""
        comment_line = re.search('^//', line)
        if comment_line is not None:
            return
        comment_line = re.search('^\s*\*|^\s*\/\*', line)
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
                    current_token = '"' + current_token
                    in_quoted_string = False
                else:
                    in_quoted_string = True


            if self.is_alpha(c) | self.is_digit(c):
                current_token = current_token + c

            if self.is_symbol(c):
                if len(current_token) > 0:
                    self.add_token(current_token)
                current_token = c
                self.add_token(current_token)
                current_token = ""

            if self.is_whitespace(c):
                if in_quoted_string:
                    current_token = current_token + c
                else:
                    if len(current_token) > 0:
                        self.add_token(current_token)
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
        token_type = self.token_type[self.token_position]
        if give_token == '&':
            # Ampersand needs to be &amp; for XML/Web
            give_token = '&amp;'
        if give_token == '<':
            # < needs to be &lt; for XML/Web
            give_token = '&lt;'
        if give_token == '>':
            # > needs to be &gt; for XML/Web
            give_token = '&gt;'
        self.token_position = self.token_position + 1
        if token_type == "STRING_CONSTANT":
            return give_token[1:], token_type
        else:
            return give_token, token_type

    def get_token_type(self, token):
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
        print("Compiling...")
        while self.tokenizer.has_more_tokens():
            self.current_token, token_type = self.tokenizer.advance()
            # print(self.current_token, token_type)
            if self.current_token == 'class':
                self.compileClass()

            if self.current_token == 'while':
                self.compileWhileStatement()

    def compileTerm(self):
        if self.tokey_type != "SYMBOL":
            print("<term>")
            print(self.current_token)
            self.eat(self.current_token)
            print("<term>")

    def compileExpression(self):
        print("<expression>")
        self.compileTerm()
        self.advance()
        if self.token_type == "SYMBOL":
            print("<symbol>", self.current_token, "</symbol>")
            self.eat(self.current_token)
            self.compileTerm()
        print("</expression>")


    def advance(self):
        if self.tokenizer.has_more_tokens():
            self.current_token, self.token_type = self.tokenizer.advance()

    def compileClass(self):
        print("<class>")
        self.eat("class")

        print("</class>")

    def compileClassVarDec(self):
        print("compile class variable declarations")

    def compileSubroutine(self):
        print("compile subroutine")

    def compileParameterList(self):
        print("compile parameter list")

    def compileVarDec(self):
        print("compile variable declaration")

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
            print("<symbol> ( </symbol>")
        else:
            print("Error processing while statement >> while", self.current_token)
            exit(-1)
        self.compileExpression()
        print("</whileStatement>")

    def eat(self, test_token):
        if self.current_token == test_token:
            if self.tokenizer.has_more_tokens():
                self.current_token, self.token_type = self.tokenizer.advance()
            return True
        else:
            return False



# Main program.
if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " dir | jack_prog.jack")
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


