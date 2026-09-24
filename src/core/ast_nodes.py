from dataclasses import dataclass

@dataclass
class Literal: value: object
@dataclass
class Variable: name: str
@dataclass
class Binary: left: object; operator: str; right: object
@dataclass
class Unary: operator: str; operand: object
@dataclass
class Logical: left: object; operator: str; right: object
@dataclass
class Call: callee: object; arguments: list
@dataclass
class VarDeclaration: name: str; initializer: object
@dataclass
class Assignment: name: str; value: object
@dataclass
class ExpressionStatement: expression: object
@dataclass
class PrintStatement: expression: object
@dataclass
class Block: statements: list
@dataclass
class IfStatement: condition: object; then_branch: object; else_branch: object = None
@dataclass
class WhileStatement: condition: object; body: object
@dataclass
class FunctionStatement: name: str; params: list; body: object
@dataclass
class ReturnStatement: value: object
