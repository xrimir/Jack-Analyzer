import sys
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine


class JackAnalyzer:
    def __init__(self, file):
        self.filename = file
        self.output_filename = filename.replace(".jack", ".xml")

    def analyze_file(self):
        tokenizer = JackTokenizer(filename)
        comp_engine = CompilationEngine()
        tokenizer.init_file()
        while tokenizer.has_more_tokens():
            tokenizer.advance()
            tokenizer.load_next_token()
        print(tokenizer.result)
        tokenizer.result.append('</tokens>')
        tokenizer.jack_file.close()


filename = sys.argv[-1]
jackAnalyzer = JackAnalyzer(filename)
jackAnalyzer.analyze_file()
