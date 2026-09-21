from lexer import Lexer
from parser import Parser
from interpreter import Interpreter, Environment


code = """
let x = 5
let name = "Jasmin"
let passed = true

print(x)
print(name)
print(passed)

if x > 3:
    print("x is greater than 3")
else:
    print("x is not greater than 3")
end

while x < 8:
    print(x)
    x = x + 1
end

function add(a, b):
    return a + b
end

let result = add(5, 3)
print(result)
"""


lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
tree = parser.parse()

interpreter = Interpreter()
environment = Environment()

interpreter.run(tree, environment)