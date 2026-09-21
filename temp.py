from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, List

# LEXICAL ANALYSIS (Tokens & Scanner)
class TokenType(Enum):
    NUMBER = auto()
    IDENTIFIER = auto()
    KEYWORD = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    EQUALS = auto()
    DOUBLE_EQUALS = auto()
    GREATER = auto()

    # Syntax
    COLON = auto()
    EOF = auto()

class Token:
    def __init__(self, type_: TokenType, value: any = None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"[{self.type.name}:{self.value}]" if self.value is not None else f"[{self.type.name}]"

KEYWORDS = ["if", "end", "print"]

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def tokenize(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char in ' \t\n':
                self.advance()
            elif self.current_char.isdigit():
                tokens.append(self.make_number())
            elif self.current_char.isalpha():
                tokens.append(self.make_identifier())
            elif self.current_char == '+':
                tokens.append(Token(TokenType.PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TokenType.MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TokenType.MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TokenType.DIV))
                self.advance()
            elif self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(TokenType.DOUBLE_EQUALS))
                    self.advance()
                else:
                    tokens.append(Token(TokenType.EQUALS))
            elif self.current_char == '>':
                tokens.append(Token(TokenType.GREATER))
                self.advance()
            elif self.current_char == ':':
                tokens.append(Token(TokenType.COLON))
                self.advance()
            else:
                raise Exception(f"Lexical Error: Illegal Character '{self.current_char}'")

        tokens.append(Token(TokenType.EOF))
        return tokens

    def make_number(self):
        num_str = ''
        dot_count = 0
        while self.current_char is not None and self.current_char in '0123456789.':
            if self.current_char == '.':
                dot_count += 1
            num_str += self.current_char
            self.advance()
        return Token(TokenType.NUMBER, float(num_str) if dot_count > 0 else int(num_str))

    def make_identifier(self):
        id_str = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()
        if id_str in KEYWORDS:
            return Token(TokenType.KEYWORD, id_str)
        return Token(TokenType.IDENTIFIER, id_str)

# SYNTAX ANALYSIS (AST & Parser)
@dataclass
class NumberNode:
    value: Any

@dataclass
class BinaryOpNode:
    left: Any
    op: Any
    right: Any

@dataclass
class VarAssignNode:
    name: str
    value_node: Any

@dataclass
class VarAccessNode:
    name: str

@dataclass
class PrintNode:
    expr: Any

@dataclass
class IfNode:
    condition: Any
    body: List[Any]

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]

    def parse(self):
        if self.current_token.type == TokenType.EOF:
            return None
        return self.statement()

    def statement(self):
        # PRINT STATEMENT
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == "print":
            self.advance()
            return PrintNode(self.expr())

        # IF STATEMENT
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == "if":
            self.advance()
            condition = self.expr()
            if self.current_token.type != TokenType.COLON:
                raise Exception("Syntax Error: Expected ':' after if condition")
            self.advance() # consume ':'

            body = []
            while not (self.current_token.type == TokenType.KEYWORD and self.current_token.value == "end"):
                if self.current_token.type == TokenType.EOF:
                    raise Exception("Syntax Error: Missing 'end' for if statement")
                body.append(self.statement())

            self.advance() # consume 'end'
            return IfNode(condition, body)

        # VARIABLE ASSIGNMENT
        if self.current_token.type == TokenType.IDENTIFIER:
            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == TokenType.EQUALS:
                var_name = self.current_token.value
                self.advance() # consume ID
                self.advance() # consume '='
                return VarAssignNode(var_name, self.expr())

        return self.expr()

    def expr(self):
        node = self.math_expr()
        # Handle comparisons for 'if' conditions
        while self.current_token.type in (TokenType.DOUBLE_EQUALS, TokenType.GREATER):
            op = self.current_token
            self.advance()
            right = self.math_expr()
            node = BinaryOpNode(node, op, right)
        return node

    def math_expr(self):
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token
            self.advance()
            right = self.term()
            node = BinaryOpNode(node, op, right)
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            op = self.current_token
            self.advance()
            right = self.factor()
            node = BinaryOpNode(node, op, right)
        return node

    def factor(self):
        tok = self.current_token
        if tok.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(tok.value)
        elif tok.type == TokenType.IDENTIFIER:
            self.advance()
            return VarAccessNode(tok.value)
        raise Exception(f"Syntax Error: Expected number or identifier, got {tok}")

# INTERPRETER & ENVIRONMENT
class Environment:
    def __init__(self):
        self.variables = {}

    def set(self, name: str, value: any):
        self.variables[name] = value

    def get(self, name: str):
        if name not in self.variables:
            raise Exception(f"Runtime Error: Undefined variable '{name}'")
        return self.variables[name]

class Interpreter:
    def visit(self, node, env: Environment):
        match node:
            case NumberNode(value):
                return value

            case VarAccessNode(name):
                return env.get(name)

            case VarAssignNode(name, value_node):
                value = self.visit(value_node, env)
                env.set(name, value)
                return value

            case PrintNode(expr):
                value = self.visit(expr, env)
                print(value)
                return None

            case IfNode(condition, body):
                cond_val = self.visit(condition, env)
                if cond_val: # If condition is truthy
                    for stmt in body:
                        self.visit(stmt, env)
                return None

            case BinaryOpNode(left, op, right):
                left_val = self.visit(left, env)
                right_val = self.visit(right, env)

                if op.type == TokenType.PLUS: return left_val + right_val
                if op.type == TokenType.MINUS: return left_val - right_val
                if op.type == TokenType.MUL: return left_val * right_val
                if op.type == TokenType.DIV:
                    if right_val == 0: raise Exception("Runtime Error: Division by zero")
                    return left_val / right_val
                if op.type == TokenType.DOUBLE_EQUALS: return left_val == right_val
                if op.type == TokenType.GREATER: return left_val > right_val

            case None:
                return None

            case _:
                raise Exception(f"Runtime Error: Unknown node type {type(node).__name__}")

# REPL (Read-Eval-Print Loop)
def run_repl():
    global_env = Environment()
    print("Mini-Language REPL v1.0")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            text = input(">> ")
            if text.strip().lower() == "exit":
                break
            if not text.strip():
                continue

            # Pipeline execution
            lexer = Lexer(text)
            tokens = lexer.tokenize()

            parser = Parser(tokens)
            # We loop here to support multiple statements on a single line (or blocks via raw string input)
            while parser.current_token.type != TokenType.EOF:
                ast = parser.parse()
                interpreter = Interpreter()
                result = interpreter.visit(ast, global_env)

                # Only print raw output if it's a direct evaluation, not assignments/prints
                if result is not None and not isinstance(ast, (VarAssignNode, PrintNode, IfNode)):
                    print(result)

        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    run_repl()