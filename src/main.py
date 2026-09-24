import sys
from .core.lexer import Lexer, LexerError
from .core.parser import Parser, ParserError
from .core.interpreter import Interpreter
from .core.environment import RuntimeErrorPPL

def execute_source(source):
    tokens=Lexer(source).scan(); tree=Parser(tokens).parse(); return Interpreter().run(tree)
def main():
    source=open(sys.argv[1],encoding='utf-8').read() if len(sys.argv)>1 else sys.stdin.read()
    try:
        for line in execute_source(source): print(line)
    except (LexerError,ParserError,RuntimeErrorPPL) as e: print(f'Error: {e}')
if __name__=='__main__': main()
