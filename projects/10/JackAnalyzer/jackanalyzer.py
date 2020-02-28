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
        self.token_type = []
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
        if token_type == 'stringConstant':
            output_file.write('<stringConstant> {0} </stringConstant>\n'.format(token))
        if token_type == 'integerConstant':
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
        if token_type == "stringConstant":
            return give_token[1:], token_type
        else:
            return give_token, token_type

    def get_token_type(self, token):
        test_value = 99999

        if token in self.symbols_list:
            #print(token, "symbol")
            return "symbol"
        if token in self.keyword_list:
            #print(token, "keyword")
            return "keyword"
        if '"' in token:
            return "stringConstant"
        try:
            test_value = int(token)
        except ValueError:
            test_value = 99999
        if test_value < 99999:
            return "integerConstant"

        return "identifier"


class JackCompiler:

    # statement beginning tokens
    statement_list = ['if', 'let', 'while', 'return', 'do']
    operator_list = ['+', '-', '*', '/', '&', '|', '<', '>', '=', '-', '~', '=']
    # indentation for xml output. should go up when adding new element and down when done with element.
    indent_depth = 0

    def __init__(self, tokenizer, source_file):
        self.indent_depth = 0
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

    def increase_indent(self):
        self.indent_depth = self.indent_depth + 2

    def decrease_indent(self):
        self.indent_depth = self.indent_depth - 2
        if self.indent_depth < 0:
            self.indent_depth = 0

    def expect_token(self, check_token):
        if check_token != self.current_token:
            print("Compile Error: Expected token '" + check_token + "', but got '" + self.current_token + "'")
            exit(-1)

    def expects_type(self, token_type):
        if token_type != self.token_type:
            print("Compile Error: Expected token of type '" + token_type + "', but got '" + self.token_type + "'")
            exit(-1)

    def compile_term(self):
        """
        term := integerConstant | stringConstant | keywordConstant |
            varName | varName '[' expression ']' | subroutineCall |
            '(' expression ')' | unaryOp term
        :return:
        """
        self.output_tag("<term>")
        self.increase_indent()
        if self.token_type == "integerConstant" or self == "stringConstant":
            self.output_element()
            self.advance()
        else:
            if self.token_type != "symbol":
                # term = varName | constant | varName '[' expr ']'
                # varName = simplevar
                # varName = class.method(expr)
                #self.increase_indent()
                self.term_expression()
            else:
                if self.current_token == '(':
                    # handle '(' expression ')'
                    #self.increase_indent()
                    self.output_element()
                    self.advance()
                    self.compile_expression()
                    self.output_element()
                    self.advance()
                    #self.decrease_indent()
                else:
                    if self.current_token == '-' or self.current_token == '~':
                        # handle unaryOp
                        # unaryOp term
                        self.output_element()
                        self.advance()
                        self.compile_term()

        self.decrease_indent()
        self.output_tag("</term>")

    def term_expression(self):
        """
        The inner part of a term expression.
        Also usable from the "do" compile as a do can be do <identifier>.<identifier>(<expressionlist>);
        Or do <identifier>(<expressionlist>);
        """
        self.output_element()
        self.advance()
        # got a '.' ??? if so, it's an object var with method call.
        if self.current_token == ".":
            # handle method
            self.output_element()
            self.advance()
            # method
            self.output_element()
            self.advance()
            # (
            # self.output_tag("*** ( *** ")
            self.output_element()
            self.advance()
            self.compile_expression_list()
            self.output_element()
            # move past )
            self.advance()
        # ** end refactor
        if self.current_token == '[':
            self.compile_array_sub()

    def compile_expression_list(self):
        self.output_tag("<expressionList>")
        self.increase_indent()
        while self.current_token != ")":
            self.compile_expression()
            self.advance()
        self.decrease_indent()
        self.output_tag("</expressionList>")

    def compile_expression(self):
        # expression: term ( op term)
        # first term is mandatory. once first term compiled, look for op.
        self.output_tag("<expression>")
        self.increase_indent()
        self.compile_term()
        # term is done, look for operator.
        if self.current_token in self.operator_list:

            self.output_element()
            self.advance()
            self.compile_term()

        self.decrease_indent()
        self.output_tag("</expression>")

    def compile_class(self):
        self.output_tag("<class>")
        self.increase_indent()
        self.output_tag("<" + self.token_type + "> class </" + self.token_type + ">")
        self.eat("class")

        self.output_tag("<identifier> " + self.current_token + " </identifier>")
        self.advance()
        if self.eat("{"):
            self.output_tag("<symbol> { </symbol>")

            while self.current_token != "}":

                if self.current_token == "static":
                    self.compile_class_var_dec("static")

                if self.current_token == "field":
                    self.compile_class_var_dec("field")

                if self.current_token == "function":
                    self.compile_subroutine("function")

                if self.current_token == "method":
                    self.compile_subroutine("method")

                if self.current_token == "constructor":
                    self.compile_subroutine("constructor")

                if self.current_token == 'while':
                    self.compile_while_statement()

                #self.output_element(self.current_token)
                self.advance()

        self.output_tag("<symbol> } </symbol>")
        self.decrease_indent()
        self.output_tag("</class>")

    def compile_class_var_dec(self, var_type):
        self.output_tag("<classVarDec>")
        self.increase_indent()
        # static / field
        self.output_element()
        self.eat(var_type)
        # type def
        self.output_element()
        self.advance()
        # identifier for variable
        if self.token_type == "identifier":
            self.output_tag("<identifier> " + self.current_token + " </identifier>")
            self.advance()
            # close it... no allowance for multiples yet.
            if self.current_token == ";":
                self.output_element()  # self.output_tag("<symbol> ; </symbol>")
        self.decrease_indent()
        self.output_tag("</classVarDec>")

    def compile_var_dec(self):
        self.output_tag("<varDec>")
        self.increase_indent()
        # var
        self.output_element()
        self.advance()
        # type
        self.output_element()
        self.advance()
        # go until ; symbol.
        while self.current_token != ";":
            # variable name.
            self.output_element()
            self.advance()
            # could be comma or semicolon.
            self.output_element()
            if self.current_token == ",":
                self.advance()

        self.decrease_indent()
        self.output_tag("</varDec>")

    def compile_subroutine(self, subroutine_type):
        self.output_tag("<subroutineDec>")
        self.increase_indent()
        self.output_element()
        self.eat(subroutine_type)
        self.output_element()
        self.advance()
        self.output_element()
        self.advance()
        if self.eat("("):
            self.output_tag("<symbol> ( </symbol>")
            self.output_tag("<parameterList>")
            self.compile_parameter_list()
            self.output_tag("</parameterList>")
            self.output_element()  #self.output_tag("<symbol> ) </symbol>")
            self.eat(")")
            self.output_tag("<subroutineBody>")
            self.increase_indent()
            if self.eat("{"):
                self.output_tag("<symbol> { </symbol>")
            while 1:
                if self.current_token == "var":
                    self.compile_var_dec()
                else:
                    self.compile_statements()
                if self.current_token == "}":
                    break
                self.advance()
            # have arrived at closing brace '}'
            self.output_element()
            self.decrease_indent()
            self.output_tag("</subroutineBody>")
            self.decrease_indent()
            self.output_tag("</subroutineDec>")

    def compile_parameter_list(self):
        self.output_tag("compile parameter list")

    def compile_statements(self):
        self.output_tag("<statements>")
        self.increase_indent()
        while self.current_token in self.statement_list:
            if self.current_token == "if":
                self.compile_if_statement()
            if self.current_token == "while":
                self.compile_while_statement()
            if self.current_token == "let":
                self.compile_let_statement()
            if self.current_token == "do":
                self.compile_do_statement()
            if self.current_token == "return":
                self.compile_return_statement()

            self.advance()
        self.decrease_indent()
        self.output_tag("</statements>")

    def compile_do_statement(self):
        self.output_tag("<doStatement>")
        self.increase_indent()
        self.output_tag("<keyword> do </keyword>")
        #self.compile_expression()
        self.advance()
        self.term_expression()
        while self.current_token != ";":
            self.advance()
        self.output_element()
        self.decrease_indent()
        self.output_tag("</doStatement>")

    def compile_return_statement(self):
        self.output_tag("<returnStatement>")
        self.increase_indent()
        self.output_tag("<keyword> return </keyword>")
        while self.current_token != ";":
            self.advance()
        self.output_element()
        self.decrease_indent()
        self.output_tag("</returnStatement>")

    def compile_let_statement(self):
        """
        'let' varName('[' expression '])? '=' expression ';'
        term = varName | varName '[' expression ']'
        :return:
        """
        self.output_tag("<letStatement>")
        self.increase_indent()
        # output 'let'
        self.output_element()
        self.eat("let")
        # output varName
        # should be output_term?
        self.output_element()
        self.advance()
        # this could be '=' or '['

        if self.current_token == '[':
            self.compile_array_sub()

        #self.output_tag("Current token " + self.current_token)
        self.output_element()
        self.expect_token("=")
        self.advance()
        #self.output_tag("after equals, before expression " + self.current_token)
        self.compile_expression()
        self.output_element()
        self.decrease_indent()
        self.output_tag("</letStatement>")

    def compile_array_sub(self):
        # output [
        self.output_element()
        self.advance()
        # do the expression in []
        self.compile_expression()
        # output ']'
        self.output_element()
        self.advance()
        #self.output_element()
        #self.output_tag("compile_array_sub current token " + self.current_token)
        # move up to = sign.
        #self.advance()

    def compile_if_statement(self):
        # if (expr) { statement(s) } [ else { statement(s) }
        self.output_tag("<ifStatement>")
        self.increase_indent()
        self.output_tag("<keyword> if </keyword>")
        # get first clause
        self.advance()
        # '(' <expr> ')'
        self.output_element()
        self.advance() # move past (
        self.compile_expression()
        self.output_element()
        #self.output_tag("if expression done.")
        self.advance()          # move past )
        self.output_element()   # write out {
        self.advance()      # move up
        self.compile_statements()   # do the statements.
        # current token should be '}'
        self.expect_token('}')
        # move past }, check for else
        self.output_element()
        self.advance()
        if self.current_token == "else":
            self.output_element()
            self.advance()
            #self.output_tag("first part of if clause, current token: " + self.current_token)
            self.output_element()
            self.advance()
            self.compile_statements()
            #self.advance()
        # output '}'
        self.output_element()
        self.decrease_indent()
        self.output_tag("</ifStatement>")

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
        output_string = self.indent_depth * " " + element
        self.output_file.write(output_string)
        self.output_file.write("\n")
        print(output_string)

    def output_element(self):
        output_string = "<" + self.token_type + "> " + self.current_token + " </" + self.token_type + ">"
        self.output_tag(output_string)


# Main program.
if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " dir | jack_prog.jack")
    exit(-1)


def compile_file(source_file):
    tokenizer = JackTokenizer(source_file)
    print("Compiling " + source_file + " ...\n\n")
    compiler = JackCompiler(tokenizer, source_file)
    compiler.run()


def compile_directory(source_dir):
    for file in glob.glob(source_dir + "*.jack"):
        compile_file(file)


compareCounter = 1
returnCounter = 1

source_filename = sys.argv[1]
# is this dir name or file name?
if source_filename.endswith('.jack'):
    compile_file(source_filename)
else:
    compile_directory(source_filename)


