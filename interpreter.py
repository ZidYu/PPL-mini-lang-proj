from lexer import TokenType
from parser import (
    NumberNode,
    StringNode,
    BooleanNode,
    VarAccessNode,
    VarAssignNode,
    BinaryOpNode,
    PrintNode,
    IfNode,
    WhileNode,
    FunctionNode,
    CallNode,
    ReturnNode
)


class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def set(self, name, value):
        self.variables[name] = value

    def get(self, name):
        if name in self.variables:
            return self.variables[name]

        if self.parent:
            return self.parent.get(name)

        raise Exception(f"Undefined variable: {name}")

    def assign(self, name, value):
        if name in self.variables:
            self.variables[name] = value
            return

        if self.parent:
            self.parent.assign(name, value)
            return

        raise Exception(f"Undefined variable: {name}")


class Function:
    def __init__(self, node, environment):
        self.node = node
        self.environment = environment


class ReturnException(Exception):
    def __init__(self, value):
        self.value = value


class Interpreter:

    def visit(self, node, environment):

        if isinstance(node, NumberNode):
            return node.value

        if isinstance(node, StringNode):
            return node.value

        if isinstance(node, BooleanNode):
            return node.value

        if isinstance(node, VarAccessNode):
            return environment.get(node.name)

        if isinstance(node, VarAssignNode):
            value = self.visit(node.value, environment)

            environment.set(node.name, value)

            return value

        if isinstance(node, PrintNode):
            value = self.visit(node.value, environment)

            print(value)

            return None

        if isinstance(node, BinaryOpNode):
            return self.visit_binary(node, environment)

        if isinstance(node, IfNode):
            condition = self.visit(node.condition, environment)

            if not isinstance(condition, bool):
                raise Exception("If condition must be true or false")

            if condition:
                child_environment = Environment(environment)

                for statement in node.body:
                    self.visit(statement, child_environment)

            else:
                child_environment = Environment(environment)

                for statement in node.else_body:
                    self.visit(statement, child_environment)

            return None

        if isinstance(node, WhileNode):
            while True:
                condition = self.visit(node.condition, environment)

                if not isinstance(condition, bool):
                    raise Exception("While condition must be true or false")

                if not condition:
                    break

                child_environment = Environment(environment)

                for statement in node.body:
                    self.visit(statement, child_environment)

            return None

        if isinstance(node, FunctionNode):
            function = Function(node, environment)

            environment.set(node.name, function)

            return None

        if isinstance(node, CallNode):
            return self.call_function(node, environment)

        if isinstance(node, ReturnNode):
            value = self.visit(node.value, environment)
            raise ReturnException(value)

        raise Exception("Unknown node")

    def visit_binary(self, node, environment):
        left = self.visit(node.left, environment)
        right = self.visit(node.right, environment)

        if node.operator == TokenType.PLUS:
            if type(left) != type(right):
                raise Exception("Both values must have the same type")

            if not isinstance(left, (int, str)):
                raise Exception("Invalid values for '+'")

            return left + right

        if node.operator == TokenType.MINUS:
            self.check_numbers(left, right)
            return left - right

        if node.operator == TokenType.MUL:
            self.check_numbers(left, right)
            return left * right

        if node.operator == TokenType.DIV:
            self.check_numbers(left, right)

            if right == 0:
                raise Exception("Cannot divide by zero")

            return left // right

        if node.operator == TokenType.DOUBLE_EQUALS:
            return type(left) == type(right) and left == right

        if node.operator == TokenType.NOT_EQUALS:
            return type(left) != type(right) or left != right

        if node.operator == TokenType.GREATER:
            self.check_numbers(left, right)
            return left > right

        if node.operator == TokenType.LESS:
            self.check_numbers(left, right)
            return left < right

        if node.operator == TokenType.GREATER_EQUALS:
            self.check_numbers(left, right)
            return left >= right

        if node.operator == TokenType.LESS_EQUALS:
            self.check_numbers(left, right)
            return left <= right

        raise Exception("Unknown operator")

    def check_numbers(self, left, right):
        if not isinstance(left, int) or isinstance(left, bool):
            raise Exception("Both values must be numbers")

        if not isinstance(right, int) or isinstance(right, bool):
            raise Exception("Both values must be numbers")

    def call_function(self, node, environment):
        function = environment.get(node.name)

        if not isinstance(function, Function):
            raise Exception(f"{node.name} is not a function")

        if len(node.arguments) != len(function.node.parameters):
            raise Exception("Incorrect number of arguments")

        values = []

        for argument in node.arguments:
            values.append(self.visit(argument, environment))

        function_environment = Environment(function.environment)

        for i in range(len(function.node.parameters)):
            parameter = function.node.parameters[i]
            function_environment.set(parameter, values[i])

        try:
            for statement in function.node.body:
                self.visit(statement, function_environment)

        except ReturnException as result:
            return result.value

        return None

    def run(self, nodes, environment):
        result = None

        for node in nodes:
            result = self.visit(node, environment)

        return result
    