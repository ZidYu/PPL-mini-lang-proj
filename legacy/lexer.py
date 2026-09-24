from enum import Enum, auto


class TokenType(Enum):
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    KEYWORD = auto()

    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()

    EQUALS = auto()
    DOUBLE_EQUALS = auto()
    NOT_EQUALS = auto()
    GREATER = auto()
    LESS = auto()
    GREATER_EQUALS = auto()
    LESS_EQUALS = auto()

    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    COLON = auto()

    NEWLINE = auto()
    EOF = auto()


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.value is not None:
            return f"{self.type.name}:{self.value}"
        return self.type.name


KEYWORDS = [
    "let",
    "if",
    "else",
    "while",
    "function",
    "return",
    "print",
    "true",
    "false",
    "end"
]


class Lexer:
    def __init__(self, text):
        self.text = text.replace("\r\n", "\n").replace("\r", "\n")
        self.pos = 0
        self.current_char = self.text[0] if self.text else None

    def advance(self):
        self.pos += 1

        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def tokenize(self):
        tokens = []

        while self.current_char is not None:

            if self.current_char in " \t":
                self.advance()
                continue

            if self.current_char == "\n":
                tokens.append(Token(TokenType.NEWLINE))
                self.advance()
                continue

            if self.current_char == "#":
                while self.current_char is not None and self.current_char != "\n":
                    self.advance()
                continue

            if self.current_char.isdigit():
                tokens.append(self.make_number())
                continue

            if self.current_char.isalpha() or self.current_char == "_":
                tokens.append(self.make_identifier())
                continue

            if self.current_char == '"':
                tokens.append(self.make_string())
                continue

            if self.current_char == "+":
                tokens.append(Token(TokenType.PLUS))
                self.advance()
                continue

            if self.current_char == "-":
                tokens.append(Token(TokenType.MINUS))
                self.advance()
                continue

            if self.current_char == "*":
                tokens.append(Token(TokenType.MUL))
                self.advance()
                continue

            if self.current_char == "/":
                tokens.append(Token(TokenType.DIV))
                self.advance()
                continue

            if self.current_char == "=":
                self.advance()

                if self.current_char == "=":
                    tokens.append(Token(TokenType.DOUBLE_EQUALS))
                    self.advance()
                else:
                    tokens.append(Token(TokenType.EQUALS))

                continue

            if self.current_char == "!":
                self.advance()

                if self.current_char == "=":
                    tokens.append(Token(TokenType.NOT_EQUALS))
                    self.advance()
                else:
                    raise Exception("Expected '=' after '!'")

                continue

            if self.current_char == ">":
                self.advance()

                if self.current_char == "=":
                    tokens.append(Token(TokenType.GREATER_EQUALS))
                    self.advance()
                else:
                    tokens.append(Token(TokenType.GREATER))

                continue

            if self.current_char == "<":
                self.advance()

                if self.current_char == "=":
                    tokens.append(Token(TokenType.LESS_EQUALS))
                    self.advance()
                else:
                    tokens.append(Token(TokenType.LESS))

                continue

            if self.current_char == "(":
                tokens.append(Token(TokenType.LPAREN))
                self.advance()
                continue

            if self.current_char == ")":
                tokens.append(Token(TokenType.RPAREN))
                self.advance()
                continue

            if self.current_char == ",":
                tokens.append(Token(TokenType.COMMA))
                self.advance()
                continue

            if self.current_char == ":":
                tokens.append(Token(TokenType.COLON))
                self.advance()
                continue

            raise Exception(f"Illegal character: {self.current_char}")

        tokens.append(Token(TokenType.EOF))
        return tokens

    def make_number(self):
        number = ""

        while self.current_char is not None and self.current_char.isdigit():
            number += self.current_char
            self.advance()

        return Token(TokenType.NUMBER, int(number))

    def make_identifier(self):
        name = ""

        while (
            self.current_char is not None
            and (self.current_char.isalnum() or self.current_char == "_")
        ):
            name += self.current_char
            self.advance()

        if name in KEYWORDS:
            return Token(TokenType.KEYWORD, name)

        return Token(TokenType.IDENTIFIER, name)

    def make_string(self):
        self.advance()
        value = ""

        while self.current_char is not None and self.current_char != '"':
            value += self.current_char
            self.advance()

        if self.current_char is None:
            raise Exception("Unclosed string")

        self.advance()
        return Token(TokenType.STRING, value)
