from dataclasses import dataclass
from lexer import TokenType


@dataclass
class NumberNode:
    value: int


@dataclass
class StringNode:
    value: str


@dataclass
class BooleanNode:
    value: bool


@dataclass
class VarAccessNode:
    name: str


@dataclass
class VarAssignNode:
    name: str
    value: object


@dataclass
class BinaryOpNode:
    left: object
    operator: TokenType
    right: object


@dataclass
class PrintNode:
    value: object


@dataclass
class IfNode:
    condition: object
    body: list
    else_body: list


@dataclass
class WhileNode:
    condition: object
    body: list


@dataclass
class FunctionNode:
    name: str
    parameters: list
    body: list


@dataclass
class CallNode:
    name: str
    arguments: list


@dataclass
class ReturnNode:
    value: object


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0]

    def advance(self):
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.current_token = self.tokens[self.pos]

    def skip_newlines(self):
        while self.current_token.type == TokenType.NEWLINE:
            self.advance()

    def parse(self):
        statements = []

        self.skip_newlines()

        while self.current_token.type != TokenType.EOF:
            statements.append(self.statement())
            self.skip_newlines()

        return statements

    def statement(self):
        if self.current_token.type == TokenType.KEYWORD:

            if self.current_token.value == "let":
                return self.assignment()

            if self.current_token.value == "print":
                return self.print_statement()

            if self.current_token.value == "if":
                return self.if_statement()

            if self.current_token.value == "while":
                return self.while_statement()

            if self.current_token.value == "function":
                return self.function_statement()

            if self.current_token.value == "return":
                return self.return_statement()

        if self.current_token.type == TokenType.IDENTIFIER:
            if self.pos + 1 < len(self.tokens):
                if self.tokens[self.pos + 1].type == TokenType.EQUALS:
                    return self.assignment()

                if self.tokens[self.pos + 1].type == TokenType.LPAREN:
                    return self.expression()

        return self.expression()

    def assignment(self):
        if self.current_token.type == TokenType.KEYWORD:
            if self.current_token.value == "let":
                self.advance()

        if self.current_token.type != TokenType.IDENTIFIER:
            raise Exception("Expected variable name")

        name = self.current_token.value
        self.advance()

        if self.current_token.type != TokenType.EQUALS:
            raise Exception("Expected '='")

        self.advance()

        value = self.expression()

        return VarAssignNode(name, value)

    def print_statement(self):
        self.advance()

        value = self.expression()

        return PrintNode(value)

    def if_statement(self):
        self.advance()

        condition = self.expression()

        if self.current_token.type != TokenType.COLON:
            raise Exception("Expected ':' after if condition")

        self.advance()
        self.skip_newlines()

        body = []

        while not (
            self.current_token.type == TokenType.KEYWORD
            and self.current_token.value in ["else", "end"]
        ):
            if self.current_token.type == TokenType.EOF:
                raise Exception("Expected 'end'")

            body.append(self.statement())
            self.skip_newlines()

        else_body = []

        if (
            self.current_token.type == TokenType.KEYWORD
            and self.current_token.value == "else"
        ):
            self.advance()

            if self.current_token.type != TokenType.COLON:
                raise Exception("Expected ':' after else")

            self.advance()
            self.skip_newlines()

            while not (
                self.current_token.type == TokenType.KEYWORD
                and self.current_token.value == "end"
            ):
                if self.current_token.type == TokenType.EOF:
                    raise Exception("Expected 'end'")

                else_body.append(self.statement())
                self.skip_newlines()

        if not (
            self.current_token.type == TokenType.KEYWORD
            and self.current_token.value == "end"
        ):
            raise Exception("Expected 'end'")

        self.advance()

        return IfNode(condition, body, else_body)

    def while_statement(self):
        self.advance()

        condition = self.expression()

        if self.current_token.type != TokenType.COLON:
            raise Exception("Expected ':' after while condition")

        self.advance()
        self.skip_newlines()

        body = []

        while not (
            self.current_token.type == TokenType.KEYWORD
            and self.current_token.value == "end"
        ):
            if self.current_token.type == TokenType.EOF:
                raise Exception("Expected 'end'")

            body.append(self.statement())
            self.skip_newlines()

        self.advance()

        return WhileNode(condition, body)

    def function_statement(self):
        self.advance()

        if self.current_token.type != TokenType.IDENTIFIER:
            raise Exception("Expected function name")

        name = self.current_token.value
        self.advance()

        if self.current_token.type != TokenType.LPAREN:
            raise Exception("Expected '('")

        self.advance()

        parameters = []

        if self.current_token.type != TokenType.RPAREN:
            while True:
                if self.current_token.type != TokenType.IDENTIFIER:
                    raise Exception("Expected parameter name")

                parameters.append(self.current_token.value)
                self.advance()

                if self.current_token.type == TokenType.COMMA:
                    self.advance()
                    continue

                break

        if self.current_token.type != TokenType.RPAREN:
            raise Exception("Expected ')'")

        self.advance()

        if self.current_token.type != TokenType.COLON:
            raise Exception("Expected ':'")

        self.advance()
        self.skip_newlines()

        body = []

        while not (
            self.current_token.type == TokenType.KEYWORD
            and self.current_token.value == "end"
        ):
            if self.current_token.type == TokenType.EOF:
                raise Exception("Expected 'end'")

            body.append(self.statement())
            self.skip_newlines()

        self.advance()

        return FunctionNode(name, parameters, body)

    def return_statement(self):
        self.advance()

        value = self.expression()

        return ReturnNode(value)

    def expression(self):
        node = self.math_expression()

        while self.current_token.type in [
            TokenType.DOUBLE_EQUALS,
            TokenType.NOT_EQUALS,
            TokenType.GREATER,
            TokenType.LESS,
            TokenType.GREATER_EQUALS,
            TokenType.LESS_EQUALS
        ]:
            operator = self.current_token.type
            self.advance()

            right = self.math_expression()

            node = BinaryOpNode(node, operator, right)

        return node

    def math_expression(self):
        node = self.term()

        while self.current_token.type in [
            TokenType.PLUS,
            TokenType.MINUS
        ]:
            operator = self.current_token.type
            self.advance()

            right = self.term()

            node = BinaryOpNode(node, operator, right)

        return node

    def term(self):
        node = self.factor()

        while self.current_token.type in [
            TokenType.MUL,
            TokenType.DIV
        ]:
            operator = self.current_token.type
            self.advance()

            right = self.factor()

            node = BinaryOpNode(node, operator, right)

        return node

    def factor(self):
        token = self.current_token

        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(token.value)

        if token.type == TokenType.STRING:
            self.advance()
            return StringNode(token.value)

        if token.type == TokenType.KEYWORD:
            if token.value == "true":
                self.advance()
                return BooleanNode(True)

            if token.value == "false":
                self.advance()
                return BooleanNode(False)

        if token.type == TokenType.IDENTIFIER:
            name = token.value
            self.advance()

            if self.current_token.type == TokenType.LPAREN:
                return self.function_call(name)

            return VarAccessNode(name)

        if token.type == TokenType.LPAREN:
            self.advance()

            node = self.expression()

            if self.current_token.type != TokenType.RPAREN:
                raise Exception("Expected ')'")

            self.advance()

            return node

        raise Exception("Unexpected token")

    def function_call(self, name):
        self.advance()

        arguments = []

        if self.current_token.type != TokenType.RPAREN:
            while True:
                arguments.append(self.expression())

                if self.current_token.type == TokenType.COMMA:
                    self.advance()
                    continue

                break

        if self.current_token.type != TokenType.RPAREN:
            raise Exception("Expected ')'")

        self.advance()

        return CallNode(name, arguments)

    