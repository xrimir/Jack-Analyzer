class CompilationEngine:
    def __init__(self, out_filename, tokens):
        self.out_filename = out_filename
        self.xml_file = open(self.out_filename, 'w')
        self.current_token = None
        self.current_token_value = None
        self.current_token_type = None
        self.current_token_index = 0
        self.tokens = tokens

    def write_to_output(self, text):
        self.xml_file.write(text + "\n")

    def set_token_value(self):
        self.current_token_value = self.current_token.split(">")[1].split("<")[0]

    def compile_all(self):
        while len(self.tokens) > self.current_token_index:
            self.get_next_token()
            self.compile_while_statement()
        self.xml_file.close()

    def get_next_token(self):
        self.current_token = self.tokens[self.current_token_index]['token']
        self.current_token_type = self.tokens[self.current_token_index]['type']
        self.set_token_value()
        self.current_token_index += 1
        print(self.current_token, self.current_token_type)

    ####################################################

    def compile_statements(self):
        self.get_next_token()
        while True:
            if self.current_token_value == "let":
                self.compile_let_statement()
            elif self.current_token_value == "if":
                self.compile_if_statement()
            elif self.current_token_value == "while":
                self.compile_while_statement()
            if self.current_token_value == "}" or self.current_token_value == ";":
                break

    def compile_if_statement(self):
        if self.current_token_value == "if":
            self.write_to_output("<ifStatement>")
            self.write_to_output("<if>")
            self.get_next_token()
            if self.current_token_value == "(":
                self.write_to_output(self.current_token)
                self.get_next_token()
                if self.current_token_value != ")":
                    self.compile_expression()
                    self.get_next_token()
                    if self.current_token_value == ")":
                        self.write_to_output(self.current_token)
                        self.get_next_token()
                        if self.current_token_value == "{":
                            self.write_to_output(self.current_token)
                            self.compile_statements()
                            if self.current_token_value == "}":
                                self.write_to_output(self.current_token)
                                self.get_next_token()
            self.write_to_output("</if>")
            self.write_to_output("</ifStatement>")


    def compile_while_statement(self):
        if self.current_token_value == "while":
            self.write_to_output("<whileStatement>")
            self.write_to_output("<while>")
            self.get_next_token()
            if self.current_token_value == "(":
                self.write_to_output(self.current_token)
                self.get_next_token()
                if self.current_token_value != ")":
                    self.compile_expression()
                    self.get_next_token()
                    if self.current_token_value == ")":
                        self.write_to_output(self.current_token)
                        self.get_next_token()
                        if self.current_token_value == "{":
                            self.write_to_output(self.current_token)
                            self.compile_statements()
                            if self.current_token_value == "}":
                                self.write_to_output(self.current_token)
                                self.get_next_token()
            self.write_to_output("</while>")
            self.write_to_output("</whileStatement>")

    def compile_let_statement(self):
        if self.current_token_value == "let":
            self.write_to_output("<letStatement>")
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

    ####################################################
    def compile_expression(self):
        self.get_next_token()

    def compile_expression_list(self):
        pass

    def compile_term(self):
        if self.current_token_type == "STRING_CONSTANT":
            pass
        elif self.current_token_type == "INT_CONSTANT":
            pass

    def compile_constant(self):
        pass

    def compile_op(self):
        pass

    def compile_do(self):
        pass

    def compile_return(self):
        pass

    def compile_class(self):
        pass

    def compile_class_var_dec(self):
        pass

    def compile_subroutine_dec(self):
        pass

    def compile_parameter_list(self):
        pass

    def compile_subroutine_body(self):
        pass