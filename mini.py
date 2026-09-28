import sys

from src.core.interpreter import Interpreter
from src.core.lexer import Lexer
from src.core.parser import Parser
from src.main import execute_source, main as run_file


VERSION = "0.1.0"


def is_complete(source):
    depth = 0
    for token in Lexer(source).scan():
        if token.kind in ("IF", "WHILE", "FUNCTION", "LBRACE"):
            depth += 1
        elif token.kind in ("END", "RBRACE"):
            depth -= 1
    return depth <= 0


def repl():
    print(f"Mini Language {VERSION}")
    print("Type exit or quit to close the interpreter.")
    interpreter = Interpreter()
    buffer = []

    while True:
        try:
            line = input("... " if buffer else "mini> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if not buffer and line.strip().lower() in ("exit", "quit"):
            return 0
        if not line.strip() and not buffer:
            continue

        buffer.append(line)
        source = "\n".join(buffer)
        if not is_complete(source):
            continue

        try:
            output_count = len(interpreter.outputs)
            interpreter.run(Parser(Lexer(source).scan()).parse())
            for output in interpreter.outputs[output_count:]:
                print(output)
        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)
        buffer = []


def main():
    args = sys.argv[1:]

    if args == ["--version"]:
        print(f"mini {VERSION}")
        return 0

    if args and args[0] in ("-c", "--code"):
        if len(args) != 2:
            print("Error: -c/--code requires a code string.", file=sys.stderr)
            return 2
        try:
            for line in execute_source(args[1]):
                print(line)
        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        return 0

    if not args:
        return repl()

    run_file()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
