import argparse
import sys

from interpreter import Environment, Interpreter
from lexer import Lexer
from parser import Parser


VERSION = "0.1.0"


def run_source(source, environment=None):
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    tree = parser.parse()

    interpreter = Interpreter()
    return interpreter.run(tree, environment or Environment())


def is_complete(source):
    depth = 0

    for token in Lexer(source).tokenize():
        if token.type.name == "KEYWORD" and token.value in ("if", "while", "function"):
            depth += 1
        elif token.type.name == "KEYWORD" and token.value == "end":
            depth -= 1

    return depth <= 0


def repl():
    print(f"Mini Language {VERSION}")
    print("Type exit or quit to close the interpreter.")

    environment = Environment()
    buffer = []

    while True:
        prompt = "... " if buffer else "mini> "

        try:
            line = input(prompt)
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
            run_source(source, environment)
        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)

        buffer = []


def read_file(path):
    with open(path, "r", encoding="utf-8") as source_file:
        return source_file.read()


def build_parser():
    parser = argparse.ArgumentParser(
        prog="mini",
        description="Run Mini language programs from Windows cmd, PowerShell, or a compiled executable.",
    )
    parser.add_argument("script", nargs="?", help="Mini source file to run.")
    parser.add_argument("-c", "--code", help="Run a Mini code string.")
    parser.add_argument("--version", action="store_true", help="Show the interpreter version.")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)

    if args.version:
        print(f"mini {VERSION}")
        return 0

    try:
        if args.code is not None:
            run_source(args.code)
            return 0

        if args.script:
            run_source(read_file(args.script))
            return 0

        return repl()
    except FileNotFoundError as exc:
        print(f"File not found: {exc.filename}", file=sys.stderr)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
