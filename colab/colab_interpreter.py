from enum import Enum, auto
from dataclasses import dataclass
from typing import Any

class TokenType(Enum):
    NUMBER=auto(); IDENTIFIER=auto(); KEYWORD=auto(); PLUS=auto(); MINUS=auto(); MUL=auto(); DIV=auto(); EQUALS=auto(); DOUBLE_EQUALS=auto(); GREATER=auto(); LESS=auto(); LPAREN=auto(); RPAREN=auto(); COLON=auto(); EOF=auto()

@dataclass
class Token:
    type: TokenType
    value: Any = None
    def __repr__(self): return f"[{self.type.name}:{self.value}]" if self.value is not None else f"[{self.type.name}]"

KEYWORDS={"if","end","print"}
class LexerError(Exception): pass
class ParserError(Exception): pass
class RuntimeErrorPPL(Exception): pass

class Lexer:
    def __init__(self,text): self.text=text; self.pos=-1; self.current_char=None; self.advance()
    def advance(self):
        self.pos+=1; self.current_char=self.text[self.pos] if self.pos<len(self.text) else None
    def tokenize(self):
        out=[]
        while self.current_char is not None:
            c=self.current_char
            if c.isspace(): self.advance()
            elif c.isdigit(): out.append(self.number())
            elif c.isalpha() or c=='_': out.append(self.identifier())
            elif c in '+-*/': out.append(Token({'+' :TokenType.PLUS,'-':TokenType.MINUS,'*':TokenType.MUL,'/':TokenType.DIV}[c],c)); self.advance()
            elif c=='=':
                self.advance()
                if self.current_char=='=': out.append(Token(TokenType.DOUBLE_EQUALS,'==')); self.advance()
                else: out.append(Token(TokenType.EQUALS,'='))
            elif c in '><': out.append(Token(TokenType.GREATER if c=='>' else TokenType.LESS,c)); self.advance()
            elif c in '():': out.append(Token({'(':TokenType.LPAREN,')':TokenType.RPAREN,':':TokenType.COLON}[c],c)); self.advance()
            else: raise LexerError(f"Illegal character '{c}'")
        out.append(Token(TokenType.EOF)); return out
    def number(self):
        s=''; dots=0
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char=='.'):
            if self.current_char=='.': dots+=1
            if dots>1: raise LexerError('Invalid number format')
            s+=self.current_char; self.advance()
        return Token(TokenType.NUMBER,float(s) if dots else int(s))
    def identifier(self):
        s=''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char=='_'):
            s+=self.current_char; self.advance()
        return Token(TokenType.KEYWORD if s in KEYWORDS else TokenType.IDENTIFIER,s)

@dataclass
class NumberNode: value: Any
@dataclass
class BinaryOpNode: left: Any; op: Token; right: Any
@dataclass
class VarAssignNode: name: str; value_node: Any
@dataclass
class VarAccessNode: name: str
@dataclass
class PrintNode: expr: Any
@dataclass
class IfNode: condition: Any; body: list

