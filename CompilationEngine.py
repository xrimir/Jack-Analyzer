import time


class CompilationEngine:
    def __init__(self, out_filename, tokens):
        self.out_filename = out_filename
        self.xml_file = open(self.out_filename, 'w')
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]['token']
        self.current_token_value = self.tokens[self.current_token_index]['type']
        self.current_token_type = None
        self.set_token_value()
        self.JACK_TYPES = ["INT", "CHAR", "BOOLEAN"]
        self.SUBROUTINE_TYPES = ["CONSTRUCTOR", "FUNCTION", "METHOD"]
        self.STATEMENT_TYPE = ['if', 'while', 'let', 'do', 'return']
        self.keyword = ("class", "constructor", "function", "method", "field", "static", "var",
                        "int", "char", "boolean", "void", "true", "false", "null", "this", "let",
                        "do", "if", "else", "while", "return")

    def write_to_output(self, text):
        self.xml_file.write(text + "\n")

    def set_token_value(self):
        self.current_token_value = self.current_token.split(">")[1].split("<")[0]

    def compile_all(self):
        self.compile_class()
        self.xml_file.close()

    def get_next_token(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]['token']
            self.current_token_type = self.tokens[self.current_token_index]['type']
            self.set_token_value()
            # print(f"---------> {self.current_token_index} {self.current_token} {len(self.tokens)}")

    ####################################################

    def compile_statements(self):
        self.write_to_output("<statements>")
        while True:
            print(self.current_token)
            if self.current_token_value == "let":
                self.compile_let_statement()
            elif self.current_token_value == "if":
                self.compile_if_statement()
            elif self.current_token_value == "while":
                self.compile_while_statement()
            elif self.current_token_value == "do":
                self.compile_do_statement()
            elif self.current_token_value == "return":
                self.compile_return_statement()
            elif self.current_token_value == "}" or self.current_token_value == ";":
                self.write_to_output("</statements>")
                break

    def compile_if_statement(self):
        if self.current_token_value == "if":
            self.write_to_output("<ifStatement>")
            self.write_to_output(self.current_token)
            self.get_next_token()
            if self.current_token_value == "(":
                self.write_to_output(self.current_token)
                self.get_next_token()
                if self.current_token_value != ")":
                    self.compile_expression()
                if self.current_token_value == ")":
                    self.write_to_output(self.current_token)
                    self.get_next_token()
                    if self.current_token_value == "{":
                        self.write_to_output(self.current_token)
                        self.get_next_token()
                        self.compile_statements()
                        print(f"COMPING {self.current_token}")
                        if self.current_token_value == "}":
                            self.write_to_output(self.current_token)
                            self.get_next_token()
                            if self.current_token_value == "else":
                                print(f"ELSE {self.current_token}")
                                self.write_to_output(self.current_token)
                                self.get_next_token()
                                if self.current_token_value == "{":
                                    self.write_to_output(self.current_token)
                                    self.get_next_token()
                                    self.compile_statements()
                                    if self.current_token_value == "}":
                                        self.write_to_output(self.current_token)
                                        self.get_next_token()
            self.write_to_output("</ifStatement>")

    def compile_while_statement(self):
        if self.current_token_value == "while":
            self.write_to_output("<whileStatement>")
            self.write_to_output(self.current_token)
            self.get_next_token()
            if self.current_token_value == "(":
                self.write_to_output(self.current_token)
                self.get_next_token()
                if self.current_token_value != ")":
                    self.compile_expression()
                if self.current_token_value == ")":
                    self.write_to_output(self.current_token)
                    self.get_next_token()
                    if self.current_token_value == "{":
                        self.write_to_output(self.current_token)
                        self.get_next_token()
                        self.compile_statements()
                        if self.current_token_value == "}":
                            self.write_to_output(self.current_token)
                            self.get_next_token()
            self.write_to_output("</whileStatement>")

    def compile_let_statement(self):
        if self.current_token_value == "let":
            self.write_to_output("<letStatement>")
            self.write_to_output(self.current_token)
            self.get_next_token()
            if self.current_token_type == "IDENTIFIER":
                self.write_to_output(self.current_token)
                self.get_next_token()
                if self.current_token_value == "=":
                    self.write_to_output(self.current_token)
                    self.get_next_token()
                    self.compile_expression()
                    if self.current_token_value == ";":
                        self.write_to_output(self.current_token)
                        self.get_next_token()
            self.write_to_output("</letStatement>")

    def compile_do_statement(self):
        if self.current_token_value == "do":
            self.write_to_output("<doStatement>")
            self.write_to_output(self.current_token)
            self.get_next_token()
            if self.current_token_type == "IDENTIFIER":
                self.write_to_output(self.current_token)
                self.get_next_token()
                if self.current_token_value == ".":
                    self.write_to_output(self.current_token)
                    self.get_next_token()
                    if self.current_token_type == "IDENTIFIER":
                        self.write_to_output(self.current_token)
                        self.get_next_token()
                if self.current_token_value == "(":
                    self.write_to_output(self.current_token)
                    self.get_next_token()
                    self.compile_expression_list()
                    if self.current_token_value == ")":
                        self.write_to_output(self.current_token)
                        self.get_next_token()
                        if self.current_token_value == ";":
                            self.write_to_output(self.current_token)
                            self.get_next_token()
                            self.write_to_output("</doStatement>")

    def compile_return_statement(self):
        if self.current_token_value == "return":
            self.write_to_output("<returnStatement>")
            self.write_to_output(self.current_token)
            self.get_next_token()
            if self.current_token_value != ";":
                self.compile_expression()
            if self.current_token_value == ";":
                self.write_to_output(self.current_token)
            self.write_to_output("</returnStatement>")
            self.get_next_token()

    ####################################################
    def compile_expression(self):
        self.write_to_output("<expression>")
        print(f"COMPILE_EXPRESSION {self.current_token}")
        if self.current_token_value != ")" and self.current_token_value != ";":
            self.compile_term()
        if self.current_token_value == ",":
            self.write_to_output("</expression>")
            self.write_to_output(self.current_token)
            self.get_next_token()
            return
        if self.current_token_value != ")" and self.current_token_value != ";" and self.current_token_type == "SYMBOL":
            self.write_to_output(self.current_token)
            self.get_next_token()
        if self.current_token_value != ")" and self.current_token_value != ";":
            self.compile_term()
        self.write_to_output("</expression>")

    def compile_expression_list(self):
        self.write_to_output("<expressionList>")
        while self.current_token_value != ")":
            self.compile_expression()
        self.write_to_output("</expressionList>")

    def compile_term(self):
        self.write_to_output("<term>")
        if self.current_token_type == "IDENTIFIER":
            self.write_to_output(self.current_token)
            self.get_next_token()
        elif self.current_token_type == "INT_CONST" or self.current_token_type == "STR_CONST":
            self.write_to_output(self.current_token)
            self.get_next_token()
        elif self.current_token_value in self.keyword:
            self.write_to_output(self.current_token)
            self.get_next_token()
        self.write_to_output("</term>")

    #####################################################
    def compile_class(self):
        self.write_to_output("<class>")
        if self.current_token_value == "class":
            self.write_to_output(self.current_token)
            self.get_next_token()
            if self.current_token_type == "IDENTIFIER":
                self.write_to_output(self.current_token)
                self.get_next_token()
                if self.current_token_value == "{":
                    self.write_to_output(self.current_token)
                    self.get_next_token()
                    self.compile_class_var_dec()
                    self.compile_subroutine_dec()
                    self.compile_class_var_dec()
                    self.compile_subroutine_dec()
                    if self.current_token_value == "}":
                        self.write_to_output(self.current_token)
        self.write_to_output("</class>")

    def compile_class_var_dec(self):
        while self.current_token_value == "static" or self.current_token_value == "field":
            if self.current_token_value == "static" or self.current_token_value == "field":
                self.write_to_output("<classVarDec>")
                self.write_to_output(self.current_token)
                self.get_next_token()
                if self.current_token_type in self.JACK_TYPES or self.current_token_type == "IDENTIFIER":
                    self.write_to_output(self.current_token)
                    self.get_next_token()
                    if self.current_token_type == "IDENTIFIER":
                        self.write_to_output(self.current_token)
                        self.get_next_token()
                        while self.current_token_value != ";":
                            print(self.current_token_value)
                            if self.current_token_value == ",":
                                self.write_to_output(self.current_token)
                                self.get_next_token()
                            if self.current_token_type == "IDENTIFIER":
                                self.write_to_output(self.current_token)
                                self.get_next_token()
                        if self.current_token_value == ";":
                            self.write_to_output(self.current_token)
                            self.get_next_token()
                            print(self.current_token)
                self.write_to_output("</classVarDec>")

    def compile_var_dec(self):
        if self.current_token_value == "var":
            self.write_to_output("<varDec>")
            self.write_to_output(self.current_token)
            self.get_next_token()
            if self.current_token_type == "IDENTIFIER" or self.current_token_type in self.JACK_TYPES:
                self.write_to_output(self.current_token)
                self.get_next_token()
                if self.current_token_type == "IDENTIFIER":
                    self.write_to_output(self.current_token)
                    self.get_next_token()
                    if self.current_token_value == ";":
                        self.write_to_output(self.current_token)
                        self.get_next_token()
            self.write_to_output("</varDec>")

    ### Functions, Methods, Constructors
    def compile_subroutine_dec(self):
        while self.current_token_type in self.SUBROUTINE_TYPES:
            self.write_to_output("<subroutineDec>")
            if self.current_token_type in self.SUBROUTINE_TYPES:
                self.write_to_output(self.current_token)
                self.get_next_token()
                print(self.current_token)
                print(self.current_token_type)
                if self.current_token_type in self.JACK_TYPES or self.current_token_type == "VOID" or self.current_token_type == "IDENTIFIER":
                    print(self.current_token_type)
                    self.write_to_output(self.current_token)
                    self.get_next_token()
                    if self.current_token_type == "IDENTIFIER":
                        self.write_to_output(self.current_token)
                        self.get_next_token()
                        if self.current_token_value == "(":
                            self.write_to_output(self.current_token)
                            self.get_next_token()
                            self.compile_parameter_list()
                            if self.current_token_value == ")":
                                self.write_to_output(self.current_token)
                                self.get_next_token()
                                if self.current_token_value == "{":
                                    self.compile_subroutine_body()
                                    self.get_next_token()
                                    if self.current_token_value == "}":
                                        self.get_next_token()
            self.write_to_output("</subroutineDec>")

    def compile_parameter_list(self):
        self.write_to_output("<parameterList>")
        while self.current_token_value != ")":
            if self.current_token_type == "IDENTIFIER" or self.current_token_type in self.JACK_TYPES:
                self.write_to_output(self.current_token)
                self.get_next_token()
            if self.current_token_value == ",":
                self.write_to_output(self.current_token)
                self.get_next_token()
        self.write_to_output("</parameterList>")

    def compile_subroutine_body(self):
        self.write_to_output("<subroutineBody>")
        self.write_to_output(self.current_token)
        self.get_next_token()

        while True:
            if self.current_token_value == "var":
                self.compile_var_dec()
            elif self.current_token_value in self.STATEMENT_TYPE:
                self.compile_statements()
            else:
                break
            if self.current_token_value == "}":
                self.write_to_output(self.current_token)

        self.write_to_output("</subroutineBody>")
