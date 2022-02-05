import sys
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine


class JackAnalyzer:
    def __init__(self, file):
        self.filename = file
        self.output_filename = filename.replace(".jack", ".xml")

    def analyze_file(self):
        tokenizer = JackTokenizer(filename)
        tokenizer.init_file()
        while tokenizer.has_more_tokens():
            tokenizer.advance()
            tokenizer.load_next_token()
        tokenizer.jack_file.close()
        comp_engine = CompilationEngine(self.output_filename, tokenizer.result)
        comp_engine.compile_all()


filename = sys.argv[-1]
jackAnalyzer = JackAnalyzer(filename)
jackAnalyzer.analyze_file()
