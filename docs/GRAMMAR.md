# Mini Language Grammar (EBNF-style)

program ::= statement* EOF
statement ::= declaration | assignment | print_statement | if_statement | while_statement | function_statement | return_statement | expression_statement

declaration ::= "let" IDENTIFIER "=" expression [";"]
assignment ::= IDENTIFIER "=" expression [";"]
print_statement ::= "print" ["("] expression [")"] [";"]
if_statement ::= "if" ["("] expression [")"] [":"] block ["else" ":" block] ("end" | "}")
while_statement ::= "while" ["("] expression [")"] [":"] block ("end" | "}")
function_statement ::= "function" IDENTIFIER "(" parameters? ")" [":"] block ("end" | "}")
return_statement ::= "return" expression [";"]
block ::= statement*
parameters ::= IDENTIFIER ("," IDENTIFIER)*

expression ::= logical_or
logical_or ::= logical_and ("or" logical_and)*
logical_and ::= equality ("and" equality)*
equality ::= comparison (("==" | "!=") comparison)*
comparison ::= term ((">" | "<" | ">=" | "<=") term)*
term ::= factor (("+" | "-") factor)*
factor ::= unary (("*" | "/") unary)*
unary ::= ("-" | "!") unary | call
call ::= primary ("(" arguments? ")")*
primary ::= NUMBER | STRING | "true" | "false" | IDENTIFIER | "(" expression ")"
arguments ::= expression ("," expression)*
