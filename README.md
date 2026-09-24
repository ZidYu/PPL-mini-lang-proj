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

## PPL concepts demonstrated

Run the complete demonstration with:

```bash
python -m src.main concepts_demo.txt
```

Expected output:

```text
factorial
120
12
```

The demonstration identifies and shows more than the required five concepts:

1. **Syntax and semantics**: `concepts_demo.txt` uses the grammar in `GRAMMAR.md`; the parser builds AST nodes and the interpreter gives them meaning.
2. **Variables and data types**: `number` is numeric, `enabled` is Boolean, and `message` is a string; `let` binds each value.
3. **Expressions and operators**: `n == 0`, `n - 1`, `n * factorial(...)`, and `enabled and number > 3` exercise comparison, arithmetic, and logical operators.
4. **Control structures**: `if`/`else` selects a branch, while the recursive function controls repeated computation.
5. **Functions/procedures**: `factorial` and `addOffset` accept parameters, return values, and are called as expressions.
6. **Recursion**: `factorial` calls itself until the base case `n == 0`.
7. **Scope and binding**: `addOffset` resolves `offset` from its defining environment through a lexical closure.
8. **Abstraction**: callers use `factorial` and `addOffset` without needing to know their implementation details.
9. **Modularity**: the lexer, parser, AST, environment, and interpreter are separate modules under `src/`.

The implementation also includes runtime exception handling for invalid syntax, undefined variables, type mismatches, invalid conditions, division by zero, and invalid function calls. These are reported as interpreter errors; the language does not currently provide a user-facing `try`/`catch` construct.

## Limitations to disclose
This is an educational interpreter, not a production language. It has no optimizer, machine-code compiler, standard library, or industrial-scale test suite. The grammar and tests should be reviewed by the group against the professor's final rubric before submission.
