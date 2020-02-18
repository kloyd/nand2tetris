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
        output_filename = filename.split('.')[0] + "T.xml"
        output_file = open(output_filename, 'w')
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
        if token_type == 'keyword':
            output_file.write('<keyword> {0} </keyword>\n'.format(token))
        if token_type == 'identifier':
            output_file.write('<identifier> {0} </identifier>\n'.format(token))
        if token_type == 'symbol':
            output_file.write('<symbol> {0} </symbol>\n'.format(token))
        if token_type == 'string_constant':
            output_file.write('<stringConstant> {0} </stringConstant>\n'.format(token))
        if token_type == 'int_constant':
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
        if token_type == "string_constant":
            return give_token[1:], token_type
        else:
            return give_token, token_type

    def get_token_type(self, token):
        test_value = 99999

        if token in self.symbols_list:
            return "symbol"
        if token in self.keyword_list:
            return "keyword"
        if '"' in token:
            return "string_constant"
        try:
            test_value = int(token)
        except ValueError:
            test_value = 99999
        if test_value < 99999:
            return "int_constant"

        return "identifier"


class JackCompiler:

    def __init__(self, tokenizer, source_file):
        self.tokenizer = tokenizer
        self.token_type = ""
        self.current_token = ""
        output_filename = source_file.split('.')[0] + ".xml"
        self.output_file = open(output_filename, 'w')

    def run(self):
        while self.tokenizer.has_more_tokens():
            self.current_token, self.token_type = self.tokenizer.advance()
            if self.current_token == 'class':
                self.compile_class()

    def compile_term(self):
        if self.token_type != "symbol":
            self.output_tag("<term>")
            self.output_tag(self.current_token)
            self.eat(self.current_token)
            self.output_tag("<term>")

    def compile_expression(self):
        self.output_tag("<expression>")
        self.compile_term()
        self.advance()
        if self.token_type == "symbol":
            self.output_tag("<symbol>" + self.current_token + "</symbol>")
            self.eat(self.current_token)
            self.compile_term()
        self.output_tag("</expression>")

    def compile_class(self):
        self.output_tag("<class>")
        self.output_tag("  <" + self.token_type + "> class </" + self.token_type + ">")
        self.eat("class")

        self.output_tag("  <identifier> " + self.current_token + " </identifier>")
        self.advance()
        if self.eat("{"):
            self.output_tag("  <symbol> { </symbol>")

            while self.current_token != "}":

                if self.current_token == "static":
                    self.compile_class_var_dec()

                if self.current_token == "function":
                    self.compile_subroutine()

                if self.current_token == 'while':
                    self.compile_while_statement()

                #self.output_element(self.current_token)
                self.advance()

        self.output_tag("  <symbol> } </symbol>")
        self.output_tag("</class>")

    def compile_class_var_dec(self):
        self.output_tag("  <classVarDec>")
        while 1:
            self.output_tag("    <keyword> static </keyword>")
            self.eat("static")
            self.output_tag("    <keyword> " + self.current_token + " </keyword>")
            self.advance()
            if self.token_type == "identifier":
                self.output_tag("    <identifier> " + self.current_token + " </identifier>")
                self.advance()
                if self.current_token == ";":
                    self.output_tag("    <symbol> ; </symbol>")
                    self.advance()
            if self.eat("static"):
                continue
            else:
                break
        self.output_tag("  </classVarDec>")

    def compile_subroutine(self):
        self.output_tag("  <subroutineDec>")
        self.output_element(4)
        self.eat("function")
        self.output_element(4)
        self.advance()
        self.output_element(4)
        self.advance()
        if self.eat("("):
            self.output_tag("    <symbol> ( </symbol>")
            self.output_tag("    <parameterList>")
            # TODO: parameter list elements
            self.output_tag("    </parameterList>")
            self.output_tag("    <symbol> ) </symbol>")
            self.eat(")")
            self.output_tag("    <subroutineBody>")
            if self.eat("{"):
                self.output_tag("      <symbol> { </symbol>")

    def compile_parameter_list(self):
        self.output_tag("compile parameter list")

    def compile_var_dec(self):
        self.output_tag("compile variable declaration")

    def compile_statements(self):
        self.output_tag("compile statements")

    def compile_if_statement(self):
        self.output_tag("compile if statement")

    def compile_while_statement(self):
        if self.eat('while'):
            self.output_tag("<whileStatement>")
            self.output_tag("<keyword> while </keyword")
        else:
            print("Error processing while statement>> while", self.current_token)
            exit(-1)
        if self.eat('('):
            self.output_tag("<symbol> ( </symbol>")
        else:
            print("Error processing while statement >> while", self.current_token)
            exit(-1)
        self.compile_expression()
        self.output_tag("</whileStatement>")

    def advance(self):
        if self.tokenizer.has_more_tokens():
            self.current_token, self.token_type = self.tokenizer.advance()
            return True
        else:
            return False

    def eat(self, test_token):
        if self.current_token == test_token:
            if self.tokenizer.has_more_tokens():
                self.current_token, self.token_type = self.tokenizer.advance()
            return True
        else:
            return False

    def output_tag(self, element):
        self.output_file.write(element)
        self.output_file.write("\n")
        print(element)

    def output_element(self, depth):
        output_string = depth*" " + "<" + self.token_type + "> " + self.current_token + " </" + self.token_type + ">"
        self.output_file.write(output_string)
        self.output_file.write("\n")
        print(output_string)

# Main program.
if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " dir | jack_prog.jack")
    exit(-1)


def analyze_file(source_file):
    tokenizer = JackTokenizer(source_file)
    print("Compiling " + source_file + " ...")
    compiler = JackCompiler(tokenizer, source_file)
    compiler.run()


def analyze_directory(source_dir):
    for file in glob.glob(source_dir + "*.jack"):
        print(file)
        analyze_file(file)


compareCounter = 1
returnCounter = 1

source_filename = sys.argv[1]
# is this dir name or file name?
if source_filename.endswith('.jack'):
    analyze_file(source_filename)
else:
    analyze_directory(source_filename)


