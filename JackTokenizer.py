class JackTokenizer:
    def __init__(self, filename):
        self.file = filename
        self.jack_file = open(self.file, "r")
        self.full_token = ""
        self.current_token = ""
        self.next_token = ""
        self.token_types = {
            "keyword": ("class", "constructor", "function", "method", "field", "static", "var",
                        "int", "char", "boolean", "void", "true", "false", "null", "this", "let",
                        "do", "if", "else", "while", "return"),
            "symbol": ("{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|",
                       "<", ">", "=", "~"),
            "intConstant": range(0, 32768),
            "identifier": "^[A-Za-z_]+[A-Za-z_0-9]+$"
        }
        self.string_flag = False
        self.symbols = []
        self.result = []

    def has_more_tokens(self):
        return bool(self.next_token)

    def load_next_token(self):
        letter = self.jack_file.read(1)
        while letter == "\n" or letter == "\t":
            letter = self.jack_file.read(1)
        self.next_token = letter

    def init_file(self):
        self.jack_file.seek(0, 0)
        self.load_next_token()

    def advance(self):
        self.current_token = self.next_token
        self.token_type()
        if len(self.symbols) > 1:
            last_symbols = f"{self.symbols[-2]}{self.symbols[-1]}"
            if last_symbols == "/*" or last_symbols == "//" or last_symbols == "**":
                self.ignore_comment(last_symbols)

    def token_adder(self, token_type, value, t_type=None):
        full_token = {
            "token": f"<{token_type}>{value}</{token_type}>",
            "type": t_type.upper()
        }
        full_token = full_token.copy()
        self.result.append(full_token)

    def token_type(self):
        if self.current_token != " ":
            if self.current_token in self.token_types['symbol']:
                self.symbols.append(self.current_token)
                if self.full_token in self.token_types["keyword"]:
                    token_type = self.token_types["keyword"][self.token_types["keyword"].index(self.full_token)]
                    self.token_adder("keyword", self.full_token, token_type)
                elif self.full_token.isdigit() and int(self.full_token) in self.token_types['intConstant']:
                    self.token_adder("intConstant", self.full_token, "INT_CONST")
                elif self.full_token and self.full_token[-1] == "\"" and not self.string_flag:
                    self.token_adder("strConstant", self.full_token.split("\"")[1], "STRING_CONST")
                elif self.full_token:
                    self.token_adder("identifier", self.full_token, "IDENTIFIER")
                self.full_token = ""
                if self.current_token == "<":
                    self.token_adder('symbol', "&lt;", "SYMBOL")
                elif self.current_token == ">":
                    self.token_adder('symbol', "&gt;", "SYMBOL")
                elif self.current_token == "&":
                    self.token_adder('symbol', "&amp;", "SYMBOL")
                else:
                    self.token_adder("symbol", self.current_token, "SYMBOL")
            else:
                if self.current_token == "\"":
                    if not self.string_flag:
                        self.string_flag = True
                    else:
                        self.string_flag = False
                self.full_token += self.current_token
        else:
            if self.full_token in self.token_types["keyword"]:
                token_type = self.token_types["keyword"][self.token_types["keyword"].index(self.full_token)]
                self.token_adder("keyword", self.full_token, token_type)
                self.full_token = ""
            elif self.full_token in self.token_types["symbol"]:
                self.symbols.append(self.current_token)
                if self.current_token == "<":
                    self.token_adder('symbol', "&lt;", "SYMBOL")
                elif self.current_token == ">":
                    self.token_adder('symbol', "&gt;", "SYMBOL")
                elif self.current_token == "&":
                    self.token_adder('symbol', "&amp;", "SYMBOL")
                else:
                    self.token_adder("symbol", self.current_token, "SYMBOL")
                self.full_token = ""
            elif self.full_token.isdigit() and int(self.full_token) in self.token_types['intConstant']:
                self.token_adder("intConstant", self.full_token, "INT_CONST")
                self.full_token = ""
            elif self.full_token and self.full_token[-1] == "\"" and not self.string_flag:
                self.token_adder("strConstant", self.full_token.split("\"")[1], "STRING_CONST")
                self.full_token = ""
            elif self.full_token and self.string_flag:
                self.full_token += self.current_token
            elif self.full_token:
                self.token_adder("identifier", self.full_token, "IDENTIFIER")
                self.full_token = ""

    def ignore_comment(self, last_symbols):
        if last_symbols == "/*":
            while self.next_token != "/":
                self.next_token = self.jack_file.read(1)
            self.result.pop()
            self.result.pop()
        elif last_symbols == "/**":
            while self.next_token != "/":
                self.next_token = self.jack_file.read(1)
            self.result.pop()
            self.result.pop()
            self.result.pop()
        elif last_symbols == "//":
            while self.next_token != "\n":
                self.next_token = self.jack_file.read(1)
            self.result.pop()
            self.result.pop()
        self.full_token = ""
        self.symbols.pop()
        self.symbols.pop()
