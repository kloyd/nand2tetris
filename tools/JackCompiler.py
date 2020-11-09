import glob
import sys
import re


class JackTokenizer:

    keyword_list = ['class', 'constructor', 'method', 'function', 'field', 'static', 'var', 'int', 'char', 'boolean',
                    'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
    symbols_list = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '-', '~']
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ?:'
    digits = '0123456789'
    whitespaces = ' \r\n\t'
    token_list = []
    token_type = []
    token_position = 0

    def __init__(self, input_file):
        current_token = ""
        self.token_list = []
        self.token_type = []
        for line in input_file:
            self.parse_tokens(line)
        input_file.close()
        self.rewind_token_list()
        #self.save_tokens(filename)

    def rewind_token_list(self):
        self.token_position = 0

    def save_tokens(self, filename):
        output_filename = filename.split('.')[0] + "T.xml"
        output_file = open(output_filename, 'w')
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

            if self.is_symbol(c) and not in_quoted_string:
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

    def look_ahead(self):
        next_pos = self.token_position
        if next_pos < len(self.token_list):
            # there is one more.
            return self.token_list[next_pos]
        else:
            return "None"

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
            return "symbol"
        if token in self.keyword_list:
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


class Variable:
    
    def __init__(self, var_name, var_type, index):
        self.var_name = var_name
        self.var_type = var_type
        self.var_index = index
     
    def get_type(self):
        return self.var_type
        
    def get_name(self):
        return self.var_name
    
    def get_index(self):
        return self.var_index


class SymbolTable:
    def __init__(self):
        self.statics = {}
        self.fields = {}
        self.args = {}
        self.locals ={}

    def start_subroutine(self):
        self.args = {}
        self.locals = {}

    def var_count(self, kind):
        count = 0
        if kind == "static":
            count = len(self.statics)
        if kind == "field":
            count = len(self.fields)
        if kind == "argument":
            count = len(self.args)
        if kind == "local":
            count = len(self.locals)
        return count

    def define_var(self, name, var_type, kind):
        var_index = self.var_count(kind)
        the_var = Variable('','',0)
        if kind == "static":
            the_var = Variable(name, var_type, var_index)
            self.statics[name] = the_var
        if kind == "field":
            the_var = Variable(name, var_type, var_index)
            self.fields[name] = the_var
        if kind == "argument":
            the_var = Variable(name, var_type, var_index)
            self.args[name] = the_var
        if kind == "local":
            the_var = Variable(name, var_type, var_index)
            self.locals[name] = the_var
        # print(kind + " variable - " + the_var.get_name() + ", type: " + the_var.get_type() + ", index: ", the_var.get_index())

    def kind_of(self, name):
        kind = "none"
        if name in self.locals:
            kind = "local"
        if name in self.args:
            kind = "argument"
        if name in self.fields:
            kind = "field"
        if name in self.statics:
            kind = "static"
        return kind

    def exists(self, name):
        kind = self.kind_of(name)
        if kind == "none":
            return False
        else:
            return True

    def type_of(self, name):
        kind = self.kind_of(name)
        the_var = Variable('n', 'n', 0)
        if kind == "local":
            the_var = self.locals.get(name)
        if kind == "argument":
            the_var = self.args.get(name)
        if kind == "field":
            the_var = self.fields.get(name)
        if kind == "static":
            the_var = self.statics.get(name)
        return the_var.get_type()

    def index_of(self, name):
        kind = self.kind_of(name)
        the_var = Variable('n', 'n', 0)
        if kind == "local":
            the_var = self.locals.get(name)
        if kind == "argument":
            the_var = self.args.get(name)
        if kind == "field":
            the_var = self.fields.get(name)
        if kind == "static":
            the_var = self.statics.get(name)

        if the_var is None:
            return 0
        else:
            return the_var.get_index()


class VMWriter:
    def __init__(self, output_file):
        self.vmFile = output_file

    def write_push(self, segment, index):
        self.vmFile.write("push " + segment + " " + str(index))
        self.vmFile.write("\n")

    def write_pop(self, segment, index):
        self.vmFile.write("pop " + segment + " " + str(index))
        self.vmFile.write("\n")

    def write_arithmetic(self, command):
        self.vmFile.write(command)
        self.vmFile.write("\n")

    def write_label(self, label):
        self.vmFile.write("label " + label)
        self.vmFile.write("\n")

    def write_goto(self, label):
        self.vmFile.write("goto " + label)
        self.vmFile.write("\n")

    def write_if(self, label):
        self.vmFile.write("if-goto " + label)
        self.vmFile.write("\n")

    def write_call(self, f_name, n_args):
        self.vmFile.write("call " + f_name + " " + str(n_args))
        self.vmFile.write("\n")

    def write_return(self):
        self.vmFile.write("return")
        self.vmFile.write("\n")

    def write_function(self, class_name, function_name, nargs):
        self.vmFile.write("function " + class_name + "." + function_name + " " + str(nargs))
        self.vmFile.write("\n")

    def close(self):
        self.vmFile.close()
        