class Parser:
    def __init__(self,tokens): self.tokens=tokens; self.pos=-1; self.current_token=None; self.advance()
    def advance(self): self.pos+=1; self.current_token=self.tokens[self.pos] if self.pos<len(self.tokens) else None
    def check(self,t,v=None): return self.current_token.type==t and (v is None or self.current_token.value==v)
    def expect(self,t,v=None,msg='Unexpected token'):
        if not self.check(t,v): raise ParserError(msg)
        x=self.current_token; self.advance(); return x
    def parse_program(self):
        result=[]
        while not self.check(TokenType.EOF): result.append(self.statement())
        return result
    def statement(self):
        if self.check(TokenType.KEYWORD,'print'): self.advance(); return PrintNode(self.expr())
        if self.check(TokenType.KEYWORD,'if'): return self.if_statement()
        if self.check(TokenType.IDENTIFIER) and self.pos+1<len(self.tokens) and self.tokens[self.pos+1].type==TokenType.EQUALS:
            name=self.current_token.value; self.advance(); self.advance(); return VarAssignNode(name,self.expr())
        return self.expr()
    def if_statement(self):
        self.expect(TokenType.KEYWORD,'if'); condition=self.expr(); self.expect(TokenType.COLON,msg="Expected ':' after if condition")
        body=[]
        while not self.check(TokenType.KEYWORD,'end'):
            if self.check(TokenType.EOF): raise ParserError("Missing 'end'")
            body.append(self.statement())
        self.advance(); return IfNode(condition,body)
    def expr(self):
        node=self.math_expr()
        while self.current_token.type in (TokenType.DOUBLE_EQUALS,TokenType.GREATER,TokenType.LESS):
            op=self.current_token; self.advance(); node=BinaryOpNode(node,op,self.math_expr())
        return node
    def math_expr(self):
        node=self.term()
        while self.current_token.type in (TokenType.PLUS,TokenType.MINUS):
            op=self.current_token; self.advance(); node=BinaryOpNode(node,op,self.term())
        return node
    def term(self):
        node=self.factor()
        while self.current_token.type in (TokenType.MUL,TokenType.DIV):
            op=self.current_token; self.advance(); node=BinaryOpNode(node,op,self.factor())
        return node
    def factor(self):
        t=self.current_token
        if t.type==TokenType.NUMBER: self.advance(); return NumberNode(t.value)
        if t.type==TokenType.IDENTIFIER: self.advance(); return VarAccessNode(t.value)
        if t.type==TokenType.LPAREN:
            self.advance(); n=self.expr(); self.expect(TokenType.RPAREN,msg="Expected ')' "); return n
        raise ParserError(f'Expected expression, got {t}')

class Environment:
    def __init__(self): self.variables={}
    def set(self,n,v): self.variables[n]=v
    def get(self,n):
        if n not in self.variables: raise RuntimeErrorPPL(f"Undefined variable '{n}'")
        return self.variables[n]

class Interpreter:
    def visit(self,node,env):
        if isinstance(node,NumberNode): return node.value
        if isinstance(node,VarAccessNode): return env.get(node.name)
        if isinstance(node,VarAssignNode):
            value=self.visit(node.value_node,env); env.set(node.name,value); return value
        if isinstance(node,PrintNode): print(self.visit(node.expr,env)); return None
        if isinstance(node,IfNode):
            if self.visit(node.condition,env):
                for stmt in node.body: self.visit(stmt,env)
            return None
        if isinstance(node,BinaryOpNode):
            a,b=self.visit(node.left,env),self.visit(node.right,env); op=node.op.type
            if op==TokenType.PLUS:return a+b
            if op==TokenType.MINUS:return a-b
            if op==TokenType.MUL:return a*b
            if op==TokenType.DIV:
                if b==0: raise RuntimeErrorPPL('Division by zero')
                return a/b
            if op==TokenType.DOUBLE_EQUALS:return a==b
            if op==TokenType.GREATER:return a>b
            if op==TokenType.LESS:return a<b
        raise RuntimeErrorPPL(f'Unknown node type: {type(node).__name__}')

def execute_program(source):
    program=Parser(Lexer(source).tokenize()).parse_program(); env=Environment(); interpreter=Interpreter()
    for stmt in program:
        result=interpreter.visit(stmt,env)
        if result is not None and not isinstance(stmt,(VarAssignNode,PrintNode,IfNode)): print(result)

def run_repl():
    print('Mini-Language REPL v1.0 - type exit to quit')
    while True:
        try:
            text=input('>> ')
            if text.strip().lower()=='exit': break
            if text.strip(): execute_program(text)
        except (LexerError,ParserError,RuntimeErrorPPL) as error: print(f'Error: {error}')

if __name__=='__main__': run_repl()
