# Group 10 - Mini Programming Language and Interpreter

Course: CSS125P - AM5

## Members
- Sanchez, Jasmin Ariane C.
- Sosa, Leon Gabriel
- Yu, Zidane Elric
- Espina, Felicity Ann

## Architecture
1. Lexer / Scanner: converts source code into tokens and reports illegal characters.
2. Recursive-descent Parser: converts tokens into AST nodes according to `GRAMMAR.md`.
3. Interpreter / Evaluator: executes the AST with lexical environments, runtime type checks, control flow, and functions.

## Supported features
- Variables: `let x = 5`
- Assignment: `x = x + 1`
- Numbers, strings, booleans
- Arithmetic and comparisons
- Logical operators: `and`, `or`, `!`
- `if` / `else` / `end`
- `while` / `end`
- Functions, parameters, calls, and return
- Function values and lexical closures
- Comments beginning with `#` or `//`
- Runtime errors for illegal characters, invalid syntax, undefined variables, type mismatches, invalid conditions, division by zero, and invalid calls

## How to run
1. Run the server in the terminal:

```bash
py server.py
```

2. Open the local web link shown in the terminal:

```text
http://127.0.0.1:8000
```

3. Run the test suite from the project directory:

```bash
py -m unittest discover -s tests -v
```

## Run
From the project directory:

```bash
python -m unittest discover -s tests -v
python -m src.main sample_program.txt
```

The language uses dynamic runtime typing. Conditions must evaluate to Boolean values. Numeric division returns a decimal result.

## Five PPL concepts
1. Formal grammar and syntax: documented in `GRAMMAR.md` and used by the parser.
2. Lexical scoping and environments: nested `Environment` objects resolve variables through parent scopes.
3. Type systems and semantics: runtime checks reject incompatible operations.
4. Control flow: conditional branching and while iteration are supported.
5. First-class functions: function values can be assigned and called; functions retain their defining environment.

## Limitations to disclose
This is an educational interpreter, not a production language. It has no optimizer, machine-code compiler, standard library, or industrial-scale test suite. The grammar and tests should be reviewed by the group against the professor's final rubric before submission.