class CompilationEngine:
    vmWriter: VMWriter
    symbol_table: SymbolTable
    # statement beginning tokens
    statement_list = ['if', 'let', 'while', 'return', 'do']
    operator_list = ['+', '-', '*', '/', '&', '|', '<', '>', '=', '-', '~', '=', '&lt;', '&gt;', '&amp;']
    type_list = ['int', 'char', 'boolean']
    # indentation for xml output. should go up when adding new element and down when done with element.
    indent_depth = 0

    def __init__(self, input_file, output_file, base_filename):
        self.indent_depth = 0
        self.tokenizer = JackTokenizer(input_file)
        self.vmWriter = VMWriter(output_file)
        self.xml_file = open(base_filename + ".xml", 'w')
        self.symbol_table = SymbolTable()
        self.token_type = ""
        self.current_token = ""
        self.class_name = ""

    def test_vmwriter(self):
        self.vmWriter.write_push("static", 0)
        self.vmWriter.write_pop("local", 1)
        self.vmWriter.write_arithmetic("add")
        self.vmWriter.write_call("String.length", 1)
        self.vmWriter.write_goto("somewhere")
        self.vmWriter.write_label("here")
        self.vmWriter.write_if("there")
        self.vmWriter.write_return()

    def run(self):

        while self.tokenizer.has_more_tokens():
            self.current_token, self.token_type = self.tokenizer.advance()
            if self.current_token == 'class':
                self.compile_class()
        self.vmWriter.close()
        self.xml_file.close()

    def output_variable_dec(self, var_name):
        self.increase_indent()
        self.output_tag("<variableDec>")
        self.increase_indent()
        self.output_tag("<kind> " + self.symbol_table.kind_of(var_name) + " </kind>")
        self.output_tag("<type> " + self.symbol_table.type_of(var_name) + " </type>")
        self.output_tag("<variableName> " + var_name + " </variableName>")
        self.output_tag("<position> " + str(self.symbol_table.index_of(var_name)) + " </position>")
        self.decrease_indent()
        self.output_tag("</variableDec>")
        self.decrease_indent()

    def compile_class(self):
        self.output_tag("<class>")
        self.increase_indent()
        self.output_tag("<" + self.token_type + "> class </" + self.token_type + ">")
        self.eat("class")
        self.symbol_table = SymbolTable()
        self.output_tag("<identifier> " + self.current_token + " </identifier>")
        self.class_name = self.current_token
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
        """
        static type varName |, varName|* ;
        field type varName |, varName|* ;
        """
        self.output_tag("<classVarDec>")
        self.increase_indent()
        self.output_element()
        # static / field
        var_category = self.current_token
        self.expect_token(var_type)
        self.advance()
        # type def
        var_type = self.current_token
        self.output_element()
        self.advance()
        # identifier for variable
        if self.token_type == "identifier":
            self.output_tag("<identifier> " + self.current_token + " </identifier>")
            var_name = self.current_token
            self.add_class_var(var_name, var_category, var_type)

            self.advance()
            self.output_element()
            # if followed by ',' - it is another variable of the same type.
            # go until ; symbol.
            while self.current_token != ";":
                self.advance()
                self.output_element()
                if self.token_type == "identifier":
                    var_name = self.current_token
                    self.add_class_var(var_name, var_category, var_type)
        self.decrease_indent()
        self.output_tag("</classVarDec>")

    def compile_subroutine(self, subroutine_type):
        # clean slate for method vars.
        self.symbol_table.start_subroutine()
        self.output_tag("<subroutineDec>")
        self.increase_indent()
        self.output_element()
        if subroutine_type == "method":
            self.add_method_var("this", "argument", self.class_name)
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
            self.output_element()  # self.output_tag("<symbol> ) </symbol>")
            self.eat(")")
            self.compile_subroutine_body()
            self.decrease_indent()
            self.output_tag("</subroutineDec>")

    def compile_parameter_list(self):
        """
        parameter list = type varName |, type varName | *
        :return:
        """
        if self.token_type != 'symbol':
            self.increase_indent()
            # type
            self.output_element()
            var_type = self.current_token
            self.advance()
            # varName
            var_name = self.current_token
            self.output_element()
            self.advance()
            self.add_method_var(var_name, "argument", var_type)
            while self.current_token == ',':
                # symbol ,
                self.output_element()
                self.advance()
                # type
                self.output_element()
                var_type = self.current_token
                self.advance()
                # varName
                var_name = self.current_token
                self.add_method_var(var_name, "argument", var_type)
                self.output_element()
                self.advance()
            self.decrease_indent()

    def compile_subroutine_body(self):
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

    def compile_var_dec(self):
        self.output_tag("<varDec>")
        self.increase_indent()
        # var
        self.output_element()
        self.advance()
        # type
        self.output_element()
        var_type = self.current_token
        self.advance()
        # go until ; symbol.
        while self.current_token != ";":
            # variable name.
            if self.token_type == "identifier":
                self.add_method_var(self.current_token, 'local', var_type)
            self.output_element()
            self.advance()
            # could be comma or semicolon.
            self.output_element()
            if self.current_token == ",":
                self.advance()

        self.decrease_indent()
        self.output_tag("</varDec>")

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

    def compile_if_statement(self):
        # if (expr) { statement(s) } [ else { statement(s) }
        self.output_tag("<ifStatement>")
        self.increase_indent()
        self.output_tag("<keyword> if </keyword>")
        # get first clause
        self.advance()
        # '(' <expr> ')'
        self.output_element()
        self.advance()  # move past (
        self.compile_expression()
        self.output_element()
        #self.output_tag("if expression done.")
        self.advance()          # move past )
        self.output_element()   # write out {
        self.advance()      # move up
        self.compile_statements()   # do the statements.
        # current token should be '}'
        self.expect_token('}')
        self.output_element()
        if self.look_ahead() == "else":
            # move past '}'
            self.advance()
            # ouput else
            self.output_element()
            # output {
            self.advance()
            self.output_element()
            #  move on to statement(s)
            self.advance()
            self.compile_statements()
            # compile_statements will leave the token pointer at '}'
            self.output_element()
        # output '}'
        #self.output_tag("after else clause")
        #self.output_element()
        self.decrease_indent()
        self.output_tag("</ifStatement>")

    def compile_while_statement(self):
        self.expect_token('while')
        self.output_tag("<whileStatement>")
        self.increase_indent()
        self.output_element()
        self.advance()
        self.output_element()
        self.advance()
        self.compile_expression()
        # handle )
        self.expect_token(')')
        self.output_element()
        self.advance()
        self.output_element()
        self.advance()
        self.compile_statements()
        self.output_element()
        self.decrease_indent()
        self.output_tag("</whileStatement>")

    def compile_do_statement(self):
        self.output_tag("<doStatement>")
        self.increase_indent()
        self.output_element()
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
        self.advance()
        while self.current_token != ";":
            self.compile_expression()
        self.output_element()
        self.decrease_indent()
        self.output_tag("</returnStatement>")

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

    def compile_expression_list(self):
        self.output_tag("<expressionList>")
        self.increase_indent()
        while self.current_token != ")":
            self.compile_expression()
            if self.current_token == ',':
                self.output_element()
                self.advance()
        self.decrease_indent()
        self.output_tag("</expressionList>")

    def term_expression(self):
        """
        The inner part of a term expression.
        Also usable from the "do" compile as a do can be do <identifier>.<identifier>(<expressionlist>);
        Or do <identifier>(<expressionlist>);
        """
        self.output_element()
        var_name = self.current_token
        #if self.symbol_table.exists(var_name):
        #    print("term expression " + var_name + " - push " + self.symbol_table.kind_of(var_name),  self.symbol_table.index_of(var_name))
        #else:
        #    self.output_tag("Found a var_name? " + var_name)
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
        if self.current_token == '(':
            # <identifier> '(' expressionList ')'
            self.output_element()
            self.advance()
            self.compile_expression_list()
            self.output_element()
        if self.current_token == '[':
            self.compile_array_sub()

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

    def advance(self):
        if self.tokenizer.has_more_tokens():
            self.current_token, self.token_type = self.tokenizer.advance()
            return True
        else:
            return False

    def look_ahead(self):
        return self.tokenizer.look_ahead()

    def eat(self, test_token):
        if self.current_token == test_token:
            if self.tokenizer.has_more_tokens():
                self.current_token, self.token_type = self.tokenizer.advance()
            return True
        else:
            return False

    def output_tag(self, element):
        output_string = self.indent_depth * " " + element
        self.xml_file.write(output_string)
        self.xml_file.write("\n")

    def output_element(self):
        output_string = "<" + self.token_type + "> " + self.current_token + " </" + self.token_type + ">"
        self.output_tag(output_string)

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

    def add_class_var(self, name, var_kind, var_type):
        self.symbol_table.define_var(name, var_type, var_kind)
        # Add Symbol Table item to XML output
        self.output_variable_dec(name)

    def add_method_var(self, name, var_kind, var_type):
        """
        argument category
        local category
        :param name:
        :param var_kind:
        :param var_type:
        :return:
        """
        self.symbol_table.define_var(name, var_type, var_kind)
        self.output_variable_dec(name)


# Jack Compiler.
# Compile a single File.
# Create a CompilationEngine with the source file stream and an output file stream.
# Run the Compile.
def compile_file(filename):
    print("... compiling " + filename + " ...\n")
    base_filename = filename.split('.')[0]
    output_filename = base_filename + ".vm"
    output_file = open(output_filename, 'w')
    source_file = open(filename)
    compiler = CompilationEngine(source_file, output_file, base_filename)
    compiler.run()


# Compile a directory of *.jack files.
def compile_directory(source_dir):
    for file in glob.glob(source_dir + "/*.jack"):
        compile_file(file)


# Compiler Main Entry point.
# Check arguments passed in.
if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " dir | jack_prog.jack")
    exit(-1)
source_filename = sys.argv[1]
# is this dir name or file name?
if source_filename.endswith('.jack'):
    compile_file(source_filename)
else:
    compile_directory(source_filename)



