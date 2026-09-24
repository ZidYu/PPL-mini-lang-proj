from .ast_nodes import *
class ParserError(Exception): pass
class Parser:
    def __init__(self,tokens): self.t=tokens; self.i=0
    def parse(self):
        s=[]
        while not self.check('EOF'): s.append(self.statement())
        return s
    def statement(self):
        if self.match('LET'): return self.var_decl()
        if self.match('PRINT'): return self.print_stmt()
        if self.match('IF'): return self.if_stmt()
        if self.match('WHILE'): return self.while_stmt()
        if self.match('FUNCTION'): return self.function_stmt()
        if self.match('RETURN'):
            value=None if self.check('SEMICOLON','END','RBRACE','EOF') else self.expression(); self.optional_endline(); return ReturnStatement(value)
        if self.match('LBRACE'): return Block(self.block('RBRACE'))
        if self.check('IDENTIFIER') and self.peek_next('EQUALS'):
            name=self.advance().value; self.consume('EQUALS','Expected ='); value=self.expression(); self.optional_endline(); return Assignment(name,value)
        expr=self.expression(); self.optional_endline(); return ExpressionStatement(expr)
    def var_decl(self):
        n=self.consume('IDENTIFIER','Expected variable name').value; self.consume('EQUALS','Expected ='); v=self.expression(); self.optional_endline(); return VarDeclaration(n,v)
    def print_stmt(self):
        if self.match('LPAREN'): e=self.expression(); self.consume('RPAREN','Expected )'); self.optional_endline(); return PrintStatement(e)
        e=self.expression(); self.optional_endline(); return PrintStatement(e)
    def if_stmt(self):
        self.match('LPAREN'); c=self.expression(); self.match('RPAREN'); self.match('COLON'); then=self.block_until('ELSE','END','RBRACE'); other=None
        if self.match('ELSE'): self.match('COLON'); other=self.block_until('END','RBRACE')
        self.match('END'); self.match('RBRACE'); return IfStatement(c,then,other)
    def while_stmt(self):
        self.match('LPAREN'); c=self.expression(); self.match('RPAREN'); self.match('COLON'); body=self.block_until('END','RBRACE'); self.match('END'); self.match('RBRACE'); return WhileStatement(c,body)
    def function_stmt(self):
        n=self.consume('IDENTIFIER','Expected function name').value; self.consume('LPAREN','Expected ('); p=[]
        if not self.check('RPAREN'):
            p.append(self.consume('IDENTIFIER','Expected parameter').value)
            while self.match('COMMA'): p.append(self.consume('IDENTIFIER','Expected parameter').value)
        self.consume('RPAREN','Expected )'); self.match('COLON'); body=self.block_until('END','RBRACE'); self.match('END'); self.match('RBRACE'); return FunctionStatement(n,p,body)
    def block_until(self,*stops):
        s=[]
        while not self.check(*stops,'EOF'): s.append(self.statement())
        return Block(s)
    def block(self,stop):
        s=[]
        while not self.check(stop,'EOF'): s.append(self.statement())
        self.consume(stop,f'Expected {stop}'); return s
    def expression(self): return self.or_expr()
    def or_expr(self):
        e=self.and_expr()
        while self.match('OR'): e=Logical(e,'or',self.and_expr())
        return e
    def and_expr(self):
        e=self.equality()
        while self.match('AND'): e=Logical(e,'and',self.equality())
        return e
    def equality(self):
        e=self.comparison()
        while self.match('EQUAL_EQUAL','NOT_EQUAL'): e=Binary(e,self.prev().value,self.comparison())
        return e
    def comparison(self):
        e=self.term()
        while self.match('GREATER','LESS','GREATER_EQUAL','LESS_EQUAL'): e=Binary(e,self.prev().value,self.term())
        return e
    def term(self):
        e=self.factor()
        while self.match('PLUS','MINUS'): e=Binary(e,self.prev().value,self.factor())
        return e
    def factor(self):
        e=self.unary()
        while self.match('STAR','SLASH'): e=Binary(e,self.prev().value,self.unary())
        return e
    def unary(self):
        if self.match('MINUS','BANG'): return Unary(self.prev().value,self.unary())
        return self.call()
    def call(self):
        e=self.primary()
        while self.match('LPAREN'):
            a=[]
            if not self.check('RPAREN'):
                a.append(self.expression())
                while self.match('COMMA'): a.append(self.expression())
            self.consume('RPAREN','Expected )'); e=Call(e,a)
        return e
    def primary(self):
        if self.match('NUMBER','STRING'): return Literal(self.prev().value)
        if self.match('TRUE'): return Literal(True)
        if self.match('FALSE'): return Literal(False)
        if self.match('IDENTIFIER'): return Variable(self.prev().value)
        if self.match('LPAREN'):
            e=self.expression(); self.consume('RPAREN','Expected )'); return e
        raise ParserError(f'Expected expression at line {self.peek().line}')
    def optional_endline(self): self.match('SEMICOLON')
    def match(self,*k):
        if self.check(*k): self.i+=1; return True
        return False
    def consume(self,k,msg):
        if self.check(k): return self.advance()
        raise ParserError(msg+f' at line {self.peek().line}')
    def check(self,*k): return self.peek().kind in k
    def advance(self):
        if not self.check('EOF'): self.i+=1
        return self.prev()
    def peek(self): return self.t[self.i]
    def prev(self): return self.t[self.i-1]
    def peek_next(self,k): return self.i+1<len(self.t) and self.t[self.i+1].kind==k
